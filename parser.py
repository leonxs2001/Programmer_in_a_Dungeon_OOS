def parse_sequence(sequence):
    """
    This Method parse a whole Sequence and return some kind of a "code tree"
    """
    return_tupel = ()
    new_start = 0
    i = 0
    while i < len(sequence):

        if sequence[i] == ".":#its a method
            open_bracket_count =- 1
            i += 1
            while open_bracket_count != 0:

                if sequence[i] == "(":
                    if open_bracket_count == -1:
                        open_bracket_count = 1
                    else:
                        open_bracket_count += 1
                elif sequence[i] == ")":
                    open_bracket_count -= 1
                i += 1

            return_tupel += (parse_method(sequence[new_start:i]),)
            new_start = i
            i -= 1
        elif sequence[i] == "$":#it is a varaible
            while sequence[i] != "=": # go to the =
                i += 1
            i += 1
            while i < len(sequence) and not (sequence[i] == "?" or (sequence[i] in "$." and sequence[i-1] not in "+-/%^*=&|!<>")):
                i += 1
            return_tupel += (parse_variable(sequence[new_start:i]),)
            new_start = i
            i -= 1
        elif sequence[i] == "?":
            condition_tupel = ("?",)#tupel for the condition
            i += 1

            open_bracket_count =- 1
            #get condition. Is in ()
            while open_bracket_count != 0:
                if sequence[i] == "(":
                    if open_bracket_count == -1:
                        open_bracket_count = 1
                    else:
                        open_bracket_count += 1
                elif sequence[i]==")":
                    open_bracket_count -= 1
                i += 1

            #add condition to condition_tupel
            condition_tupel += (parse_logical_expression(sequence[new_start+1:i]),)

            i += 1
            new_start = i

            open_bracket_count = 1

            while open_bracket_count != 0:
                if sequence[i] == "{":
                    open_bracket_count += 1
                elif sequence[i] == "}":
                    open_bracket_count -= 1
                i += 1

            #add sequence if true
            condition_tupel += (parse_sequence(sequence[new_start:i-1]),)

            if i< len(sequence) and sequence[i] == "!":#there is an else
                i += 2
                new_start = i

                open_bracket_count = 1

                while open_bracket_count != 0:
                    if sequence[i] == "{":
                        open_bracket_count += 1
                    elif sequence[i] == "}":
                        open_bracket_count -= 1
                    i += 1

                #add sequence if false
                condition_tupel += (parse_sequence(sequence[new_start:i-1]),)

            new_start = i

            return_tupel += (condition_tupel,)
            i -= 1

        i += 1
    return return_tupel

