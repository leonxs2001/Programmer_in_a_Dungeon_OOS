import pygame
from pylint import modify_sys_path
class VariableInput:
    def __init__(self, heading):
        self.aktiv = False
        self.value = ""
        self.size = pygame.Vector2(400,220)

        self.heading = heading
        self.build()
        
    def build(self):
        #draw the frame and the text in it
        self.frame_image = pygame.Surface(self.size)
        self.frame_image.fill((220,220,220))
        self.frame_rect = self.frame_image.get_rect()
        pygame.draw.rect(self.frame_image, (0,0,0), self.frame_rect, width=4)
        self.frame_rect.center = (640, 250)

        font = pygame.font.Font(None, 45)
        text = font.render(self.heading, True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (200, 40)
        self.frame_image.blit(text, text_rect)

        #draw inputfield
        self.input_size = pygame.Vector2(300, 40)
        self.input_field = pygame.Surface(self.input_size)
        self.input_field.fill((255,255,255))
        self.input_field_rect = self.input_field.get_rect()
        pygame.draw.rect(self.input_field, (0,0,0), self.input_field_rect, width=2)
        self.input_field_rect.center = (640, 230)

        #create the text:
        self.text_font = pygame.font.Font(None, 30)
        self.text = self.text_font.render(self.value, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.centery = self.input_field_rect.centery
        self.text_rect.left = self.input_field_rect.left + 10

        #create the cursor 
        self.cursor_counter = 0
        self.cursor_rect = pygame.rect.Rect((0,0), (3, self.text_rect.height))
        self.cursor_rect.left = self.text_rect.right + 3
        self.cursor_rect.top = self.text_rect.top

        self.button_size = pygame.Vector2(140, 60)
        #draw confirm Button
        self.confirm_button = pygame.Surface(self.button_size)
        self.confirm_button.fill((200,200,200))
        self.confirm_button_rect = self.confirm_button.get_rect()
        pygame.draw.rect(self.confirm_button, (0,0,0), self.confirm_button_rect, width=2)
        self.confirm_button_rect.centery = 300
        self.confirm_button_rect.left = self.input_field_rect.left

        font = pygame.font.Font(None, 40)
        text = font.render("Confirm!", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (70, 30)
        self.confirm_button.blit(text, text_rect)

        #draw cancel button
        self.cancel_button_size = pygame.Vector2(250, 60)
        self.cancel_button = pygame.Surface(self.button_size)
        self.cancel_button.fill((200,200,200))
        self.cancel_button_rect = self.cancel_button.get_rect()
        pygame.draw.rect(self.cancel_button, (0,0,0), self.cancel_button_rect, width=2)
        self.cancel_button_rect.centery = 300
        self.cancel_button_rect.right = self.input_field_rect.right

        text = font.render("Cancel!", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (70, 30)
        self.cancel_button.blit(text, text_rect)

    def give_keyboard_down_event(self, event):
        if self.aktiv:
            if event.key == pygame.K_BACKSPACE:#delete last letter
                self.value = self.value[:-1]
            else:
                if len(self.value) < 20:
                    char = event.unicode
                    self.value += char
            #recreate the text and reset the cursorposition
            self.text = self.text_font.render(self.value, True, (0,0,0))
            self.text_rect.size = self.text.get_size()
            self.cursor_rect.left = self.text_rect.right + 3
            
    def check_collision(self, mouse_position : pygame.Vector2):
        #check collision with the input field
        if self.input_field_rect.collidepoint(mouse_position):
            self.aktiv = True
        else:
            self.aktiv = False
        #check collision with the Button
        if self.confirm_button_rect.collidepoint(mouse_position):
            if self.value != "" and self.value[0].isalpha:
                self.aktiv = False
                value = self.value
                self.value = ""
                self.build()
                return value
        elif self.cancel_button_rect.collidepoint(mouse_position):#return true if ready
            self.value = ""
            self.build()
            return True
        else:
            self.value = ""

    def draw(self, screen : pygame.Surface):
        screen.blit(self.frame_image, self.frame_rect)
        screen.blit(self.input_field, self.input_field_rect)
        screen.blit(self.text, self.text_rect)
        if self.aktiv:
            self.cursor_counter += 1
            if self.cursor_counter % 40 < 25:
                pygame.draw.rect(screen, (0,0,0),self.cursor_rect)
        screen.blit(self.confirm_button, self.confirm_button_rect)
        screen.blit(self.cancel_button, self.cancel_button_rect)