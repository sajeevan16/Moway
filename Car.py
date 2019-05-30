import os
import pygame
import math
from math import tan, radians, degrees, copysign
from pygame.math import Vector2
import random

width = 1280
height = 720
THECOLORS = pygame.color.THECOLORS

class Car:
    def __init__(self, screen, x, y, angle=0.0, length=3, max_steering=1, max_acceleration=240.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.startPosition = (x, y)
        self.angle = angle
        self.startangle = angle
        self.length = length
        self.max_acceleration = max_acceleration #+ random.randint(1,101)- 50
        self.max_steering = max_steering
        self.max_velocity = 60
        self.brake_deceleration = 70
        self.free_deceleration = 1000
        self.acceleration = 0.0
        self.steering = 0.0
        self.show_sensors = True
        self.screen = screen
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "img/car.png")
        self.car_image = pygame.image.load(image_path)
        self.car_image = pygame.transform.scale(self.car_image, (54, 30))

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        #CAR Drawing
        ppu =1
        rotated = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, self.position*ppu)

    def car_is_crashed(self, readings):
        if readings[0] == 1 or readings[1] == 1 or readings[2] == 1:
            return True
        else:
            return False

    def recover_from_crash(self):
        self.position = Vector2(self.startPosition[0], self.startPosition[1])
        self.angle = self.startangle
        self.velocity = Vector2(0.0, 0.0)
        self.acceleration = 0.0
        self.steering = 0.0



    def action(self,act,dt):
        if act==0: #Forward
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
                self.velocity += (self.brake_deceleration * dt * 2, 0)
            else:
                self.acceleration += 10 * 90 * dt
        if act ==4: #Break
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
                self.velocity -= (self.brake_deceleration * dt * 2, 0)
            else:
                self.acceleration -= 1 * 90 * dt
        if act == 1: #
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
                self.velocity += (self.brake_deceleration * dt * 2, 0)
            else:
                self.acceleration += 10 * 90 * dt
            self.angle -= 25 *dt
            #self.steering -= self.max_steering / 1 * dt
        if act == 2: #
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
                self.velocity += (self.brake_deceleration * dt * 2, 0)
            else:
                self.acceleration += 10 * 90 * dt
            self.angle += 25 * dt
            #self.steering += self.max_steering / 1 * dt
        if act == 3: # None input
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt


    def get_sonar_readings(self, x, y, angle, show_sensors=True):
        carsize = pygame.transform.rotate(self.car_image, self.angle).get_rect().size
        x = x+(carsize[0]/2)
        y = y+(carsize[1]/2)
        readings = []
        # Make our arms.
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.75))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.75))

        if show_sensors:
            pygame.display.update()
        return readings

    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0
        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1
            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return i  # Sensor is off the screen.
            else:
                obs = self.screen.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    return i

            if self.show_sensors:
                # print(rotated_p)
                # print("eeeeeeee")
                pygame.draw.circle(self.screen, (255, 255, 255), (rotated_p), 0)
                # pygame.draw.circle(self.screen, (0, 0, 255), (5,5), 2)
        # Return the distance for the arm.
        return i

    def make_sonar_arm(self, x, y):
        spread = 3  # Gap between sensors.
        distance = 32  # Gap between first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(0, 40):
            arm_points.append((distance + x + (spread * i), y))
            # print(arm_points)
        return arm_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = (y_change + y_1) # height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        # print(reading)
        if reading == THECOLORS['black']:
            return 0
        else:
            return 1
