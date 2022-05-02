import pygame
from pygame.locals import *
import fight.opponent as opponent
import fight.player as player
import fight.menu as menu
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
        """
        opponentcode = """
        ?(.getOpLifes() < 70){
            .move(.getOpMovementX(),.getOpMovementY())
        }!{
            ?(.onBorder()){
                $y = $y * -1
            }
            .move(0,$y)
        }
        .shootTo(.getOpPos())
        """
        self.player = player.Player("$var=-1",playercode)
        self.opponent = opponent.Opponent("$y=-10",opponentcode)
        self.player.opponent = self.opponent
        self.opponent.opponent = self.player
        self.bg = pygame.image.load("fight/image/bg.png")
        self.bg = pygame.transform.scale(self.bg, (1200, 675))
        self.menu = menu.Menu()
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
    
    