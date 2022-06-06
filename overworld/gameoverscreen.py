import pygame

from sqlitedataaccess import SqliteDataAccess


class GameOverScreen:
    def __init__(self):

        self.size = pygame.Vector2(400, 400)

        self.heading = "Game Over!"
        self.build()

    def set_score(self, score):
        data_access = SqliteDataAccess()
        data_access.save_score(score)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Your time is {self.get_time_string(score)}!", True, (0, 0, 0))

        text_rect = text.get_rect()
        text_rect.center = (200, 90)
        self.frame_image.blit(text, text_rect)

        text = font.render(f"The 5 best times are:", True, (0, 0, 0))

        text_rect = text.get_rect()
        text_rect.center = (200, 120)
        self.frame_image.blit(text, text_rect)

        score_list = data_access.get_5_best_scores()

        centery = 160
        centerx = self.frame_rect.size[0] / 2

        for i, score_b in enumerate(score_list):
            text = font.render(f"{i}. {self.get_time_string(score_b)}", True, (0, 0, 0))
            text_rect = text.get_rect()

            text_rect.center = (centerx, centery)
            centery += text_rect.height
            self.frame_image.blit(text, text_rect)


    def get_time_string(self, time):
        seconds = int(time // 1000)

        minutes = int(seconds // 60)
        seconds -= 60 * minutes

        seconds = str(seconds)
        minutes = str(minutes)
        if len(seconds) == 1:
            seconds = "0" + seconds
        
        if len(minutes) == 1:
            minutes = "0" + minutes

        return f"{minutes}:{seconds}"
        
    def build(self):
        # draw the frame and the text in it
        self.frame_image = pygame.Surface(self.size)
        self.frame_image.fill((220, 220, 220))
        self.frame_rect = self.frame_image.get_rect()
        pygame.draw.rect(self.frame_image, (0, 0, 0), self.frame_rect, width=4)
        self.frame_rect.center = (640, 250)

        font = pygame.font.Font(None, 55)
        text = font.render(self.heading, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (200, 50)
        self.frame_image.blit(text, text_rect)

        # draw confirm Button
        self.button_size = pygame.Vector2(240, 60)
        self.confirm_button = pygame.Surface(self.button_size)
        self.confirm_button.fill((200, 200, 200))
        self.confirm_button_rect = self.confirm_button.get_rect()
        pygame.draw.rect(self.confirm_button, (0, 0, 0),
                         self.confirm_button_rect, width=2)
        self.confirm_button_rect.centery = 390
        self.confirm_button_rect.centerx = self.frame_rect.centerx

        font = pygame.font.Font(None, 40)
        text = font.render("Confirm!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = pygame.Vector2(self.confirm_button_rect.size) / 2
        self.confirm_button.blit(text, text_rect)

    def check_collision(self, mouse_position: pygame.Vector2):
        # check collision with the Button
        if self.confirm_button_rect.collidepoint(mouse_position):
            return True
        else:
            return False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.frame_image, self.frame_rect)

        screen.blit(self.confirm_button, self.confirm_button_rect)
