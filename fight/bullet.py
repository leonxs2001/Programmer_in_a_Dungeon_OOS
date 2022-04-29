from turtle import position
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position : pygame.Vector2, direction : pygame.Vector2):
        super().__init__()
        self.size = (12,12)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        speed = 15

        direction.scale_to_length(speed)
        self.movement = direction.copy()
        self.position = position.copy()

    def update(self, elapsed_time):
        movement = self.movement * (33.33 / elapsed_time)
        self.position += movement

        if self.position.x - self.size[0] < 0 or self.position.x + self.size[0] > 1200 or\
            self.position.y - self.size[1] < 0 or self.position.y + self.size[1] > 675:
            self.kill()


        self.rect.center = (self.position.x, self.position.y)
