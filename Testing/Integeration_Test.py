import unittest
import pygame
from Car import Car
from Rlcar import Rlcar
from Rbcar import Rbcar
import math
import learning
import csv


class IntegerationTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_log_results(self):
        learning.log_results("test1", [[43, 43], [91, 48]], [], istest=True)
        with open('../results/sonar-frames/learn_data-test1.csv') as csvfile:
            learndata = list(csv.reader(csvfile, delimiter=','))
            self.assertIn (['43', '43'], learndata)
            self.assertIn(['91', '48'], learndata)

        learning.log_results("test2", [[12, 78], [95, 28], [34, 67]], [], istest=True)
        with open('../results/sonar-frames/learn_data-test2.csv') as csvfile:
            learndata = list(csv.reader(csvfile, delimiter=','))
            self.assertIn(['34', '67'], learndata)
            self.assertIn(['12', '78'], learndata)
            self.assertIn(['95', '28'], learndata)


if __name__ == '__main__':
    unittest.main()