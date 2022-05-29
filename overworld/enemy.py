from random import random, randrange
from typing import List, Tuple
import pygame

class Melee_E(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos, move_points, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = pos
            self.move_points = move_points
            self.move_reset = move_points
            self.assets = assets
            self.uni_size = (40,40)
        
        def update(self, groups:List, assets, *args: any, **kwargs: any) -> None:

            if self.move_points == 0:
               
                temp = pygame.sprite.Group()

                rnd = randrange(4)

                if rnd == 0:                    
                    temp.add(Melee_E(assets, self.uni_size, (self.rect.x-40, self.rect.y), 40, self.image))

                        
                if rnd == 1:              
                    temp.add(Melee_E(assets, self.uni_size, (self.rect.x+40, self.rect.y), 40, self.image))


                if rnd == 2:       
                    temp.add(Melee_E(assets, self.uni_size, (self.rect.x, self.rect.y-40), 40, self.image))
                    
                if rnd == 3:                
                    temp.add(Melee_E(assets, self.uni_size, (self.rect.x, self.rect.y+40), 40, self.image))
                
                if not(pygame.sprite.groupcollide(temp, groups, False,False)):

                    if rnd == 0:
                        self.rect.x -= 40
                        
                    if rnd == 1:
                        self.rect.x += 40

                    if rnd == 2:
                        self.rect.y -= 40
                            
                    if rnd == 3:
                        self.rect.y += 40

                self.move_points = self.move_reset
            else:
                self.move_points -= 1
                print(self.move_points)

            return super().update(*args, **kwargs)


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
                        self.monster = Melee_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]), 40, pygame.transform.scale(pygame.image.load(assets['melee_e']),self.uni_size))
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'big_melee_e':
                        self.monster = Melee_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]), 20, pygame.transform.scale(pygame.image.load(assets['big_melee_e']),self.uni_size))
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'shooting_e':
                        self.monster = Melee_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]), 40, pygame.transform.scale(pygame.image.load(assets['shooting_e']),self.uni_size))
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'big_shooting_e':
                        self.monster = Melee_E(self.assets, self.uni_size, ((self.done_map[x][y])[1]), 100, pygame.transform.scale(pygame.image.load(assets['big_shooting_e']),self.uni_size))
                        self.monstergroup.add(self.monster)
                   

    def update(self, groups:List):

        self.monstergroup.update(groups, self.assets)
      

    def draw(self, screen : pygame.Surface):
        self.monstergroup.draw(screen)
        
