import pygame
BACKGROUND_COLOR = (130,130,130)
INVISIBLE_COLOR = (255,0,0)
class codeBlock:
    
    def __init__(self):
        self.size = pygame.Vector2(250,90)
        self.position = pygame.Vector2(10,10)
        self.__build_image()

    def __build_image(self):
        self.image = pygame.Surface(self.size)
        self.image.fill((255,255,255))
        self.image.set_colorkey(INVISIBLE_COLOR)#set the Color invisble

        border_size = 2
        #draw the normal rect with border
        visible_size = self.size - pygame.Vector2(0,0.3*self.size.y)
        rect = pygame.Rect((0,0),visible_size)
        pygame.draw.rect(self.image,BACKGROUND_COLOR,rect)
        pygame.draw.rect(self.image,(0,0,0),rect,width=border_size)

        #draw the bottom circle width border
        factor = self.size.x/250
        circle_overlap = 10 * factor
        circle_radius = 20 * factor
        circle_x = self.size.x / 2
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

    def draw(self, screen):
        screen.blit(self.image, self.position)