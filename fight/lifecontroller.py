import pygame

class LifeController:
    def __init__(self,max_lifes, width):
        self.size = (width,width/6)
        self.image = pygame.Surface(self.size)
        self.live_bar_size = (self.size[0]-4, self.size[1]-4)
        self.white_bar = pygame.Surface(self.live_bar_size)
        self.white_bar.fill((255,255,255))

        self.max_lifes = max_lifes
        self.lifes = max_lifes

    def __setattr__(self, name: str, value):
        super().__setattr__(name,value)
        if name == "lifes":
            self.reset_lifes()
    def getLifePercentage(self):
        return (self.lifes / self.max_lifes) * 100
    def reset_lifes(self):
        if self.lifes < 0:
            self.lifes = 0
        elif self.lifes > self.max_lifes:
            self.lifes = self.max_lifes
        relative_lifes = self.lifes / self.max_lifes
        live_bar_size = list(self.live_bar_size)
        live_bar_size[0] *= relative_lifes
        
        live_bar = pygame.Surface(live_bar_size)
        if relative_lifes > 0.5:
            live_bar.fill((0,255,0))
        elif relative_lifes > 0.3:
            live_bar.fill((255,255,0))
        else:
            live_bar.fill((255,0,0))
        
        self.image.blit(self.white_bar, (2,2))
        self.image.blit(live_bar, (2,2))
        

    def draw(self,screen,position):
        pos = position-pygame.Vector2(0,self.size[1])
        screen.blit(self.image, pos)
