import pygame
class SelectionInput:
    def __init__(self, heading, data = ()):
        self.size = pygame.Vector2(400,400)
        self.heading = heading
        self.data = data
        self.build()
        
    def load(self, data):
        self.data = data
        self.build()

    def build(self):
        #draw the frame and the text in it
        self.frame_image = pygame.Surface(self.size)
        self.frame_image.fill((220,220,220))
        self.frame_rect = self.frame_image.get_rect()
        pygame.draw.rect(self.frame_image, (0,0,0), self.frame_rect, width=4)
        self.frame_rect.center = (640, 250)

        font = pygame.font.Font(None, 45)
        self.text = font.render(self.heading, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pygame.Vector2(200, 40) + self.frame_rect.topleft

        #draw the scroll background
        self.scroll_background = pygame.Surface((300, 230))
        self.scroll_background.fill((190,190,190))
        self.scroll_background_rect = self.scroll_background.get_rect()
        self.scroll_background_rect.center = self.frame_rect.center
        self.scroll_background_rect.top -= 14

        #create the buttons for the selection
        self.selection_buttons = []
        button = pygame.Surface((280, 38))
        button.fill((150, 150, 150))
        rect = button.get_rect()
        pygame.draw.rect(button, (0,0,0), rect, width=2)
        rect.centerx = self.scroll_background_rect.centerx

        distance = 6
        y = self.scroll_background_rect.top + distance + 2

        for date in self.data:
            #copy the template buttton and rect
            new_button = button.copy()
            new_rect = rect.copy()

            font = pygame.font.Font(None, 30)
            text = font.render(date[0], True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = pygame.Vector2(new_button.get_size()) / 2
            new_button.blit(text, text_rect)

            new_rect.top = y
            y += rect.height + distance
            
            self.selection_buttons.append((new_button, new_rect, date[1]))

        self.button_size = pygame.Vector2(250, 60)
        #draw cancel button
        self.cancel_button = pygame.Surface(self.button_size)
        self.cancel_button.fill((190,190,190))
        self.cancel_button_rect = self.cancel_button.get_rect()
        pygame.draw.rect(self.cancel_button, (0,0,0), self.cancel_button_rect, width=2)
        self.cancel_button_rect.centerx = 640
        self.cancel_button_rect.bottom = self.frame_rect.bottom - 20

        text = font.render("Cancel!", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (125, 30)
        self.cancel_button.blit(text, text_rect)

        #create cover up rect
        self.cover_up_rect = pygame.rect.Rect(self.scroll_background_rect.left, 0, self.scroll_background_rect.width, 60)
            
    def check_collision(self, mouse_position : pygame.Vector2):

        for button in self.selection_buttons:
            rect = button[1]
            if rect.bottom > self.scroll_background_rect.bottom + 60:
                break
            elif rect.top > self.scroll_background_rect.top - 60:
                if button[1].collidepoint(mouse_position):
                    return button[2]#return the pressed id

        if self.cancel_button_rect.collidepoint(mouse_position):#return true if ready
            return True

    def scroll(self, scrollment):
        if self.scroll_background_rect.collidepoint(pygame.mouse.get_pos()):
            scrollment *= 12
            if len(self.selection_buttons) > 0:
                max = self.scroll_background_rect.top + 8
                max2 = self.scroll_background_rect.bottom - 8
                if self.selection_buttons[0][1].top + scrollment > max:
                    scrollment = max - self.selection_buttons[0][1].top
                elif self.selection_buttons[-1][1].bottom + scrollment < max2:
                    scrollment = max2 - self.selection_buttons[-1][1].bottom

                for button in self.selection_buttons:
                    button[1].top += scrollment

    def draw(self, screen : pygame.Surface):
        screen.blit(self.frame_image, self.frame_rect)
        screen.blit(self.scroll_background, self.scroll_background_rect)
        for button in self.selection_buttons:
            rect = button[1]
            if rect.bottom > self.scroll_background_rect.bottom + 60:
                break
            elif rect.top > self.scroll_background_rect.top - 60:
                screen.blit(button[0], rect)

        pygame.draw.rect(screen, (0,0,0), self.scroll_background_rect, width=3)

        self.cover_up_rect.bottom = self.scroll_background_rect.top
        pygame.draw.rect(screen, (220,220,220), self.cover_up_rect)
        self.cover_up_rect.top = self.scroll_background_rect.bottom
        pygame.draw.rect(screen, (220,220,220), self.cover_up_rect)

        screen.blit(self.text, self.text_rect)
        screen.blit(self.cancel_button, self.cancel_button_rect)