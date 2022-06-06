import pygame


class GameOverScreen:
    def __init__(self):

        self.size = pygame.Vector2(400, 220)

        self.heading = "Game Over!"
        self.build()

    def build(self):
        # draw the frame and the text in it
        self.frame_image = pygame.Surface(self.size)
        self.frame_image.fill((220, 220, 220))
        self.frame_rect = self.frame_image.get_rect()
        pygame.draw.rect(self.frame_image, (0, 0, 0), self.frame_rect, width=4)
        self.frame_rect.center = (640, 250)

        font = pygame.font.Font(None, 45)
        text = font.render(self.heading, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (200, 40)
        self.frame_image.blit(text, text_rect)

        # draw confirm Button
        self.button_size = pygame.Vector2(240, 60)
        self.confirm_button = pygame.Surface(self.button_size)
        self.confirm_button.fill((200, 200, 200))
        self.confirm_button_rect = self.confirm_button.get_rect()
        pygame.draw.rect(self.confirm_button, (0, 0, 0),
                         self.confirm_button_rect, width=2)
        self.confirm_button_rect.centery = 300
        self.confirm_button_rect.centerx = self.frame_rect.centerx

        font = pygame.font.Font(None, 40)
        text = font.render("Confirm!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = pygame.Vector2(self.confirm_button_rect.size) / 2
        self.confirm_button.blit(text, text_rect)

    def set_state(self, state):
        font = pygame.font.Font(None, 45)
        self.state = state
        if state:
            text = font.render("You win!", True, (0, 0, 0))
        else:
            text = font.render("You lose!", True, (0, 0, 0))

        text_rect = text.get_rect()
        text_rect.center = (200, 80)
        self.frame_image.blit(text, text_rect)

    def check_collision(self, mouse_position: pygame.Vector2):
        # check collision with the Button
        if self.confirm_button_rect.collidepoint(mouse_position):
            return True
        else:
            return False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.frame_image, self.frame_rect)

        screen.blit(self.confirm_button, self.confirm_button_rect)
