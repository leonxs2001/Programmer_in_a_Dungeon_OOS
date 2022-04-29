import pygame
from fight.player import Player

class Opponent(Player):
    def __init__(self,initial_sequence_string,sequence_string):
        super().__init__(initial_sequence_string,sequence_string)
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect.center = (1100, 337)
        self.position = pygame.Vector2(self.rect.topleft)