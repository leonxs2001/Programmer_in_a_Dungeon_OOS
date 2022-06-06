import pygame


class Menu:
    def __init__(self):
        size = pygame.Vector2(100, 75)
        # create the load Button
        self.play_btn = pygame.Surface(size)
        self.play_btn.fill((100, 100, 100))
        font = pygame.font.Font(None, 55)
        btn_text = font.render("Play", True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.play_btn.blit(btn_text, btn_text_rect)

        # create the save Button
        self.stop_btn = pygame.Surface(size)
        self.stop_btn.fill((100, 100, 100))
        btn_text = font.render("Stop", True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.stop_btn.blit(btn_text, btn_text_rect)

        self.btn_rect = self.play_btn.get_rect()
        self.btn_rect.bottom = 700
        self.btn_rect.right = 1260
        self.wait = True

    def is_mouse_on_play(self):
        return self.btn_rect.collidepoint(pygame.mouse.get_pos())

    def update(self):

        if self.is_mouse_on_play():
            self.play_btn.set_alpha(255)
            self.stop_btn.set_alpha(255)
        else:  # make the image more transparent
            self.play_btn.set_alpha(100)
            self.stop_btn.set_alpha(100)

    def draw(self, screen):
        if self.wait:
            screen.blit(self.play_btn, self.btn_rect)
        else:
            screen.blit(self.stop_btn, self.btn_rect)