#returns parsed Logical Expression as Tupel
def parse_logical_expression(logical_expression):
    """return parsed logical Expression"""
    logical_expression = delete_outside_brackets(logical_expression)

    #Seperate fist on |(logical or) than &(logical and) than !(logical not) than =, !=, <, <=, >, >=
    i = 0
    last_symbol = "f"#is only a filler
    positions = ()
    open_bracket_count = 0
    while i < len(logical_expression):
        if logical_expression[i] == "(":
            open_bracket_count += 1
        elif logical_expression[i] == ")":
            open_bracket_count -= 1
        elif open_bracket_count == 0: #only look for operators if we are not in Brackets
            if logical_expression[i] == "|":
                if last_symbol == "|":
                    positions += (i,)#add | position to position
                else:
                    last_symbol = "|"
                    positions = (i,)
            elif logical_expression[i] == "&" and last_symbol != "|":
                if last_symbol == "&":
                    positions += (i,)#add | position to position
                else:
                    last_symbol = "&"
                    positions = (i,)
            elif logical_expression[i] == "!" and last_symbol not in "!|&":
                if i+1!=len(logical_expression):#i+1!=len(logical_expression) is only to prohibit errors
                    if logical_expression[i+1] == "=":#than it is != ; 
                        last_symbol = "!="
                        positions = (i,)
                        i += 1
                    else:#than it is a !
                        last_symbol = "!"
                        positions = (0,)#iso n each case on position 0
                else:
                    raise RuntimeError("There is an ! on wrong point")#raise an exception because of a ! on a wrong place
            elif logical_expression[i] in "<>" and last_symbol not in "|&!":
                if i+1 != len(logical_expression):#i+1!=len(logical_expression) is only to prohibit errors
                    last_symbol = logical_expression[i]
                    positions = (i,)
                    if logical_expression[i+1] == "=":#it is <= or >=
                        last_symbol += "="
                        i += 1
                else: 
                    raise RuntimeError("There is an "+logical_expression[i]+" on wrong point")#raise an exception because of a < or > on a wrong place
            elif logical_expression[i] == "=" and last_symbol not in "|&!":
                 
                last_symbol = logical_expression[i]
                positions = (i,)
        i += 1

    #check which operator was the importanst symbol
    #and than add this operator with its operands
    if last_symbol in "|&":
        return_tupel = (last_symbol,parse_logical_expression(logical_expression[:positions[0]]))#set the maker and add first argument
        for i in range(1,len(positions)):
            return_tupel += (parse_logical_expression(logical_expression[positions[i-1]+1:positions[i]]),) # add operand 
        return_tupel += (parse_logical_expression(logical_expression[positions[len(positions)-1]+1:]),)#add last operand
        return return_tupel
    elif last_symbol == "!":
        return ('!',parse_logical_expression(logical_expression[1:]))
    elif last_symbol[0] in "!=<>":#than it is relational
        return_tupel = (last_symbol,)
        if len(last_symbol) > 1: #than it is >= <= or !=
            return_tupel += (parse_logical_expression(logical_expression[:positions[0]]),parse_logical_expression(logical_expression[positions[0]+2:]))
        else:#than it is < > or =
            return_tupel += (parse_logical_expression(logical_expression[:positions[0]]),parse_logical_expression(logical_expression[positions[0]+1:]))
        return return_tupel
    elif logical_expression == "t":
        return True
    elif logical_expression == "f":
        return False
    else:
        operators = "+-/%^*"
        no_operators = True
        for op in operators:
            if op in logical_expression:
                no_operators = False
        if not no_operators:#there are operators
            return parse_arithmetic_expression(logical_expression)
        elif logical_expression[0] == ".":#maybe it is a single method
            return parse_method(logical_expression)
        elif logical_expression[0] ==" $":#is variable
            return parse_variable(logical_expression)
    
        try:
            return float(logical_expression)
        except ValueError:
            return logical_expression

