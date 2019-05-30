import unittest
import pygame
from Car import Car
from Rlcar import Rlcar
from Rbcar import Rbcar
import math


class UnitTestCar(unittest.TestCase):
    def setUp(self):
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.car_1 = Car(self.screen, 320, 180, angle=0)
        self.car_2 = Rbcar(self.screen, 320, 540, angle=0)
        self.car_3 = Rlcar(self.screen, 960, 180, angle=180)
        self.car_4 = Car(self.screen, 960, 540, angle=180)

    def test_car_is_crashed(self):
        self.assertEqual(self.car_1.car_is_crashed([3, 40, 8]), False)
        self.assertEqual(self.car_2.car_is_crashed([31, 1, 36]), True)
        self.assertEqual(self.car_3.car_is_crashed([1, 40, 1]), True)
        self.assertEqual(self.car_4.car_is_crashed([1, 1, 1]), True)
        self.assertEqual(self.car_2.car_is_crashed([32, 5, 6]), False)

    def test_calculate_reward(self):
        self.assertEqual(self.car_3.calculate_reward([20, 40, 20]), 90)
        self.assertEqual(self.car_3.calculate_reward([21, 32, 17]), 76.5)
        self.assertEqual(self.car_3.calculate_reward([24, 1, 27]), 39.75)

    def test_make_sonar_arm(self):
        arm_1 = [(352, 180), (355, 180), (358, 180), (361, 180), (364, 180), (367, 180), (370, 180), (373, 180), (376, 180), (379, 180), (382, 180), (385, 180), (388, 180), (391, 180), (394, 180), (397, 180), (400, 180), (403, 180), (406, 180), (409, 180), (412, 180), (415, 180), (418, 180), (421, 180), (424, 180), (427, 180), (430, 180), (433, 180), (436, 180), (439, 180), (442, 180), (445, 180), (448, 180), (451, 180), (454, 180), (457, 180), (460, 180), (463, 180), (466, 180), (469, 180)]
        self.assertEqual(self.car_1.make_sonar_arm(320,180), arm_1)

    def test_get_rotated_point(self):
        self.assertEqual(self.car_1.get_rotated_point(5.0,5.0,5,10,math.pi/2), (10,5))
        self.assertEqual(self.car_2.get_rotated_point(25, 25, 15, 25, math.pi), (35, 25))
        self.assertEqual(self.car_3.get_rotated_point(10, 10, 8, 8, 3*math.pi / 2), (12, 12))

    def test_get_track_or_not(self):
        self.assertEqual(self.car_1.get_track_or_not((255,255,255,255)), 1)
        self.assertEqual(self.car_2.get_track_or_not((0, 0, 0,255)), 0)
        self.assertEqual(self.car_3.get_track_or_not((0, 0, 165,255)), 1)
        self.assertEqual(self.car_4.get_track_or_not((0, 0, 0, 0)), 1)

    def test_car_is_crashed(self):
        self.assertEqual(self.car_1.car_is_crashed([40,40,40]), False)
        self.assertEqual(self.car_3.car_is_crashed([35,1,7]), True)
        self.assertEqual(self.car_4.car_is_crashed([3,6,5]), False)
        self.assertEqual(self.car_2.car_is_crashed([1,1,1]), True)

    def test_calculate_reward(self):
        self.assertEqual(self.car_3.calculate_reward([40, 40, 40]), 120.0)
        self.assertEqual(self.car_3.calculate_reward([35, 1, 25]), 46.5)
        self.assertEqual(self.car_3.calculate_reward([10, 40, 15]), 78.75)
        self.assertEqual(self.car_3.calculate_reward([1, 1, 1]), 3.0)

if __name__ == '__main__':
    unittest.main()