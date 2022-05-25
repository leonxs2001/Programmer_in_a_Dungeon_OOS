#Import and Initialize
import pygame
from pygame.locals import *
from fight.fight import Fight
from overworld.overworld import OverWorld
from level import Level 

pygame.init()
# Display
size = (1280,720) #Understandabl
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Labi")

# Entities
fight_scene = Fight()
overworld = OverWorld()
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
                
            elif Level.state == 1:
                fight_scene.give_event(event)  

    #update
    if Level.state == 0:
        overworld.update()
        
    elif Level.state == 1:
        fight_scene.update()

    # Redisplay
    if Level.state == 0:
        overworld.draw(screen)
    elif Level.state == 1:
        fight_scene.draw(screen)
    pygame.display.flip()