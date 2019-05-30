import pygame
import os
import time
from pygame.math import Vector2
import math
import math
import numpy as np
import Environment
import numpy as np
from nn import neural_net
import numpy as np
import random
import csv
from nn import neural_net, LossHistory
import os.path
import timeit
from math import tan, radians, degrees, copysign
from pygame.math import Vector2

width = 1280
height = 800
pygame.init()
COLOR_INACTIVE = pygame.Color('black')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 48)



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
        self.max_acceleration = max_acceleration
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
        #print(carsize,"carsize")
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
        #print(sensors) #14 21 32 43
        if sensors[0] > sensors[2]:
            self.action(1,dt)
        if sensors[0] < sensors[2]:
            self.action(2, dt)
        if sensors[0] == sensors[2]:
            if sensors[1] < sensors[2]:
                self.action(1, dt)
            else:
                self.action(0,dt)



class Rlcar(Car):
    def __init__(self, screen, x, y, angle=0.0, length=3, max_steering=1, max_acceleration=520.0):
        Car.__init__(self, screen, x, y, angle, length, max_steering, max_acceleration)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "img/Autonomous-Car.png")
        self.car_image = pygame.image.load(image_path)
        self.car_image = pygame.transform.scale(self.car_image, (54, 30))

    def calculate_reward(self, readings):
        """Sum the number of non-zero readings."""
        tot = 0
        #print(readings)
        for i in readings:
            tot += i
        tot = readings[0]*0.75 + readings[1]*1.5 + readings[2]*0.75
        return tot

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(550, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


width = 1280
height = 780
THECOLORS = pygame.color.THECOLORS


class Menu:
    def __init__(self,Objects=[]):
        pygame.init()
        pygame.display.set_caption("Moway")
        width = 1280
        height = 780
        self.screen = pygame.display.set_mode((width, height))
        icon = pygame.image.load('img/icon.ico')
        pygame.display.set_icon(icon)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (125, 30)
        self.clock = pygame.time.Clock()
        self.Message = "Welcome to Moway"
        self.distace = 0.0
        self.ticks = 60
        self.input_box = InputBox(683, 276, 480, 48)
        self.exit = False
        self.ErrorMessage = ""
        self.timenow = time.time()

    def run(self):
        dt = self.clock.get_time() / 1000
        self.distace += 1
        #print(str(dt)+"clock
        # Event queue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mousepressed = event.pos
                if(683<self.mousepressed[0]<940 and 352<self.mousepressed[1]<408) and self.input_box.text!="":
                    if not os.path.exists('saved-models/' + str(self.input_box.text) + '.h5'):
                        return ("Train",self.input_box.text)
                    else:
                        self.timenow = time.time()
                        self.ErrorMessage = "The file already exists. Choose Another file name"
                if (979 < self.mousepressed[0]<1232 and 352<self.mousepressed[1] < 408) and self.input_box.text!="":
                    if os.path.exists('saved-models/'+str(self.input_box.text)+'.h5'):
                        return ("Play", self.input_box.text)
                    else:
                        self.timenow = time.time()
                        self.ErrorMessage = "This Model is Not Trained."
            self.input_box.handle_event(event)
        self.screen.fill((0, 0, 0))
        if self.timenow < time.time() - 2.5: self.ErrorMessage = ""
        map = pygame.image.load("img/menu.jpg")
        map = pygame.transform.scale(map, (1280, 800))
        self.screen.blit(map, (0,0))
        self.input_box.update()
        self.input_box.draw(self.screen)
        font = pygame.font.SysFont("arial", 24)
        text = font.render(self.ErrorMessage, True, (255, 0, 0))
        self.screen.blit(text,(683, 240))
        pygame.display.flip()
        self.clock.tick(self.ticks)
        return 0


THECOLORS = pygame.color.THECOLORS


class EnvironmentMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Moway")
        width = 1280
        height = 790
        self.timenow = time.time()
        self.screen = pygame.display.set_mode((width, height))
        icon = pygame.image.load('img/icon.ico')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.Message = "Welcome to Moway"
        self.distace = 0.0
        self.ticks = 60
        self.exit = False
        self.returnmenu = False
        self.MapList = ["Erangel","Vikendi","Sanhok","Miramar"]
        self.map = 0
        self.ObstacleList = ["Autonomous-Car"]
        self.obstacle = 0
        self.Objects = ["Map"]
        self.ismousepressed = False
        self.ErrorMessage = "Error "
        self.timenow = time.time()


    def run(self):
        dt = self.clock.get_time() / 1000
        # Event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousepressed = event.pos
                self.ismousepressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.ismousepressed = False
                self.mousereleased = event.pos
                p1 = Vector2(self.mousepressed[0], self.mousepressed[1])
                if(p1[1]>700): continue
                p2 = Vector2(self.mousereleased[0], self.mousereleased[1])
                _, angle = (p1 - p2).as_polar()
                angle = (180-angle)%360
                if(p1==p2): angle=0
                if(self.ObstacleList[self.obstacle % (len(self.ObstacleList))] in "Autonomous-Car__Rule-Based-Car"):
                    if(True):
                        car_image = pygame.transform.scale(pygame.image.load("img/car.png"), (50, 25))
                        carsize = pygame.transform.rotate(car_image, angle).get_rect().size
                        x = self.mousepressed[0] - (carsize[0] / 2)
                        y = self.mousepressed[1] - (carsize[1] / 2)
                        car = Rbcar(self.screen, x,y,angle=angle)

                        if (self.ObstacleList[self.obstacle % (len(self.ObstacleList))] in "Autonomous-Car"):
                            car = Rlcar(self.screen, x, y, angle=angle)
                            self.ObstacleList=["Rule-Based-Car", "Barrier","Stop", "Traffic-Cones", "Traffic-Cones-2"]
                        readings = car.get_sonar_readings(car.position[0], car.position[1],-(car.angle * math.pi / 180.0), show_sensors=False)
                        print(readings)
                        if not (1 in readings):

                            self.Objects.append(car)
                        else:
                            self.ErrorMessage = "Please establish the car only in the black area."
                            self.timenow = time.time()
                else:
                    obstaclesample = pygame.image.load("img/Obstacles/" + self.ObstacleList[self.obstacle % (len(self.ObstacleList))] + ".png")
                    obstaclesample=pygame.transform.rotate(obstaclesample, angle)
                    obssize = obstaclesample.get_rect().size
                    x = self.mousepressed[0] - (obssize[0] / 2)
                    y = self.mousepressed[1] - (obssize[1] / 2)
                    self.Objects.append((obstaclesample,(x,y)))
        angle = 0
        if self.ismousepressed:
            p1 = Vector2(self.mousepressed[0], self.mousepressed[1])
            pos1 = pygame.mouse.get_pos()
            p2 = Vector2(pos1[0], pos1[1])
            _, angle = (p1 - p2).as_polar()
            angle = (180 - angle) % 360
            if (p1 == p2): angle = 0

        mousecursor = pygame.image.load(
            "img/Obstacles/" + self.ObstacleList[self.obstacle % (len(self.ObstacleList))] + ".png")
        if "Car" in self.ObstacleList[self.obstacle % (len(self.ObstacleList))]:
            mousecursor = pygame.transform.scale(mousecursor, (54, 54))
        mousecursor = pygame.transform.rotate(mousecursor, angle)
        obssize = mousecursor.get_rect().size
        pos = pygame.mouse.get_pos()
        if self.ismousepressed: pos = self.mousepressed
        mx = pos[0] - (obssize[0] / 2)
        my = pos[1] - (obssize[1] / 2)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and self.timenow < time.time()-0.4:
            self.obstacle += 1
            self.timenow = time.time()
        elif pressed[pygame.K_DOWN] and self.timenow < time.time()-0.4:
            self.obstacle -= 1
            self.timenow = time.time()
        elif pressed[pygame.K_RIGHT] and self.timenow < time.time()-0.4:
            self.map += 1
            self.timenow = time.time()
            self.Objects = ["Map"]
        elif pressed[pygame.K_LEFT] and self.timenow < time.time()-0.4:
            self.map -= 1
            self.timenow = time.time()
            self.Objects = ["Map"]
        elif pressed[pygame.K_z] and self.timenow < time.time()-0.4:
            if (len(self.Objects)> 1):
                self.Objects.pop()
        if pressed[pygame.K_KP_ENTER] and self.timenow < time.time() - 0.4:
            if (len(self.Objects)> 1):
                return self.Objects
        if pressed[pygame.K_m]:
            self.returnmenu = True
            self.exit = True
        if (len(self.Objects) == 1):
            self.ObstacleList = ["Autonomous-Car"]
        self.screen.fill((0, 0, 0))
        map = pygame.image.load("img/map/"+self.MapList[self.map%(len(self.MapList))]+".png")
        map = pygame.transform.scale(map, (1280, 720))
        self.Objects[0] = map
        obstaclesample = pygame.image.load("img/Obstacles/" + self.ObstacleList[self.obstacle % (len(self.ObstacleList))] + ".png")
        obstaclesample = pygame.transform.scale(obstaclesample, (70, 70))
        self.screen.blit(obstaclesample, (300+12*len(self.ObstacleList[self.obstacle%(len(self.ObstacleList))]),725))
        self.screen.blit(self.Objects[0], (0,0))
        font = pygame.font.SysFont("arial", 24)
        text = font.render("Map : "+self.MapList[self.map%(len(self.MapList))], True, (255, 255, 255))
        text2 = font.render("Object Add : "+self.ObstacleList[self.obstacle%(len(self.ObstacleList))], True, (255, 255, 255))
        self.screen.blit(text,(20,735))
        self.screen.blit(text2, (200, 735))
        font = pygame.font.SysFont("arial", 20)
        self.screen.blit(font.render("Press 'Z' to Undo", True, (255, 255, 255)), (970, 730))
        self.screen.blit(font.render("Press 'M' to Menu", True, (255, 255, 255)), (970, 755))
        self.screen.blit(font.render("Change the Map Using RIGHT, LEFT Arrows", True, (255, 255, 255)), (570, 730))
        self.screen.blit(font.render("Change the Objects Using UP, DOWN Arrows", True, (255, 255, 255)), (570, 755))
        enterimg = pygame.image.load("img/enter.jpg")
        self.screen.blit(enterimg,(1150, 725))
        self.screen.blit(mousecursor, (mx, my))
        for item in self.Objects[1:]:
            if isinstance(item,Car):
                item.update(dt)
            else:
                self.screen.blit(item[0],item[1])

        if self.timenow < time.time() - 2.5:
            self.ErrorMessage = ""
        font = pygame.font.SysFont("arial", 24)
        text = font.render(self.ErrorMessage, True, (255, 0, 0))
        self.screen.blit(text, (30, 670))

        self.screen.blit(mousecursor, (mx, my))

        pygame.display.flip()
        self.clock.tick(self.ticks)
        return 0



width = 1280
height = 780
THECOLORS = pygame.color.THECOLORS


class Environment:
    def __init__(self,Objects=[]):
        pygame.init()
        pygame.display.set_caption("Moway")
        width = 1280
        height = 780
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.Message = "Welcome to Moway"
        self.distance = 0.0
        self.ticks = 60
        self.exit = False
        self.Objects = Objects
        self.savemsgtext = "Press 'S' to Save"
        self.returnmenu = False

    def setMessage(self,Message):
        self.Message = Message

    def setSaveMsg(self, Message):
        self.savemsgtext = Message

    def run(self,act,Model):
        dt = self.clock.get_time() / 1000
        self.distance += 1
        #print(str(dt)+"clock")
        # Event queue
        SAVE = False
        for item in self.Objects[2:]:
            if isinstance(item,Rbcar):
                item.run(dt,8,20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_s]:
            SAVE = True
        if pressed[pygame.K_m]:
            self.returnmenu = True
            self.exit = True
        self.Objects[1].action(act,dt)
        # print(self.Objects[1].position,(self.Objects[1].angle*math.pi/180.0)%2*math.pi)
        # print("CAR - position, angle")
        # print("Sensor R,M,L - ",self.Objects[1].get_sonar_readings(self.Objects[1].position[0],self.Objects[1].position[1],-(self.Objects[1].angle*math.pi/180.0)))
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.Objects[0], (0,0))
        font = pygame.font.SysFont("arial", 18)
        text = font.render(self.Message, True, (255, 255, 255))
        self.screen.blit(text,(20,735))
        if (Model=="T"):
            savemsg = font.render(self.savemsgtext, True, (255, 255, 255))
            self.screen.blit(savemsg, (1120, 725))
        self.screen.blit(font.render("Press 'M' to Menu", True, (255, 255, 255)), (1120, 750))
        for item in self.Objects[1:]:
            if isinstance(item,Car):
                item.update(dt)
            else:
                self.screen.blit(item[0],item[1])
        pygame.display.flip()
        self.clock.tick(self.ticks)
        # Get the current location and the readings there.
        x, y = self.Objects[1].position
        readings = self.Objects[1].get_sonar_readings(x,y,-(self.Objects[1].angle*math.pi/180.0))
        normalized_readings = [(rx-20.0)/20.0 for rx in readings]
        state = np.array([normalized_readings])
        # Set the reward.num_steps
        # Car crashed when any reading == 1
        if self.Objects[1].car_is_crashed(readings):
            self.distance = 0
            reward = -750
            for item in self.Objects[1:]:
                if isinstance(item, Car):
                    item.recover_from_crash()
        else:
            # Higher readings are better, so return the sum.
            reward = -5 + int(self.Objects[1].calculate_reward(readings)/ 3) #+ (self.distance**0.1)
        #self.Objects[1].num_steps += 1
        #print (reward, state)
        return reward, state, SAVE



