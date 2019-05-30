import os
import pygame
import math
from math import tan, radians, degrees, copysign
import Car
import time
from Car import Car


from pygame.math import Vector2

width = 1280
height = 720
THECOLORS = pygame.color.THECOLORS


class Rbcar(Car):
    def __init__(self, screen, x, y, angle=0.0, length=3, max_steering=1, max_acceleration=520.0):
        Car.__init__(self, screen, x, y, angle, length, max_steering, max_acceleration)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "img/Rule-Based-Car.png")
        self.car_image = pygame.image.load(image_path)
        self.car_image = pygame.transform.scale(self.car_image, (54, 30))
    def run(self ,dt,side_over,front_over):
        side_over = side_over#20
        front_over = front_over#38
        sensors = self.get_sonar_readings(self.position[0],self.position[1],-(self.angle*math.pi/180.0))
        if sensors[0] > sensors[2]:
            self.action(1,dt)
        if sensors[0] < sensors[2]:
            self.action(2, dt)
        if sensors[0] == sensors[2]:
            if sensors[1] < sensors[2]:
                self.action(1, dt)
            else:
                self.action(0,dt)

