import pygame
class Selector:
    arrow_size = pygame.Vector2(20,40)
    background_color = (200,200,200)
    def __init__(self):
        self.open = False
        self.build()

    def build(self):
        #create the little arrow image
        self.arrow_image = pygame.Surface(Selector.arrow_size)
        self.arrow_image.fill(Selector.background_color)
        pygame.draw.rect(self.arrow_image, (0,0,0), pygame.rect.Rect((0,0), Selector.arrow_size),width=2)
        center_y = Selector.arrow_size.y / 2
        pygame.draw.lines(self.arrow_image, (0,0,0), False, [(0,0), (Selector.arrow_size.x, center_y), (0, Selector.arrow_size.y)], width=2)
        self.arrow_image_rect = self.arrow_image.get_rect()
        self.arrow_image_rect.centery = 360

        self.drawn_arrow_image = self.arrow_image.copy()

        #create backgroundsuface
        self.background_image = pygame.Surface((400, 720))
        self.background_image.fill(Selector.background_color)
        pygame.draw.rect(self.background_image, (0,0,0), pygame.rect.Rect((0,0), (400, 720)),width=2)

    def check_collision(self, mouse_position : pygame.Vector2):
        if self.arrow_image_rect.collidepoint(mouse_position):
            self.open = not self.open
            if self.open:
                self.arrow_image_rect.left = 400
                self.drawn_arrow_image = pygame.transform.rotate(self.arrow_image, 180)
            else:
               self.arrow_image_rect.left = 0
               self.drawn_arrow_image = self.arrow_image.copy()
            return True
        else:
            if self.open and mouse_position.x < 400:
                return True
            return False 

    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.drawn_arrow_image, self.arrow_image_rect)
        if self.open:#only draw background if its open
            screen.blit(self.background_image, (0,0))