NUM_SENSORS = 3


def play(model,environment):

    car_distance = 0
    # Create a new game instance.
    game_state = environment

    # Get initial state by doing nothing and getting the state.
    _, state, _ = game_state.run(2,"P")

    # Move.
    while not game_state.exit:
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))
        #print(action)

        # Take action.
        _, state, _ = game_state.run(action,"P")

        # Tell us something.
        if car_distance % 1000 == 0:
            pass#print("Current distance: %d frames." % car_distance)
    pygame.quit()



NUM_INPUT = 3
GAMMA = 0.9 # Forgetting.
TUNING = False  # If False, just use arbitrary, pre-selected params.

def train_net(model, params, environment, modelname="untitle", train_frames = 10000):
    filename = modelname#params_to_filename(params)
    observe = 1000  # Number of frames to observe before training.
    epsilon = 1
    train_frames = train_frames  # Number of frames to play.
    batchSize = params['batchSize']
    buffer = params['buffer']

    # Just stuff used below.
    max_car_distance = 0
    car_distance = 0
    t = 0
    data_collect = []
    replay = []  # stores tuples of (S, A, R, S').
    loss_log = []

    # Create a new game instance.
    game_state = environment

    # Get initial state by doing nothing and getting the state.
    _, state, SAVE = game_state.run(0,"T")

    # Let's time it.
    start_time = timeit.default_timer()

    # Run the frames.
    while (t < train_frames) and not game_state.exit:
        t += 1
        car_distance += 1
        # Choose an action.
        if random.random() < epsilon or t < observe:
            action = np.random.randint(0, 3)  # random
        else:
            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            action = (np.argmax(qval))  # best

        # Take action, observe new state and get our treat.
        reward, new_state, SAVE = game_state.run(action,"T")

        # Experience replay storage.
        replay.append((state, action, reward, new_state))

        # If we're done observing, start training.
        if t > observe:

            # If we've stored enough in our buffer, pop the oldest.
            if len(replay) > buffer:
                replay.pop(0)

            # Randomly sample our experience replay memory
            minibatch = random.sample(replay, batchSize)

            # Get training values.
            X_train, y_train = process_minibatch2(minibatch, model)

            # Train the model on this batch.
            history = LossHistory()
            model.fit(
                X_train, y_train, batch_size=batchSize,
                nb_epoch=1, verbose=0, callbacks=[history]
            )
            loss_log.append(history.losses)

        # Update the starting state with S'.
        state = new_state

        # Decrement epsilon over time.
        if epsilon > 0.1 and t > observe:
            epsilon -= (1.0/train_frames)
            #print(epsilon, "epsilon")

        # We died, so update stuff.
        if reward == -750:
            # Log the car's distance at this T.
            data_collect.append([t, car_distance])

            # Update max.
            if car_distance > max_car_distance:
                max_car_distance = car_distance

            # Time it.
            tot_time = timeit.default_timer() - start_time
            fps = car_distance / tot_time

            # Output some stuff so we can watch.
            #print("Max: %d at %d\tepsilon %f\t(%d)\t%f fps" %(max_car_distance, t, epsilon, car_distance, fps))
            Msg = ("TRAINING -     Epsilon Value : %f      Max Distance : %d      Last Distance : %d      Total Frams: %d      fps: %f" %(epsilon, max_car_distance, car_distance, t, fps))
            game_state.setMessage(Msg)
            # Reset.
            car_distance = 0
            start_time = timeit.default_timer()

        # Save the model every 25,000 frames.
        #print(SAVE, t)
        if t % 5000 == 0 or SAVE:
            SAVE = False
            game_state.setSaveMsg("Last Save at "+str(t))
            model.save_weights('saved-models/' + filename +'.h5',overwrite=True)
            print("Saving model %s - %d" % (filename, t))

    # Log results after we're done all frames.
    log_results(filename, data_collect, loss_log)


