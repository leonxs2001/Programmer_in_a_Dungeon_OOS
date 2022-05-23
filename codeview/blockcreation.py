from OOS.codeview.ifblock import IfBlock
from OOS.codeview.ifelseblock import IfElseBlock
from OOS.codeview.methodblock import MethodBlock
from codeview.operationblock import OperationBlock
#Blockdict with every possible block
#Notation {(name, type): Block}
block_dict = {
    ("+", "operation"): OperationBlock("+"),
    ("-", "operation"): OperationBlock("-"),
    ("*", "operation"): OperationBlock("*"),
    ("/", "operation"): OperationBlock("/"),
    ("%", "operation"): OperationBlock("%"),
    ("^", "operation"): OperationBlock("^"),
    ("and", "operation"): OperationBlock("and"),
    ("or", "operation"): OperationBlock("or"),
    ("not", "operation"): OperationBlock("not"),
    ("=", "operation"): OperationBlock("="),
    ("!=", "operation"): OperationBlock("!="),
    ("<", "operation"): OperationBlock("<"),
    (">", "operation"): OperationBlock(">"),
    ("<=", "operation"): OperationBlock("<="),
    (">=", "operation"): OperationBlock(">="),
    ("", "if"): IfBlock(),
    ("", "ifelse"): IfElseBlock(),
    ("goto", "method"): MethodBlock("goTo","goto", parameters=("x", "y")),
    ("goto", "method"): MethodBlock("goTo","goto", parameters=("position", )),
    ("move", "method"): MethodBlock("move","move", parameters=("x", "y")),
    ("getRandom", "method"): MethodBlock("getRandom","getRandom", parameters=("min", "max")),
    ("getX", "method"): MethodBlock("getOwnX","getX", parameters=()),
    ("getY", "method"): MethodBlock("getOwnY","getY", parameters=()),
    ("getPos", "method"): MethodBlock("getOwnPosition","getPos", parameters=()),
    ("getOpX", "method"): MethodBlock("getOpponentX","getOpX", parameters=()),
    ("getOpY", "method"): MethodBlock("getOpponentY","getOpY", parameters=()),
    ("getOpPos", "method"): MethodBlock("getOpponentPosition","getOpPos", parameters=()),
    ("getOpMovementX", "method"): MethodBlock("getOpponentMovementX","getOpMovementX", parameters=()),
    ("getOpMovementY", "method"): MethodBlock("getOpponentMovementY","getOpMovementY", parameters=()),
    ("getOpDistance", "method"): MethodBlock("getOpponentDistance","getOpDistance", parameters=()),
    ("getDistance", "method"): MethodBlock("getDistanceTo","getDistance", parameters=("X", "Y")),
    ("getDistance", "method"): MethodBlock("getDistanceTo","getDistance", parameters=("position",)),

}
methods = 
        elif name == "getTimeToNextAttack":#in milliseconds
            print(self.id)
            if self.id == "shooting":
                result = self.shoot_delay - self.elapsed_time
            elif self.id == "touching":
                result = self.hit_delay - self.elapsed_time

            if result <= 0: 
                return 0 
            else: 
                return result
        elif name == "getOpTimeToNextAttack":#in milliseconds
            if self.opponent_player.id == "shooting":
                result = self.opponent_player.shoot_delay - self.opponent_player.elapsed_time
            elif self.opponent_player.id == "touching":
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