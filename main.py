#!/usr/bin/python
# -*- encoding utf-8 -*-

#Import and Initialize
import pygame
from pygame.locals import *
from codeview.codeview import CodeView
from fight.fight import Fight
from overworld.overworld import OverWorld
from level import Level 
pygame.init()
# Display
size = (1200, 675)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Labi")

# Enteties
fight_scene = Fight()
overworld = OverWorld()
code_view_scene = CodeView()
# Action --> ALTER
# Assign Variables
keep_going = True
clock = pygame.time.Clock()
# Loop
while keep_going:
    # Time
    clock.tick(30)

    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            keepGoing = False
            pygame.quit()
            break
        else:
            if Level.state == 0:
                overworld.give_event(event)
                pass
            elif Level.state == 1:
                fight_scene.give_event(event)  
            elif Level.state == 2:
                code_view_scene.give_event(event)

    #update
    if Level.state == 0:
        overworld.update()
        pass
    elif Level.state == 1:
        fight_scene.update()
    elif Level.state == 2:
        code_view_scene.update()

    # Redisplay
    if Level.state == 0:
        overworld.update()
        pass
    elif Level.state == 1:
        fight_scene.draw(screen)
    elif Level.state == 2:
        code_view_scene.draw(screen)
    pygame.display.flip()