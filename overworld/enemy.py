from random import randrange
from typing import List, Tuple
import pygame

tup = None

class Robot(pygame.sprite.Sprite):
        def __init__(self, assets, pos, move_points, image, type, difficulty):
            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = pos
            self.move_points = move_points
            self.move_reset = move_points
            self.assets = assets
            self.uni_size = (40,40)
            self.type = type
            self.difficulty = difficulty
        
        def update(self, groups:List, hero:List, monstergroup:List, assets, *args: any, **kwargs: any) -> None:

            if self.move_points == 0:
               
                temp = pygame.sprite.Group()

                rnd = randrange(4)

                if rnd == 0:                    
                    temp.add(Robot(assets, (self.rect.x-40, self.rect.y), 40, self.image, self.type, self.difficulty))

                        
                if rnd == 1:              
                    temp.add(Robot(assets, (self.rect.x+40, self.rect.y), 40, self.image, self.type, self.difficulty))


                if rnd == 2:       
                    temp.add(Robot(assets, (self.rect.x, self.rect.y-40), 40, self.image, self.type, self.difficulty))
                    
                if rnd == 3:                
                    temp.add(Robot(assets, (self.rect.x, self.rect.y+40), 40, self.image, self.type, self.difficulty))
                
                if pygame.sprite.groupcollide(temp, hero, False, False):
                    tup = (self.type, self.difficulty)
                    return tup

                if not(pygame.sprite.groupcollide(temp, groups, False,False)) and not(pygame.sprite.groupcollide(temp, monstergroup, False,False)):

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
                        self.monster = Robot(self.assets,  ((self.done_map[x][y])[1]), 5, pygame.transform.scale(pygame.image.load(assets['melee_e']),self.uni_size), "m", 1)
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'big_melee_e':
                        self.monster = Robot(self.assets,  ((self.done_map[x][y])[1]), 7, pygame.transform.scale(pygame.image.load(assets['big_melee_e']),self.uni_size), "m", 2)
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'shooting_e':
                        self.monster = Robot(self.assets,  ((self.done_map[x][y])[1]), 10, pygame.transform.scale(pygame.image.load(assets['shooting_e']),self.uni_size), "s", 1)
                        self.monstergroup.add(self.monster)
                    if (self.done_map[x][y])[0] == 'big_shooting_e':
                        self.monster = Robot(self.assets,  ((self.done_map[x][y])[1]), 15, pygame.transform.scale(pygame.image.load(assets['big_shooting_e']),self.uni_size), "s", 2)
                        self.monstergroup.add(self.monster)
                   

    def update(self, groups:List, hero:List):

        for monster in self.monstergroup:
            tup = monster.update(groups, hero, self.monstergroup, self.assets)
            
            if tup != None:
                monster.kill()
                return tup


    def draw(self, screen : pygame.Surface):
        self.monstergroup.draw(screen)
        