def parse_arithmetic_expression(arithmetic_expression):
    """return parsed arithmetic expression"""
    arithmetic_expression = delete_outside_brackets(arithmetic_expression)

    #Seperate fist on + and - first than * thand / and % than ^
    i = 0
    last_symbol = "f"#is only a filler
    positions = ()
    open_bracket_count = 0

    while i < len(arithmetic_expression):
        if arithmetic_expression[i] == "(":
            open_bracket_count += 1
        elif arithmetic_expression[i] == ")":
            open_bracket_count -= 1
        elif open_bracket_count == 0: #only look for operators if we are not in Brackets
            if arithmetic_expression[i] == "+":
                if last_symbol == "-":
                    last_symbol = "+-"
                    positions = ((i,),positions)#left side for the + and right side for -
                elif last_symbol == "+-":
                    positions = (positions[0]+(i,),positions[1])
                elif last_symbol == "+":
                    positions += (i,)
                else:
                    last_symbol="+"
                    positions = (i,)
            elif arithmetic_expression[i] == "-" and i!=0 and arithmetic_expression[i-1] not in "+-*/^%|!=&<>":#not a negative number
                if last_symbol == "+":
                    last_symbol = "+-"
                    positions=(positions,(i,))#left side for the + and right side for -
                elif last_symbol == "+-":
                    positions = (positions[0],positions[1]+ (i,))
                elif last_symbol == "-":
                    positions += (i,)
                else:
                    last_symbol = "-"
                    positions = (i,)
            elif arithmetic_expression[i] == "*" and last_symbol not in "+-":
                if last_symbol == "*":
                    positions += (i,)
                else:
                    last_symbol = "*"
                    positions = (i,)
            elif arithmetic_expression[i] == "/" and last_symbol not in "+-*":
                if last_symbol == "%":
                    last_symbol = "/%"
                    positions = ((i,),positions)#left side for the / and right side for %
                elif last_symbol == "/%":

                    positions = (positions[0]+(i,),positions[1])
                elif last_symbol == "/":
                    positions += (i,)
                else:
                    last_symbol = "/"
                    positions = (i,)
            elif arithmetic_expression[i] == "%"and last_symbol not in "+-*":
                if last_symbol == "/":
                    last_symbol = "/%"
                    positions = (positions,(i,))#left side for the / and right side for %
                elif last_symbol == "/%":
                    positions = (positions[0],positions[1]+ (i,))
                elif last_symbol == "%":
                    positions += (i,)
                else:
                    last_symbol = "%"
                    positions = (i,)
            elif arithmetic_expression[i] == "^" and last_symbol not in "+-*/%":
                if last_symbol == "^":
                    positions += (i,)
                else:
                    last_symbol = "^"
                    positions = (i,)
        i += 1
    if last_symbol in "-+%/^":
        return_tupel = (last_symbol,parse_logical_expression(arithmetic_expression[:positions[0]]))#set the maker and add first argument
        for i in range(1,len(positions)):
            return_tupel += (parse_arithmetic_expression(arithmetic_expression[positions[i-1]+1:positions[i]]),) # add operand 
        return_tupel += (parse_arithmetic_expression(arithmetic_expression[positions[len(positions)-1]+1:]),)#add last operand
        return return_tupel
    elif last_symbol == "+-":
        #create one Tupel with all posizions of + and -(merge together)
        new_positions = ()
        l = 0#for the plusses
        k = 0#for the minuses
        while l<len(positions[0]) and k < len(positions[1]):
            if positions[0][l] < positions[1][k]:
                new_positions += (positions[0][l],)
                l += 1
            else:
                new_positions += (positions[1][k],)
                k += 1

        if l < len(positions[0]):
            for i in range(l,len(positions[0])):
                new_positions += (positions[0][i],)
        elif k < len(positions[1]):
            for i in range(k,len(positions[1])):
                new_positions += (positions[1][i],)
        
        #save followerposition of every operator by its position
        follower = {}
        for i in range(0,len(new_positions)-1):
            follower[new_positions[i]] = new_positions[i+1]
        follower[new_positions[len(new_positions)-1]] = len(arithmetic_expression)
        
        return_tupel = ("+",)#set the maker
        #add all adition operands
        for i in range (0,len(positions[0])):
            return_tupel += (parse_arithmetic_expression(arithmetic_expression[positions[0][i]+1:follower[positions[0][i]]]),)

        #add all subtraction operands
        return_tupel2 = ("-",parse_arithmetic_expression(arithmetic_expression[:new_positions[0]]))#set the maker and add first argument(first operand)
        for i in range (0,len(positions[1])):
            return_tupel2 += (parse_arithmetic_expression(arithmetic_expression[positions[1][i]+1:follower[positions[1][i]]]),)
        return_tupel += (return_tupel2,)

        return return_tupel

    elif last_symbol == "*":
        return_tupel = ("*",parse_arithmetic_expression(arithmetic_expression[:positions[0]]))#set the maker and add first argument
        for i in range(0,len(positions)-1):
            return_tupel += (parse_arithmetic_expression(arithmetic_expression[positions[i]+1:positions[i+1]]),)
        return_tupel += (parse_arithmetic_expression(arithmetic_expression[positions[len(positions)-1]+1:]),)
        return return_tupel
    elif last_symbol == "/%":
        #create one Tupel with all positions of / and %(merge together)
        new_positions = ()
        operators = ()#save the operator to the position
        l=0#for the /
        k=0#for the %
        while l<len(positions[0]) and k < len(positions[1]):
            if positions[0][l] < positions[1][k]:
                new_positions += (positions[0][l],)
                operators += ("/",)
                l += 1
            else:
                new_positions += (positions[1][k],)
                operators += ("%",)
                k += 1

        if l < len(positions[0]):
            for i in range(l,len(positions[0])):
                new_positions += (positions[0][i],)
                operators += ("/",)
        elif k < len(positions[1]):
            for i in range(k,len(positions[1])):
                new_positions += (positions[1][i],)
                operators += ("%",)

        return_tupel = (operators[0],parse_arithmetic_expression(arithmetic_expression[0:new_positions[0]]),parse_arithmetic_expression(arithmetic_expression[new_positions[0]+1:new_positions[1]]))
        for i in range(1,len(operators)-1):
            return_tupel = (operators[i],return_tupel,parse_arithmetic_expression(arithmetic_expression[new_positions[i]+1:new_positions[i+1]]))
        return_tupel = (operators[len(operators)-1],return_tupel,parse_arithmetic_expression(arithmetic_expression[new_positions[len(operators)-1]+1:]))
        return return_tupel
    elif arithmetic_expression[0] == ".":#is method
        return parse_method(arithmetic_expression)
    elif arithmetic_expression[0] == "$":#is variable
        return parse_variable(arithmetic_expression)
    else:
        try:
            return float(arithmetic_expression)
        except ValueError:
            print("Es gab ein Problem, da der Wert keine Nummer ist!",arithmetic_expression)
            return arithmetic_expression


