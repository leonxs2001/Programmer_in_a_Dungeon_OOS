from typing import List, Tuple
import pygame

class Melee_E(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['melee_e']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos

class Big_Melee_E(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['big_melee_e']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos


class Shooting_E(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['shooting_e']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos

class Big_Shooting_E(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['big_shooting_e']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos





class Mon(pygame.sprite.Sprite):
    
    def __init__(self,assets,pos:List):
            pygame.sprite.Sprite.__init__(self)
            self.done_map = pos
            self.assets = assets
            self.monstergroup = pygame.sprite.Group()
            self.uni_size = (40,40)
            for x in range(len(self.done_map)):
                for y in range(len(self.done_map[x])):
                    if (self.done_map[x][y])[0] == 'melee_e':
                        self.monster = Melee_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]))
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'big_melee_e':
                        self.monster = Big_Melee_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]))
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'shooting_e':
                        self.monster = Shooting_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]))
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'big_shooting_e':
                        self.monster = Big_Shooting_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]))
                        self.monstergroup.add(self.monster)
                   



    def move(self, event, groups:List):

        temp = pygame.sprite.Group()

      


    def draw(self, screen : pygame.Surface):
        self.monstergroup.draw(screen)
        
