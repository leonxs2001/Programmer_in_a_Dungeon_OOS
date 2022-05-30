from random import random
import pygame
from pygame.locals import *
from fight.interpreter.interpreter import Interpreter
from fight.player.lifecontroller import LifeController
from overworld.config import asset

class Player:
    """Player is a template for special players."""
    def __init__(self,initial_sequence_string : str, sequence_string : str, is_opponent : bool):
        super().__init__()
        self.image = self.load_image(is_opponent)
        self.size = (70,70)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 360)

        self.speed = 5

        self.position = pygame.Vector2(self.rect.topleft)
        self.destination = pygame.Vector2(self.rect.topleft)
        self.movement = pygame.Vector2((0,0))

        self.life_controller = LifeController(100,self.size[1])
        self.interpreter = Interpreter(initial_sequence_string,sequence_string,self)

        if is_opponent:
            self.rect.center = (1180, 360)
            self.position = pygame.Vector2(self.rect.topleft)
    def load_image(self, is_opponent):
        return pygame.image.load(asset["player"])
        
    def setOpponent(self,opponent):
        self.opponent_player = opponent 
    opponent = property(fset=setOpponent)

    def draw(self, screen : pygame.Surface):
        screen.blit(self.image, self.rect)
        self.life_controller.draw(screen, self.position)

    def update(self,elapsed_time):
        self.interpreter.interpret()#interpret sequence

        #move towards destination
        if(self.position != self.destination):
            if abs((self.destination - self.position).length()) < self.speed:
                self.position = self.destination.copy()
                self.movement = pygame.Vector2(0,0)
            else:
                movement = self.movement * (elapsed_time/33.333)
                self.position += movement
                
        #update center to position
        self.rect.topleft = (self.position.x, self.position.y)

        from fight.player.shootingplayer import ShootingPlayer
        #check collision with opponent bullets
        if isinstance(self.opponent_player, ShootingPlayer):
            for bullet in self.opponent_player.bullet_group:
                if self.rect.colliderect(bullet.rect):
                    self.life_controller.lifes -= bullet.damage
                    bullet.kill()
            if isinstance(self, ShootingPlayer):
                pass#hier collision von den Bullets der beiden Shootingplayers !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #check if player is outside the field
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.update(self.rect.topleft)
        elif self.rect.bottom > 720:
            self.rect.bottom = 720
            self.position.update(self.rect.topleft)

        if self.rect.left < 0:
            self.rect.left = 0
            self.position.update(self.rect.topleft)
        elif self.rect.right > 1280:
            self.rect.right = 1280
            self.position.update(self.rect.topleft)
                
    def process_collision(self, elapsed_time):
        movement = self.movement * (elapsed_time/33.333)
        self.position -= movement

    def call_method(self, name : str, parameters : tuple):
        from fight.player.shootingplayer import ShootingPlayer
        from fight.player.touchingplayer import TouchingPlayer
        if name == "goto":
            if len(parameters) == 2:
                x, y = parameters
            else:#if parameter is a tupel
                x, y = parameters[0]
            self.goto(x,y)
        elif name == "move":
            if len(parameters) == 2:
                x, y = parameters
            else:#if parameter is a tupel
                x, y = parameters[0]
            self.goto(self.position.x + x, self.position.y + y)
        elif name == "getRandom":
            if len(parameters) == 2:
                min, max = parameters
            else:#if parameter is a tupel
                min, max = parameters[0]
            return random.randint(min, max)
        elif name == "getX":
            return self.rect.left
        elif name == "getY":
            return self.rect.top
        elif name == "getOpPos":
            return self.opponent_player.rect.center
        elif name == "getOpX":
            return self.opponent_player.rect.centerx
        elif name == "getOpY":
            return self.opponent_player.rect.centery
        elif name == "getOpMovementX":
            return self.opponent_player.movement.x
        elif name == "getOpMovementY":
            return self.opponent_player.movement.y
        elif name == "getOpDistance":
            return (self.position - self.opponent_player.position).length()
        elif name == "getDistance":#to the given point
            if len(parameters) == 2:
                x, y = parameters
            else:#if parameter is a tupel
                x, y = parameters[0]
            pos = pygame.Vector2(x,y)
            return (pos - self.position).length()
        elif name == "getTimeToNextAttack":#in milliseconds
            if isinstance(self, ShootingPlayer):
                result = self.shoot_delay - self.elapsed_time
            elif isinstance(self, TouchingPlayer):
                result = self.hit_delay - self.elapsed_time

            if result <= 0: 
                return 0 
            else: 
                return result
        elif name == "getOpTimeToNextAttack":#in milliseconds
            if isinstance(self.opponent_player, ShootingPlayer):
                result = self.opponent_player.shoot_delay - self.opponent_player.elapsed_time
            elif isinstance(self.opponent_player, TouchingPlayer):
                result = self.opponent_player.hit_delay - self.opponent_player.elapsed_time

            if result <= 0: 
                return 0 
            else: 
                return result
        elif name == "getLifes":#get lives in percent
            return self.life_controller.getLifePercentage()
        elif name == "getOpLifes":#get opponent lives in percent
            return self.opponent_player.life_controller.getLifePercentage() 
        elif name == "destinationReached":#is destination reached
            return self.position == self.destination
        elif name == "onPos":#checks if is on Position
            if len(parameters) == 2:
                x, y = parameters
            else:#if parameter is a tupel
                x, y = parameters[0]
            return (x, y) == self.rect.topleft
        elif name == "onX":
            return parameters[0] == self.rect.left
        elif name == "onY":
            return parameters[0] == self.rect.top
        elif name == "onBorder":
            if self.position.x >= 1280 - self.size[0] or self.position.x <= 0 or \
                 self.position.y >= 720 - self.size[1] or self.position.y <= 0:
                return True
            else:  
                return False
        elif name == "onLeftBorder":
            return self.position.x <= 0
        elif name == "onRightBorder":
            return self.position.x >= 1280 - self.size[0]
        elif name == "onTopBorder":
            return self.position.y <= 0
        elif name == "onBottomBorder":
            return self.position.y >= 720 - self.size[1]
        elif name == "print":
            if len(parameters) > 0:
                print(parameters)
            else: 
                print("Test")

    def goto(self,x,y):

        self.destination.update(x,y)
        self.movement = self.destination - self.position
        
        if self.movement.length() != 0: 
            
            if self.movement.length() < self.speed:
                self.movement.scale_to_length(self.speed)
                self.destination = self.position + self.movement
            else:
                self.movement.scale_to_length(self.speed)

            if self.destination.x < 0 :
                self.destination.x = 0
            elif self.destination.x > 1280 - self.size[0]:
                self.destination.x = 1280 - self.size[0]

            if self.destination.y < 0 :
                self.destination.y = 0
            elif self.destination.y > 720 - self.size[1]:
                self.destination.y = 720 - self.size[1]    
        
        



