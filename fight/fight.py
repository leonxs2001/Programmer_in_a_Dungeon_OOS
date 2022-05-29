import pygame
from pygame.locals import *
from fight.player.shootingplayer import ShootingPlayer
from fight.player.touchingplayer import TouchingPlayer
from fight.menu import Menu
from level import Level

class Fight(Level):
    def __init__(self):
        #Entities
        playercode = """
        
        ?(.onBorder()){
            $var = $var * -1
        }
        ?(.getLifes() < 50){
            .move(0,$var)
        }!{
            .move($var,0)
        }
        .shoot()
        """
        opponentcode = """
        ?(.getOpTimeToNextAttack() < 500){
            .move(0,.getOpMovementX())
        }!{
            .goto(.getOpPos())
        }
        """
        self.player = ShootingPlayer("$var=-1",playercode, False)
        self.opponent = TouchingPlayer("$y=10",opponentcode, True)
        self.player.opponent = self.opponent
        self.opponent.opponent = self.player
        self.bg = pygame.image.load("fight/image/bg.png")
        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.menu = Menu()
        self.last_time = pygame.time.get_ticks()
        
    def update(self):
        #calculate elapsed time
        new_time = pygame.time.get_ticks()
        elapsed_time = new_time - self.last_time
        self.last_time = new_time

        self.menu.update()
        if not self.menu.wait:
            self.player.update(elapsed_time)
            self.opponent.update(elapsed_time)
            #check collsion between the two players
            if self.player.rect.colliderect(self.opponent.rect):
                self.player.process_collision(elapsed_time)
                self.opponent.process_collision(elapsed_time)

        

    def give_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == K_SPACE:
                if self.player.ready:
                    self.player.next_step()
            elif event.key == K_RETURN:
                self.menu.wait = not self.menu.wait
        elif event.type == MOUSEBUTTONDOWN:
            if self.menu.is_mouse_on_play():
                self.menu.wait = not self.menu.wait

    def draw(self,screen):
        #Redisplay
        screen.blit(self.bg, (0,0))
        self.player.draw(screen)
        self.opponent.draw(screen)
        self.menu.draw(screen)
    
    