import pygame
class Menu:
    def __init__(self):
        self.play_btn = pygame.image.load("fight/image/play_btn.png")
        self.stop_btn = pygame.image.load("fight/image/stop_btn.png")
        self.play_btn_rect = self.play_btn.get_rect()
        self.play_btn_rect.right = 1260
        self.play_btn_rect.bottom = 700
        self.wait = True
        
    def is_mouse_on_play(self):
        return self.play_btn_rect.collidepoint(pygame.mouse.get_pos())

    def update(self):

        if self.is_mouse_on_play():
            self.play_btn.set_alpha(255)
            self.stop_btn.set_alpha(255)
        else:#make the image more transparent
            self.play_btn.set_alpha(100)
            self.stop_btn.set_alpha(100)
        

    def draw(self, screen):
        if self.wait:
            screen.blit(self.play_btn, self.play_btn_rect)
        else:
            screen.blit(self.stop_btn, self.play_btn_rect)