def log_results(filename, data_collect, loss_log):
    # Save the results to a file so we can graph it later.
    with open('results/sonar-frames/learn_data-' + filename + '.csv', 'w') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('results/sonar-frames/loss_data-' + filename + '.csv', 'w') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)

def process_minibatch2(minibatch, model):
    # by Microos, improve this batch processing function
    #   and gain 50~60x faster speed (tested on GTX 1080)
    #   significantly increase the training FPS

    # instead of feeding data to the model one by one,
    #   feed the whole batch is much more efficient

    mb_len = len(minibatch)

    old_states = np.zeros(shape=(mb_len, 3))
    actions = np.zeros(shape=(mb_len,))
    rewards = np.zeros(shape=(mb_len,))
    new_states = np.zeros(shape=(mb_len, 3))

    for i, m in enumerate(minibatch):
        old_state_m, action_m, reward_m, new_state_m = m
        old_states[i, :] = old_state_m[...]
        actions[i] = action_m
        rewards[i] = reward_m
        new_states[i, :] = new_state_m[...]

    old_qvals = model.predict(old_states, batch_size=mb_len)
    new_qvals = model.predict(new_states, batch_size=mb_len)

    maxQs = np.max(new_qvals, axis=1)
    y = old_qvals
    non_term_inds = np.where(rewards != -750)[0]
    term_inds = np.where(rewards == -750)[0]

    y[non_term_inds, actions[non_term_inds].astype(int)] = rewards[non_term_inds] + (GAMMA * maxQs[non_term_inds])
    y[term_inds, actions[term_inds].astype(int)] = rewards[term_inds]

    X_train = old_states
    y_train = y
    return X_train, y_train

