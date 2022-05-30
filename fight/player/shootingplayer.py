import pygame
from fight.player.player import Player
from fight.player.bullet import Bullet
from overworld.config import asset
class ShootingPlayer(Player):
    def __init__(self,initial_sequence_string : str, sequence_string : str, is_opponent : bool):
        super().__init__(initial_sequence_string, sequence_string, is_opponent)
        self.bullet_group = pygame.sprite.Group()
        self.shoot_delay = 2000 #min delay between the single shoots in ms
        self.elapsed_time = self.shoot_delay + 1

    def load_image(self, is_opponent):
        if is_opponent:
            return pygame.image.load(asset["shooting_e"])
        else:
            return super().load_image(is_opponent)
            
    def update(self, elapsed_time):
        if self.elapsed_time <= self.shoot_delay:
            self.elapsed_time += elapsed_time
        super().update(elapsed_time)
        self.bullet_group.update(elapsed_time)
    def draw(self, screen: pygame.Surface):
        self.bullet_group.draw(screen)
        return super().draw(screen)
    def call_method(self, name : str, parameters : tuple):
        if name == "shoot":
            if len(parameters) == 0:#shoots in movementdirection
                self.shoot(self.movement)
            else:#shoots in given direction
                if len(parameters) == 2:
                    x, y = parameters
                else:#if parameter is a tupel
                    x, y = parameters[0]
                self.shoot(pygame.Vector2(x,y))
        elif name == "shootTo":
            if len(parameters) == 2:
                x, y = parameters
            else:#if parameter is a tupel
                x, y = parameters[0]
            direction =pygame.Vector2(x,y) - pygame.Vector2(self.rect.center)
            self.shoot(direction)
        else:
            return super().call_method(name, parameters)# give it back to the superclass

    def shoot(self, direction : pygame.Vector2):
        if self.elapsed_time > self.shoot_delay:
            position_center = self.position + (pygame.Vector2(self.size)/2)
            self.bullet_group.add(Bullet(position_center ,direction))
            self.elapsed_time = 0