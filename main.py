#!/usr/bin/python
# -*- encoding utf-8 -*-

#Import and Initialize
import pygame
from pygame.locals import *
from fight.fight import Fight
from overworld.overworld import OverWorld

pygame.init()
# Display
size = (1200, 675)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Labi")

# Enteties
fight_scene = Fight()
overworld = OverWorld()
# Action --> ALTER
# Assign Variables
keep_going = True
clock = pygame.time.Clock()
state = 1
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
            if state == 0:
                overworld.give_event(event)
                pass
            elif state == 1:
                fight_scene.give_event(event)  

    #update
    if state == 0:
        overworld.update()
        pass
    elif state == 1:
        fight_scene.update()

    # Redisplay
    if state == 0:
        overworld.update()
        pass
    elif state == 1:
        fight_scene.draw(screen)
    pygame.display.flip()