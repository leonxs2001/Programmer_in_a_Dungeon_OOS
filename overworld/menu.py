import pygame


class Menu:
    def __init__(self):
        size = pygame.Vector2(100, 30)
        # create the code Button
        self.code_btn = pygame.Surface(size)
        self.code_btn.fill((255, 254, 254))
        font = pygame.font.Font(None, 40)
        btn_text = font.render("Code", True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.code_btn.blit(btn_text, btn_text_rect)

        self.code_btn_rect = self.code_btn.get_rect()
        self.code_btn_rect.right = 1260
        self.code_btn_rect.bottom = 715

    def is_mouse_on_code(self):
        return self.code_btn_rect.collidepoint(pygame.mouse.get_pos())

    def update(self):

        if self.is_mouse_on_code():
            self.code_btn.set_alpha(255)
        else:  # make the image more transparent
            self.code_btn.set_alpha(100)

    def draw(self, screen):
        screen.blit(self.code_btn, self.code_btn_rect)
