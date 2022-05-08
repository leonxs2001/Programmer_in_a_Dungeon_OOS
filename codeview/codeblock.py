from pydoc import visiblename
import pygame
INVISIBLE_COLOR = (255,0,0)
class CodeBlock(pygame.sprite.Sprite):
    
    def __init__(self, background_color = (130,130,130)):
        super().__init__()
        self.background_color = background_color
        self.size = pygame.Vector2(300,80)
        self.position = pygame.Vector2(10,10)
        self.in_focus = False
        self.position_in_image = pygame.Vector2(0,0)
        self.next_block = None
        self.build_image(self.size)

    def update_scale_factor(self, scalefactor):
        last_scale_factor = self.rect.size[0] / self.size.x

        self.build_image(self.size * scalefactor)

        center_of_scrollment = pygame.mouse.get_pos()
        distance = (self.position - center_of_scrollment) / last_scale_factor
        distance *= scalefactor
        self.position = center_of_scrollment + distance

        if self.next_block:
            self.next_block.update_scale_factor(scalefactor)
            self.adjust_blocks()

    def build_image(self, size):
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.image.fill(INVISIBLE_COLOR)
        self.image.set_colorkey(INVISIBLE_COLOR)#set the Color invisble

        self.border_size = 2
        #draw the normal rect with border
        self.visible_size = size - pygame.Vector2(0,0.15*size.y)

        #the collision box should only be on the visible part of the surface
        self.rect.size = self.visible_size.copy()
        rect = pygame.Rect((0,0),self.visible_size)

        pygame.draw.rect(self.image,self.background_color,rect)
        pygame.draw.rect(self.image,(0,0,0),rect,width=self.border_size)

        #draw the bottom circle width border
        factor = size.x/300
        self.circle_overlap = 10 * factor
        self.circle_radius = (size.y - self.visible_size.y) + self.circle_overlap
        self.circle_x = size.x / 2
        pygame.draw.circle(self.image,self.background_color,(self.circle_x ,self.visible_size.y - self.circle_overlap),self.circle_radius)
        pygame.draw.circle(self.image, (0,0,0), (self.circle_x ,self.visible_size.y - self.circle_overlap) ,self.circle_radius, width=self.border_size)

        #rect for covering the circlelines inside the rect
        rect.update((0,0),(self.circle_radius * 2, self.circle_radius+self.circle_overlap))
        rect.centerx = self.circle_x
        rect.bottom = self.visible_size.y - self.border_size
        pygame.draw.rect(self.image, self.background_color, rect)

    def append(self, code_block):
        """append the given block"""
        if self.next_block: 
            self.next_block.append(code_block)
        else: # found the right place to append
            self.next_block = code_block
            self.adjust_blocks() 
          
    def get_last_invisible_rect(self):  
        """returns the invisible rect of the last element(bottom)"""
        if self.next_block:
            return self.next_block.get_last_invisible_rect()
        else:
            invisible_size = (self.visible_size.x, (self.visible_size.y/0.85)*0.15)
            invisible_position = self.position + (0,self.visible_size.y)
            invisible_rect = pygame.rect.Rect(invisible_position, invisible_size)
            return invisible_rect

    def try_to_connect(self, block):
        """checks if the two blocks can connect, connect if possible 
        and return the one that is beneath the other"""
        own_invisible_rect = self.get_last_invisible_rect()
        other_invisible_rect = block.get_last_invisible_rect()
        print(own_invisible_rect.size, self.rect.size,self.size)
        if own_invisible_rect.colliderect(block.rect):
            self.append(block)
            return block
        elif other_invisible_rect.colliderect(self.rect):
            block.append(self)
            return self


    def adjust_blocks(self):
        """adjust the next block to the right position"""
        if self.next_block:
            self.next_block.position = self.position + (0,self.visible_size.y - 1)
            self.next_block.adjust_blocks()

    def mouse_button_up(self):
        self.in_focus = False
        if self.next_block:
            self.next_block.mouse_button_up()

    def get_collider(self, mouse_position):
        """check own and child block collision with given position"""
        if self.rect.collidepoint(mouse_position):
            self.in_focus = True
            return self
        else: 
            if self.next_block:
                collider = self.next_block.get_collider(mouse_position)
                if collider == self.next_block:
                    self.next_block = None
                return collider
    def move(self, movement : pygame.Vector2):
        self.position += movement
        if self.next_block:
            self.next_block.move(movement)

    def update(self):
        self.rect.topleft = self.position
        if self.next_block:
            self.next_block.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.next_block:
            self.next_block.draw(screen)