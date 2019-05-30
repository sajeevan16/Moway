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