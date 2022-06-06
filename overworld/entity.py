from typing import List, Tuple
import pygame

class Player(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['player']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos
            

class Entity(pygame.sprite.Sprite):
    
    def __init__(self,assets,pos:List):
            pygame.sprite.Sprite.__init__(self)
            self.done_map = pos
            self.assets = assets
            self.playergroup = pygame.sprite.Group()
            self.uni_size = (40,40)
            for x in range(len(self.done_map)):
                for y in range(len(self.done_map[x])):
                    if (self.done_map[x][y])[0] == 'player':
                        self.player = Player(self.assets, self.uni_size, ((self.done_map[x][y])[1]))
                        self.playergroup.add(self.player)


    def group(self):
        return self.playergroup

    def move(self, event, groups:List):

        temp = pygame.sprite.Group()

        if event.key == pygame.K_LEFT:
                
            temp.add(Player(self.assets, self.uni_size, (self.player.rect.x-40, self.player.rect.y)))
              
        if event.key == pygame.K_RIGHT:
            
            temp.add(Player(self.assets, self.uni_size, (self.player.rect.x+40, self.player.rect.y)))

        if event.key == pygame.K_UP:
    
            temp.add(Player(self.assets, self.uni_size, (self.player.rect.x, self.player.rect.y-40)))
            
        if event.key == pygame.K_DOWN:
            
            temp.add(Player(self.assets, self.uni_size, (self.player.rect.x, self.player.rect.y+40)))


        if not(pygame.sprite.groupcollide(temp, groups, False,False)):

            if event.key == pygame.K_LEFT:
                self.player.rect.x -= 40
                
            if event.key == pygame.K_RIGHT:
                self.player.rect.x += 40

            if event.key == pygame.K_UP:
                self.player.rect.y -= 40
                    
            if event.key == pygame.K_DOWN:
                self.player.rect.y += 40


    def draw(self, screen : pygame.Surface):
        self.playergroup.draw(screen)
        
