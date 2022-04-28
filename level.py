import pygame 

class Level(pygame.sprite.Sprite):
    state = 1#0 is main game. 1 is fighting game tec.
    def __init__(self):
        """Entities, Assign Variables etc"""
        super.__init__()
    def update(self):
        """Update everything important"""
        pass
    def draw(self, screen):
        """Draw everything important on the screen."""
        pass
    def give_event(self,event):
        """Get the Events and handle them"""
        pass
