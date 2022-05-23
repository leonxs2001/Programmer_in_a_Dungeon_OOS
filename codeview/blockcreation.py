from codeview.valueblock import ValueBlock
from codeview.ifblock import IfBlock
from codeview.ifelseblock import IfElseBlock
from codeview.methodblock import MethodBlock
from codeview.operationblock import OperationBlock
import pygame
pygame.font.init()
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
    ("getRandom", "value"): ValueBlock("getRandom","getRandom", parameters=("min", "max")),
    ("getX", "value"): ValueBlock("getOwnX","getX", parameters=()),
    ("getY", "value"): ValueBlock("getOwnY","getY", parameters=()),
    ("getPos", "value"): ValueBlock("getOwnPosition","getPos", parameters=()),
    ("getOpX", "value"): ValueBlock("getOpponentX","getOpX", parameters=()),
    ("getOpY", "value"): ValueBlock("getOpponentY","getOpY", parameters=()),
    ("getOpPos", "value"): ValueBlock("getOpponentPosition","getOpPos", parameters=()),
    ("getOpMovementX", "value"): ValueBlock("getOpponentMovementX","getOpMovementX", parameters=()),
    ("getOpMovementY", "value"): ValueBlock("getOpponentMovementY","getOpMovementY", parameters=()),
    ("getOpDistance", "value"): ValueBlock("getOpponentDistance","getOpDistance", parameters=()),
    ("getDistance", "value"): ValueBlock("getDistanceTo","getDistance", parameters=("X", "Y")),
    ("getDistance", "value"): ValueBlock("getDistanceTo","getDistance", parameters=("position",)),
    ("getTimeToNextAttack", "value"): ValueBlock("getTimeToNextAttack","getTimeToNextAttack", parameters=()),
    ("getTimeOpToNextAttack", "value"): ValueBlock("getOpTimeToNextAttack","getOpponentTimeToNextAttack", parameters=()),
    ("getLifes", "value"): ValueBlock("getLifes","getLifes", parameters=()),
    ("getOpLifes", "value"): ValueBlock("getOpLifes","getOpponentLifes", parameters=()),
    ("destinationReached", "value"): ValueBlock("destinationReached","destinationReached", parameters=()),
    ("onPos", "value"): ValueBlock("onPos","onPosistion", parameters=("X", "Y")),
    ("onPos", "value"): ValueBlock("onPos","onPosistion", parameters=("Position",)),
    ("onX", "value"): ValueBlock("onX","onX", parameters=("X",)),
    ("onY", "value"): ValueBlock("onY","onY", parameters=("Y",)),
    ("onBorder", "value"): ValueBlock("onBorder","onBorder", parameters=()),
    ("onLeftBorder", "value"): ValueBlock("onLeftBorder","onLeftBorder", parameters=()),
    ("onRightBorder", "value"): ValueBlock("onRightBorder","onRightBorder", parameters=()),
    ("onTopBorder", "value"): ValueBlock("onTopBorder","onTopBorder", parameters=()),
    ("onBottomBorder", "value"): ValueBlock("onBottomBorder","onBottomBorder", parameters=()),
}