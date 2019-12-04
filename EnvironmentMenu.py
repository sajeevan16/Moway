import os
import pygame

import Car
from Car import Car
import Rbcar
from Rbcar import Rbcar
import Rlcar
from Rlcar import Rlcar
import time
import math



from pygame.math import Vector2

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
        if pressed[pygame.K_RETURN] and self.timenow < time.time() - 0.4:
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

if __name__ == '__main__':
    game = EnvironmentMenu()
    while not game.exit:
        game.run()
    pygame.quit()
