import pygame 

class Level(pygame.sprite.Sprite):
    state = 2#0 is main game. 1 is fighting game 2 is codingview tec.
    def __init__(self):
        """Enteties, Assign Variables etc"""
    def update(self):
        """Update everything important"""
        pass
    def draw(self, screen):
        """Draw everything important on the screen."""
        pass
    def give_event(self,event):
        """Get the Events and handle them"""
        pass