def process_minibatch(minibatch, model):
    """This does the heavy lifting, aka, the training. It's super jacked."""
    X_train = []
    y_train = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in minibatch:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        # Get our predicted best move.
        maxQ = np.max(newQ)
        y = np.zeros((1, 3))
        y[:] = old_qval[:]
        # Check for terminal state.
        if reward_m != -750:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update
        X_train.append(old_state_m.reshape(NUM_INPUT,))
        y_train.append(y.reshape(3,))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train


def params_to_filename(params):
    return str(params['nn'][0]) + '-' + str(params['nn'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


def launch_learn(params,environment, modelname):
    filename = modelname
    print("Trying %s" % filename)
    # Make sure we haven't run this one.
    if not os.path.isfile('results/sonar-frames/loss_data-' + filename + '.csv'):
        # Create file so we don't double test when we run multiple
        # instances of the script at the same time.
        open('results/sonar-frames/loss_data-' + filename + '.csv', 'a').close()
        print("Starting test.")
        # Train.
        model = neural_net(NUM_INPUT, params['nn'])
        train_net(model, params, environment, modelname)
    else:
        print("Already tested.")

def train(environment, modelname="untitle"):
    if TUNING:
        param_list = []
        nn_params = [[164, 150], [256, 256],
                     [512, 512], [1000, 1000]]
        batchSizes = [40, 100, 400]
        buffers = [10000, 50000]
        for nn_param in nn_params:
            for batchSize in batchSizes:
                for buffer in buffers:
                    params = {
                        "batchSize": batchSize,
                        "buffer": buffer,
                        "nn": nn_param
                    }
                    param_list.append(params)

        for param_set in param_list:
            launch_learn(param_set, environment, modelname)
    else:
        nn_param = [128, 128]
        params = {
            "batchSize": 64,
            "buffer": 50000,
            "nn": nn_param
        }
        model = neural_net(NUM_INPUT, nn_param)
        train_net(model, params, environment, modelname)




pygame.init()
if (True):
    menu = Menu()
    Environmentmenu = EnvironmentMenu()

    while (True):
        menu = Menu()
        Environmentmenu = EnvironmentMenu()
        modelname=(0,0)
        objlist = 0
        while not menu.exit:
            modelname = menu.run()
            if modelname!=0: break
        if (menu.exit or Environmentmenu.exit): break
        while not Environmentmenu.exit:
            objlist = Environmentmenu.run()
            if objlist!=0:
                break
        if Environmentmenu.returnmenu: continue
        if (menu.exit or Environmentmenu.exit): break
        environment = Environment(objlist)
        if(modelname[0]=="Train"):
            train(environment,modelname[1])
        elif (modelname[0] == "Play"):
            saved_model = 'saved-models/'+str(modelname[1])+'.h5'
            model = neural_net(NUM_SENSORS, [128, 128], saved_model)
            play(model, environment)
        if environment.returnmenu: continue
        if (menu.exit or Environmentmenu.exit or environment.exit): break


