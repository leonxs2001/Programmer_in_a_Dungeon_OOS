from random import random
import pygame
from pygame.locals import *
import fight.opponent as opponent
from fight.bullet import Bullet
import fight.interpreter.interpreter as interpreter
import fight.lifecontroller as lifecontroller

class Player(pygame.sprite.Sprite):

    def __init__(self,initial_sequence_string : str, sequence_string : str):
        super().__init__()

        self.image = pygame.image.load("fight/image/player.png")
        self.size = (70,70)
        self.image = pygame.transform.scale(self.image,self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 337)

        self.speed = 5
        self.shoot_delay = 2000 #min delay between the single shoots in ms

        self.position = pygame.Vector2(self.rect.topleft)
        self.destination = pygame.Vector2(self.rect.topleft)
        self.movement = pygame.Vector2((0,0))

        self.life_controller = lifecontroller.LifeController(100,self.size[1])
        self.interpreter = interpreter.Interpreter(initial_sequence_string,sequence_string,self)
        self.bullet_group = pygame.sprite.Group()
        self.elapsed_time = self.shoot_delay + 1
    
    def setOpponent(self,opponent):
        self.opponent_player = opponent
    opponent = property(fset=setOpponent)
    def draw(self, screen : pygame.Surface):
        self.bullet_group.draw(screen)
        screen.blit(self.image, self.rect)
        self.life_controller.draw(screen, self.position)

    def update(self,elapsed_time):
        if self.elapsed_time <= self.shoot_delay:
            self.elapsed_time += elapsed_time

        self.interpreter.interpret()#interpret sequence
        
        self.bullet_group.update(elapsed_time)

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

        #check collision with opponent bullets
        for bullet in self.opponent_player.bullet_group:
            if self.rect.colliderect(bullet.rect):
                self.life_controller.lifes -= bullet.damage
                bullet.kill()
                
    def process_collision(self, elapsed_time):
        movement = self.movement * (elapsed_time/33.333)
        self.position -= movement

    def call_method(self, name : str, parameters : tuple):
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
            if self.position.x >= 1200 - self.size[0] or self.position.x <= 0 or \
                 self.position.y >= 675 - self.size[1] or self.position.y <= 0:
                return True
            else:  
                return False
        elif name == "onLeftBorder":
            return self.position.x <= 0
        elif name == "onRightBorder":
            return self.position.x >= 1200 - self.size[0]
        elif name == "onTopBorder":
            return self.position.y <= 0
        elif name == "onBottomBorder":
            return self.position.y >= 675 - self.size[1]
        elif name == "shoot":
            if len(parameters) == 0:#shoots in movementdirection
                self.shoot(self.movement)
            else:#shoots in given direction
                if len(parameters) == 2:
                    x, y = parameters
                else:#if parameter is a tupel
                    x, y = parameters[0]
                self.shoot(pygame.Vector2(x,y))

        elif name == "shootTo":
            if len(parameters) == 2:
                x, y = parameters
            else:#if parameter is a tupel
                x, y = parameters[0]
            direction =pygame.Vector2(x,y) - pygame.Vector2(self.rect.center)
            self.shoot(direction)
        elif name == "print":
            if len(parameters) > 0:
                print(parameters)
            else: 
                print("Test")

    def goto(self,x,y):
    
        if x < 0 :
            x = 0
        elif x > 1200 - self.size[0]:
            x = 1200 - self.size[0]

        if y < 0 :
            y = 0
        elif y > 675 - self.size[1]:
            y = 675 - self.size[1]    

        self.destination.update(x,y)
        self.movement = self.destination - self.position
        
        if self.movement.length() != 0: 
            
            if self.movement.length() < self.speed:
                self.movement.scale_to_length(self.speed)
                self.destination = self.position + self.movement
            else:
                self.movement.scale_to_length(self.speed)

    def shoot(self, direction : pygame.Vector2):
        if self.elapsed_time > self.shoot_delay:
            position_center = self.position + (pygame.Vector2(self.size)/2)
            self.bullet_group.add(Bullet(position_center ,direction))
            self.elapsed_time = 0
        
        



