import pygame
from InputBox import InputBox
import os
import time


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


if __name__ == '__main__':
    game = Menu()
    while not game.exit:
        game.run()
    pygame.quit()