import pygame
from Menu import Menu
from EnvironmentMenu import EnvironmentMenu
from Environment import Environment
import learning
import playing
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
            learning.train(environment,modelname[1])
        elif (modelname[0] == "Play"):
            saved_model = 'saved-models/'+str(modelname[1])+'.h5'
            model = playing.neural_net(playing.NUM_SENSORS, [128, 128], saved_model)
            playing.play(model, environment)
        if environment.returnmenu: continue
        if (menu.exit or Environmentmenu.exit or environment.exit): break


