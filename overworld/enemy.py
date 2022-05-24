from random import random, randrange
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
                   



    def update(self, groups:List):


        for treasure in self.monstergroup:
            
            temp = pygame.sprite.Group()

            rnd = randrange(4)

            if rnd == 0:
                    
                temp.add(Melee_E(self.assets, self.uni_size, (treasure.rect.x-40, treasure.rect.y)))

                    
            if rnd == 1:
                
                temp.add(Melee_E(self.assets, self.uni_size, (treasure.rect.x+40, treasure.rect.y)))


            if rnd == 2:
        
                temp.add(Melee_E(self.assets, self.uni_size, (treasure.rect.x, treasure.rect.y-40)))
                
            if rnd == 3:
                
                temp.add(Melee_E(self.assets, self.uni_size, (treasure.rect.x, treasure.rect.y+40)))
            
            if not(pygame.sprite.groupcollide(temp, groups, False,False)):

                if rnd == 0:
                    treasure.rect.x -= 40
                    
                if rnd == 1:
                    treasure.rect.x += 40

                if rnd == 2:
                    treasure.rect.y -= 40
                        
                if rnd == 3:
                    treasure.rect.y += 40




      


    def draw(self, screen : pygame.Surface):
        self.monstergroup.draw(screen)
        
