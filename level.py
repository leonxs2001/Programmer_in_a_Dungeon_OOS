import pygame 

class Level(pygame.sprite.Sprite):
    state = 0#0 is main game. 1 is fighting game tec. 2 is code view
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
