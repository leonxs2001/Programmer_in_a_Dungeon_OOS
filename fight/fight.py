import pygame
from pygame.locals import *
import fight.player as player
import fight.menu as menu
from level import Level

class Fight(Level):
    def __init__(self):
        #Entities
        self.player = player.Player()
        self.bg = pygame.image.load("fight/image/bg.png")
        self.bg = pygame.transform.scale(self.bg, (1200, 675))
        self.menu = menu.Menu()

        # Assign Variables
    def update(self):
        self.menu.update()
        self.player.update() 
        if not self.menu.wait and self.player.ready:
            self.player.next_step()

    def give_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == K_SPACE:
                if self.player.ready:
                    self.player.next_step()
            elif event.key == K_RETURN:
                self.menu.wait = not self.menu.wait
        elif event.type == MOUSEBUTTONDOWN:
            if self.menu.is_mouse_on_next():
                if self.player.ready:
                    self.player.next_step()
            elif self.menu.is_mouse_on_play():
                self.menu.wait = not self.menu.wait

    def draw(self,screen):
        #Redisplay
        screen.blit(self.bg, (0,0))
        self.player.draw(screen)
        self.menu.draw(screen)
    
    