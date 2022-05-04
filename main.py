import pygame
import os
import time
import math
import random
import json
import os
import os, sys


from _gui                   import *
from _gameState             import *
from _input                 import *
from _utils                 import *
from _player                import *


#----------------------------------------
"""
Reusable classes
GUI- it contains width,height,font and userinput








"""
#----------------------------------------

# -----------VARIABLES & FLAGS

white          = (255,255,255)
green          = (0,255,0)
blue           = (176,224,230)
FPS            = 90
width, height  = 1280,720
themeColour    = (128,0,0)
time = 0


# ---------------PYGAME

pygame.init()
pygame.display.set_caption("Fitba")
clock          = pygame.time.Clock()
nextFrame      = pygame.time.get_ticks()
screen         = pygame.display.set_mode((width,height),pygame.DOUBLEBUF)
#phoneScreen    = pygame.display.set_mode((405,544),pygame.DOUBLEBUF)
pygame.time.set_timer(pygame.USEREVENT, 20)

font        = pygame.font.Font('fonts/nokiafc22.ttf', 32)



# ---------------CLASS OBJECTS
gui                   = gui(screen,width,height,font)
user_input            = userInputObject("","",(0.27,0.65,0.45,0.08), gui)
modifyInput           = manageInput()


# -----------game objects

footballSpriteList     = importFiles('foo',3,tDir='sprites/football/')
footballSprite         = sprite(footballSpriteList,gui.width/2,gui.height/2)
fitba                  = fitbaObject(footballSprite)

playerSSW            = importFiles('ssW',3,tDir='sprites/players/ssw/')
tDir='sprites/players/ssw/'
playerSSW            = [pygame.image.load(tDir+'ssW1.png'),pygame.image.load(tDir+'ssW2.png'),pygame.image.load(tDir+'ssW3.png'),pygame.image.load(tDir+'ssW4.png'),pygame.image.load(tDir+'ssW5.png'),pygame.image.load(tDir+'ssW6.png'),pygame.image.load(tDir+'ssW7.png'),pygame.image.load(tDir+'ssW8.png'),pygame.image.load(tDir+'ssW9.png'),pygame.image.load(tDir+'ssW10.png'),pygame.image.load(tDir+'ssW11.png'),pygame.image.load(tDir+'ssW12.png')]
playerSprite         = playerSprite(playerSSW)
player               = playerObject(playerSprite,gui.width/2,gui.height/3,2.5,1.8)





# ****TurnDebug on/off***
gui.debugSwitch = False 

# ---------------setup finished

gui.itercount = 0
while gui.running:
    gui.itercount+=1

    screen.fill((10, 100, 10))
    gui.clicked = False
    # Reset the key each round
    user_input.returnedKey=''

    # Did the user click the window close button?
    for event in pygame.event.get():
        pos            = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: gui.running = False
        if event.type == pygame.MOUSEBUTTONDOWN: gui.clicked  = True
        user_input     = modifyInput.manageButtons(event,user_input,gui)

    # Update GUI with dynamic vars
    gui.userInput  = user_input
    gui.mx, gui.my = pygame.mouse.get_pos()


    fitba.updateSprite(gui)

    player.play_selected(gui,fitba)

    #if(user_input.kick): print('Ball kicked')


        










    # Flip the display
    pygame.display.flip()
    # Tick
    gui.dt           = clock.tick(FPS)
    gui.gameElapsed += gui.dt/1000
    continue

# Done! Time to quit.
pygame.quit()