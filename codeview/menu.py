import pygame


class Menu:
    def __init__(self):
        size = pygame.Vector2(100, 75)
        # create the load Button
        self.load_btn = pygame.Surface(size)
        self.load_btn.fill((200, 130, 130))
        font = pygame.font.Font(None, 40)
        btn_text = font.render("Load", True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.load_btn.blit(btn_text, btn_text_rect)

        self.load_btn_rect = self.load_btn.get_rect()
        self.load_btn_rect.right = 1260
        self.load_btn_rect.bottom = 700

        # create the save Button
        self.save_btn = pygame.Surface(size)
        self.save_btn.fill((200, 130, 130))
        font = pygame.font.Font(None, 40)
        btn_text = font.render("Save", True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.save_btn.blit(btn_text, btn_text_rect)

        self.save_btn_rect = self.save_btn.get_rect()
        self.save_btn_rect.right = self.load_btn_rect.left - 20
        self.save_btn_rect.bottom = 700

        # create the delete Button
        self.delete_btn = pygame.Surface(size)
        self.delete_btn.fill((200, 130, 130))
        font = pygame.font.Font(None, 40)
        btn_text = font.render("Delete", True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.delete_btn.blit(btn_text, btn_text_rect)

        self.delete_btn_rect = self.delete_btn.get_rect()
        self.delete_btn_rect.right = self.save_btn_rect.left - 20
        self.delete_btn_rect.bottom = 700

    def is_mouse_on_delete(self):
        return self.delete_btn_rect.collidepoint(pygame.mouse.get_pos())

    def is_mouse_on_save(self):
        return self.save_btn_rect.collidepoint(pygame.mouse.get_pos())

    def is_mouse_on_load(self):
        return self.load_btn_rect.collidepoint(pygame.mouse.get_pos())

    def update(self):

        if self.is_mouse_on_delete():
            self.delete_btn.set_alpha(255)
        else:  # make the image more transparent
            self.delete_btn.set_alpha(100)

        if self.is_mouse_on_save():
            self.save_btn.set_alpha(255)
        else:  # make the image more transparent
            self.save_btn.set_alpha(100)

        if self.is_mouse_on_load():
            self.load_btn.set_alpha(255)
        else:  # make the image more transparent
            self.load_btn.set_alpha(100)

    def draw(self, screen):
        screen.blit(self.delete_btn, self.delete_btn_rect)
        screen.blit(self.save_btn, self.save_btn_rect)
        screen.blit(self.load_btn, self.load_btn_rect)
