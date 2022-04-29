import pygame

class LiveController:
    def __init__(self,max_lives, width):
        self.size = (width,width/6)
        self.image = pygame.Surface(self.size)
        self.live_bar_size = (self.size[0]-4, self.size[1]-4)
        self.white_bar = pygame.Surface(self.live_bar_size)
        self.white_bar.fill((255,255,255))

        self.max_lives = max_lives
        self.lives = max_lives

    def __setattr__(self, name: str, value):
        super().__setattr__(name,value)
        if name == "lives":
            self.reset_lives()

    def reset_lives(self):
        if self.lives < 0:
            self.lives = 0
        elif self.lives > self.max_lives:
            self.lives = self.max_lives
        relative_lives = self.lives / self.max_lives
        live_bar_size = list(self.live_bar_size)
        live_bar_size[0] *= relative_lives
        
        live_bar = pygame.Surface(live_bar_size)
        if relative_lives > 0.5:
            live_bar.fill((0,255,0))
        elif relative_lives > 0.3:
            live_bar.fill((255,255,0))
        else:
            live_bar.fill((255,0,0))
        
        self.image.blit(self.white_bar, (2,2))
        self.image.blit(live_bar, (2,2))
        

    def draw(self,screen,position):
        pos = position-pygame.Vector2(0,self.size[1])
        screen.blit(self.image, pos)