def delete_outside_brackets(command):
    """delete all Brackets if they are completely outside e.g.: "(hallo())" is going to be hallo()"""
    changed = True#shows, that the logical Expression is a new one. Have to be checked for Brackets
    while changed:
        changed = False
        if command[0] == "(":
            open_bracket_count = 1
            i = 1
            while i < len(command):
                if command[i] == "(":
                    open_bracket_count += 1
                elif command[i] == ")":
                    open_bracket_count -= 1

                if open_bracket_count == 0:
                    
                    if i == len(command) - 1:
                        command = command[1:-1]
                        changed = True
                    i = len(command)
                i += 1
    return command

def parse_expression(expression):
    """decide which type of expression it is and parse ist"""
    operators = "<>=!&|"
    is_logic = False
    i=  0
    if expression == "t":
        return True
    elif expression == "f":
        return False

    while i < len(operators) and not is_logic:
        if operators[i] in expression:
            is_logic = True
        i += 1

    if is_logic:
        return parse_logical_expression(expression)
    else:
        return parse_arithmetic_expression(expression)


def parse_variable(variable):
    """gets variable command with the $ and return parsed variable"""
    variable = variable[1:]
    variable_name = ""
    variable_definition = "n"#filler
    if "=" in variable:#with definition
        variables = variable.split("=",1)
        variable_name = variables[0]
        variable_definition = variables[1]
        variable_definition = parse_expression(variable_definition)
    else:
        variable_name = variable
    
    if variable_definition == "n":
        return ("$",variable_name)
    else:
        return ("$",variable_name,variable_definition)

def parse_method(method):
    """gets method command with . and return parsed method"""
    method = method[1:]
    methods = method.split("(",1)
    method_name = methods[0]
    method_parameter = methods[1][:-1]
    if method_parameter == "":
        return (".",method_name)
    else:
        parameters = ()
        start = 0
        open_bracket_counter = 0
        for i in range(0,len(method_parameter)):
            if method_parameter[i] == "(":
                open_bracket_counter += 1
            elif method_parameter[i] == ")":
                open_bracket_counter -= 1
            elif open_bracket_counter == 0:
                if method_parameter[i] == ",":
                    parameters += (parse_expression(method_parameter[start:i]),)
                    start = i+1#set next start
        parameters += (parse_expression(method_parameter[start:]),)
        return (".",method_name) + parameters
