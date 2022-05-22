from typing import List, Tuple
import pygame

class Monster(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['melee_e']),size)
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
                        self.monster = Monster(self.assets, self.uni_size, ((self.done_map[x][y])[1]))
                        self.monstergroup.add(self.monster)



    def move(self, event, groups:List):

        temp = pygame.sprite.Group()

        if event.key == pygame.K_LEFT:
                
            temp.add(Monster(self.assets, self.uni_size, (self.monster.rect.x-40, self.monster.rect.y)))

                
        if event.key == pygame.K_RIGHT:
            
            temp.add(Monster(self.assets, self.uni_size, (self.monster.rect.x+40, self.monster.rect.y)))


        if event.key == pygame.K_UP:
    
            temp.add(Monster(self.assets, self.uni_size, (self.monster.rect.x, self.monster.rect.y-40)))
            
        if event.key == pygame.K_DOWN:
            
            temp.add(Monster(self.assets, self.uni_size, (self.monster.rect.x, self.monster.rect.y+40)))


        if not(pygame.sprite.groupcollide(temp, groups, False,False)):

            if event.key == pygame.K_LEFT:
                self.monster.rect.x -= 40
                
            if event.key == pygame.K_RIGHT:
                self.monster.rect.x += 40

            if event.key == pygame.K_UP:
                self.monster.rect.y -= 40
                    
            if event.key == pygame.K_DOWN:
                self.monster.rect.y += 40


    def draw(self, screen : pygame.Surface):
        self.monstergroup.draw(screen)
        
