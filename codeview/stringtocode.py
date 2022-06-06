import copy
from codeview.block.variabelblock import *
from fight.interpreter.parser import parse_sequence
from codeview.block.blockcreation import block_dict


def get_blocks_from_string(string, block_dict):
    """Create visualisation from code as String"""
    sequence = parse_sequence(string)#get the code three representation
    return get_blocks_from_sequence(sequence, block_dict)

def get_string_from_value(value):
    """Returns the stringrepresentation with the fewest digits"""
    if value == int(value):
        return str(int(value))
    else:
        return str(value)

def get_blocks_from_sequence(sequence, block_dict):
    """Create Visualisation from sequence as tuples"""
    if(len(sequence) == 0):#if the sequence is empty we cant create a new block
        return False
    else:
        block = None
        if sequence[0][0] == ".":#the block is a method block
            #get the block from the block dict and copy it
            method_name = sequence[0][1]
            if method_name == "goto" or method_name == "move" or method_name == "shootTo":
                if len(sequence[0]) == 4:
                    method_name += "0"
                else:
                    method_name += "1"
            elif method_name == "shoot":
                if len(sequence[0]) == 2:
                    method_name += "0"
                elif len(sequence[0]) == 4:
                    method_name += "1"
                else:
                    method_name += "2"

            block = block_dict[(method_name, "method")]
            block = copy.copy(block)
            #go through the parameters, create them as a block and rebuild 
            parameters = sequence[0][2:]
            for count, param in enumerate(parameters):
                if isinstance(param, tuple):#is a block to
                    block.input_fields[count].append(get_block_from_expression(param))
                    block.rebuild()
                else:#is only a normal value
                    block.input_fields[count].value = get_string_from_value(param)
                    block.input_fields[count].rebuild()

        elif sequence[0][0] == "?":#the block is a if block
            if len(sequence[0]) == 3:#is only a if
                #create the if block from die block_dict and copy it
                block = block_dict[("", "if")]
                block = copy.copy(block)
            else:#it is a if else
                #create the if block from die block_dict and copy it
                block = block_dict[("", "ifelse")]
                block = copy.copy(block)
                #get the blocks in the else part and add them to the right place
                if_false_block = get_blocks_from_sequence(sequence[0][3], block_dict)
                if if_false_block:
                    block.if_false_block = if_false_block
                    if_false_block.parent_block = block
                    block.rebuild()
            
            #get the block representation of the condition and add it to the right place
            condition = sequence[0][1]
            if isinstance(condition, tuple):#the inputfield
                block.input_field.append(get_block_from_expression(condition))
                block.rebuild()
            else:
                block.input_field.value = get_string_from_value(condition)
                block.input_field.rebuild()

            #get the blocks in the do part and add them to the right place
            if_true_block = get_blocks_from_sequence(sequence[0][2], block_dict)
            if if_true_block:
                block.if_true_block = if_true_block
                if_true_block.parent_block = block
                block.rebuild()

        elif sequence[0][0] == "$":#it is a variabel definition
            #create the right block and the VariabelBlock and add them to the Block dict
            name = sequence[0][1]
            block = VariabelDefinitionBlock(name)
            block_dict[(name,"variabeldefinition")] = copy.copy(block)
            block_dict[(name,"variabel")] = VariabelBlock(name)
            if isinstance(sequence[0][2], tuple):
                block.input_fields[0].append(get_block_from_expression(sequence[0][2]))
            else:
                block.input_fields[0].value = get_string_from_value(sequence[0][2])
                block.input_fields[0].rebuild()
            block.rebuild()
        else: 
            return False
            
        #get next block in the sequence and append it to the end
        next_block = get_blocks_from_sequence(sequence[1:], block_dict)
        if next_block:
            block.append(next_block)
            block.rebuild()
            next_block.rebuild()
    return block

def get_block_from_expression(expression):
    """Create the expression Visualisation (for opperations like +- and or etc and Methods with return value and Variabels)"""
    block = None
    if expression[0] == ".":#it is a Method with return value
        #create the block from the block_dict with inputs etc.
        block = block_dict[(expression[1], "value")]
        block = copy.copy(block)
        parameters = expression[2:]
        for count, param in enumerate(parameters):
            if isinstance(param, tuple):#is a block to
                block.input_fields[count].append(get_block_from_expression(param))
            else:#is only a normal value
                block.input_fields[count].value =get_string_from_value(param)
                block.input_fields[count].rebuild()

    elif expression[0] in "+-*/%^|&<=>=!=":#it is a opperation
        operation = expression[0]
        #convert the operation to the right representation
        if operation == "&":
            operation = "and"
        elif operation == "|":
            operation = "or"
        elif operation == "!":
            operation = "not"

        #get the block from the block_dict with inputs etc.
        block = block_dict[(operation, "operation")]
        block = copy.copy(block)
        parameters = expression[1:]
        for count, param in enumerate(parameters):
            if isinstance(param, tuple):
                block.input_fields[count].append(get_block_from_expression(param))
            else:
                block.input_fields[count].value =get_string_from_value(param)
                block.input_fields[count].rebuild()
    elif expression[0] == "$":
        #create the right block and the VariabelBlock and add them to the Block dict
        name = expression[1]
        block = VariabelBlock(name)
        block_dict[(name,"variabel")] = copy.copy(block)
        block_dict[(name,"variabeldefinition")] = VariabelDefinitionBlock(name)

    return block
