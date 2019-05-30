import os
import pygame

from math import tan, radians, degrees, copysign
import Car
from Car import Car
import Rbcar
from Rbcar import Rbcar
import Rlcar
from Rlcar import Rlcar

import random
import math
import numpy as np



from pygame.math import Vector2

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

if __name__ == '__main__':
    game = Environment()
    while not game.exit:
        game.run(1,"S")
    pygame.quit()
