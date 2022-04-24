import pygame
from pygame.locals import *
import fight.interpreter.interpreter as interpreter

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load("fight/image/player.png")
        self.image1 = pygame.transform.scale(self.image1,(75,75))
        self.rect = self.image1.get_rect()
        self.rect.topleft = (0,0)
        self.ready = True
        self.destination = self.rect.topleft
        self.speed = 20
        self.case_position = (0,0)
        self.case_speed = 2 #cases per move
        self.cases_to_move = (0,0)
        code = """
        .move($x_direction,0)
        ?(.onX(0) | .onX(15)){
            $x_direction = $x_direction * -1
            .move(0, $y_direction)
            ?(.onY(0) | .onY(8)){
                $y_direction = $y_direction * -1
            }
        }
        """
        self.interpreter = interpreter.Interpreter("$y_direction=1 $x_direction=2",code,self)

    def draw(self, screen):
        screen.blit(self.image1, self.rect)

    def update(self):
        x_distance = self.destination[0] - self.rect.left
        y_distance = self.destination[1] - self.rect.top
        if abs(x_distance) < self.speed and x_distance != 0: # near enought
            self.rect.left = self.destination[0]
        elif x_distance < 0: # go to the left
            self.rect.left -= self.speed
        elif x_distance > 0:
            self.rect.left += self.speed
        elif abs(y_distance) < self.speed and y_distance != 0: # near enought
            self.rect.top = self.destination[1]
        elif y_distance < 0: # go up
            self.rect.top -= self.speed
        elif y_distance > 0:
            self.rect.top += self.speed
        else:
            self.ready = True

    def next_step(self):
        self.ready = False
        self.interpreter.interpret()

    def goto(self,x_case, y_case):#overwrite every movement

        #can only move in given window(16x9 cases)
        if x_case < 0:
            x_case = 0
        elif x_case > 15:
            x_case = 15
        if y_case < 0:
            y_case = 0
        elif y_case > 8:
            y_case = 8

        self.cases_to_move = (x_case - self.case_position[0], y_case - self.case_position[1])

        if self.cases_to_move != (0,0): #set movement for the cases
            
            #only move case_speed cases per move
            case_distance = list(self.cases_to_move)
            while abs(case_distance[0]) + abs(case_distance[1]) > self.case_speed:
                if abs(case_distance[0]) > abs(case_distance[1]):
                    if case_distance[0] < 0:
                        case_distance[0] += 1
                    else:
                        case_distance[0] -= 1
                else:
                    if case_distance[1] < 0:
                        case_distance[1] += 1
                    else:
                        case_distance[1] -= 1

            self.cases_to_move = (self.cases_to_move[0] - case_distance[0], self.cases_to_move[1] - case_distance[1])#set new cases_to_move
            x_case = case_distance[0] + self.case_position[0] 
            y_case = case_distance[1] + self.case_position[1]

            self.case_position = (x_case, y_case)
            
            x = x_case * 75
            y = y_case * 75
            self.destination = (x, y)

    def move(self,x_case, y_case):
        self.goto(self.case_position[0] + x_case, self.case_position[1] + y_case)
            
    def call_method(self, name, parameters):
        if name == "goto":
            if len(parameters) == 2:
                x_c, y_c = parameters
            else:#if parameter is a tupel
                x_c, y_c = parameters[0]
            
            self.goto(x_c, y_c)
            
        elif name == "move":
            if len(parameters) == 2:
                x_c, y_c = parameters
            else:#if parameter is a tupel
                x_c, y_c = parameters[0]
            self.move(x_c, y_c)
        elif name == "getX":
            return self.case_position[0]
        elif name == "getY":
            return self.case_position[1]
        elif name == "destRea":#is destination reached
            if self.cases_to_move == (0,0):
                return True
            else: 
                return False
        elif name == "onPos":#checks if is on Position
            if len(parameters) == 2:
                x_c, y_c = parameters
            else:#if parameter is a tupel
                x_c, y_c = parameters[0]
            return (x_c, y_c) == self.case_position
        elif name == "onX":
            return parameters[0] == self.case_position[0]
        elif name == "onY":
            return parameters[0] == self.case_position[1]
        elif name == "print":
            if len(parameters) > 0:
                print(parameters)
            else: 
                print("Test")



