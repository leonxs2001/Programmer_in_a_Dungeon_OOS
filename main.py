#Import and Initialize
import pygame
from pygame.locals import *
from fight.fight import Fight
from overworld.overworld import OverWorld
pygame.init()

# Display
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Programmer in the Dungeon")

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
            overworld.give_event(event)
    # update
    overworld.update()
    overworld.draw(screen)
    # Redisplay
    pygame.display.flip()
