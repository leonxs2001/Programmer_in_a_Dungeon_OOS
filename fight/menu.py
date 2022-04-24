import pygame
class Menu:
    def __init__(self):
        self.next_btn = pygame.image.load("fight/image/next_btn.png")
        self.next_btn_rect = self.next_btn.get_rect()
        self.next_btn_rect.right = 1020
        self.next_btn_rect.bottom = 638
        self.play_btn = pygame.image.load("fight/image/play_btn.png")
        self.stop_btn = pygame.image.load("fight/image/stop_btn.png")
        self.play_btn_rect = self.next_btn_rect.copy()
        self.play_btn_rect.left += 130
        self.wait = True
        
        #make the image more transparent
        self.next_btn.set_alpha(100)
        self.play_btn.set_alpha(100)

    def is_mouse_on_next(self):
        return self.next_btn_rect.collidepoint(pygame.mouse.get_pos())
        
    def is_mouse_on_play(self):
        return self.play_btn_rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        if self.is_mouse_on_next():
            self.next_btn.set_alpha(255)
        else:
            self.next_btn.set_alpha(100)

        if self.is_mouse_on_play():
            self.play_btn.set_alpha(255)
            self.stop_btn.set_alpha(255)
        else:
            self.play_btn.set_alpha(100)
            self.stop_btn.set_alpha(100)
        

    def draw(self, screen):
        screen.blit(self.next_btn, self.next_btn_rect)
        if self.wait:
            screen.blit(self.play_btn, self.play_btn_rect)
        else:
            screen.blit(self.stop_btn, self.play_btn_rect)
