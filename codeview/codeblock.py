import pygame
BACKGROUND_COLOR = (130,130,130)
INVISIBLE_COLOR = (255,0,0)
class CodeBlock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = pygame.Vector2(250,90)
        self.position = pygame.Vector2(10,10)
        self.in_focus = False
        self.position_in_image = pygame.Vector2(0,0)
        self.__build_image(self.size)

    def update_scale_factor(self, scalefactor):
        last_scale_factor = self.rect.size[0] / self.size.x

        self.__build_image(self.size * scalefactor)

        center_of_scrollment = pygame.mouse.get_pos()
        distance = (self.position - center_of_scrollment) / last_scale_factor
        distance *= scalefactor
        self.position = center_of_scrollment + distance
    def __build_image(self, size):
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.image.fill((255,255,255))
        self.image.set_colorkey(INVISIBLE_COLOR)#set the Color invisble

        border_size = 2
        #draw the normal rect with border
        visible_size = size - pygame.Vector2(0,0.3*size.y)
        rect = pygame.Rect((0,0),visible_size)
        pygame.draw.rect(self.image,BACKGROUND_COLOR,rect)
        pygame.draw.rect(self.image,(0,0,0),rect,width=border_size)

        #draw the bottom circle width border
        factor = size.x/250
        circle_overlap = 10 * factor
        circle_radius = 20 * factor
        circle_x = size.x / 2
        pygame.draw.circle(self.image,BACKGROUND_COLOR,(circle_x ,visible_size.y - circle_overlap),circle_radius)
        pygame.draw.circle(self.image, (0,0,0), (circle_x ,visible_size.y - circle_overlap) ,circle_radius, width=border_size)
        #rect for covering the circlelines inside the rect
        rect.update((0,0),(circle_radius * 2, circle_radius+circle_overlap))
        rect.centerx = circle_x
        rect.bottom = visible_size.y - border_size
        pygame.draw.rect(self.image, BACKGROUND_COLOR, rect)

        #draw the top circle with border
        pygame.draw.circle(self.image,INVISIBLE_COLOR,(circle_x ,-circle_overlap),circle_radius)
        pygame.draw.circle(self.image,(0,0,0),(circle_x ,-circle_overlap),circle_radius,width=border_size)

    def mouse_button_down(self):
        mouse_position = pygame.mouse.get_pos()
        #check collision with mouse
        if self.rect.collidepoint(mouse_position):
            self.in_focus = True
            self.position_in_image = mouse_position - self.position

    def mouse_button_up(self):
        self.in_focus = False

    def update(self):
        if self.in_focus:
            self.position = pygame.mouse.get_pos() - self.position_in_image

        self.rect.topleft = self.position