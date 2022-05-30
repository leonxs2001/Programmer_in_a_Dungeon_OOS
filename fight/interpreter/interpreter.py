from fight.interpreter.parser import parse_sequence

class Interpreter:
    """
    Interpreter gets an initialisation sequence, a sequence and an instance.
    The initialisation sequence is parsed and interpreted at the beginnig.
    The other sequence only is parsed and saved.
    This parsed Sequence is interpreted every time by calling interpret().
    The instance needs the method call_method() in which the right things happen.
    """
    def __init__(self,initialization_sequence_string,sequence_string,instance):
        initialization_sequence_string = self.__delete_space(initialization_sequence_string)
        sequence_string = self.__delete_space(sequence_string)

        self.variabels = {}
        self.sequence = parse_sequence(sequence_string)
        self.instance = instance

        if initialization_sequence_string != "":
            self.__interpret(parse_sequence(initialization_sequence_string))

    def interpret(self):
        """
        Interpret the whole sequence by calling the private interpret Method with your own sequence
        """
        self.__interpret(self.sequence)

    def __delete_space(self,string):
        """
        Deletes all spaces \n and \t
        """
        string = string.replace(" ","")
        string = string.replace("\n","")
        string = string.replace("\t","")
        return string

    def __interpret(self, sequence):
        """
        Finds out which expresion a Tupel represents.
        """
        for element in sequence:
            if element[0] == "$":#is a variabel
                self.__interpret_variabel(element)
            elif element[0] == ".":#is a method
                self.__interpret_method(element)
            elif element[0] == "?":#is a condition
                self.__interpret_condition(element)

    def __interpret_expression(self,expression):
        """
        finds out if an expression is logical or arithmetic and than call the right Method
        """
        if isinstance(expression,tuple):
            if expression[0] in "+-*/^%":
                return self.__interpret_arithmetic_expression(expression)
            else:
                return self.__interpret_logical_expression(expression)
        else:
            return expression

    def __interpret_arithmetic_expression(self,expression):
        """
        Interprets a arithmetic expression
        """
        if isinstance(expression, tuple):#if the expression is a tupel we have to calculate
            if expression[0] == ".":#if the expression is a method it is important to call this
                return self.__interpret_method(expression)
            elif expression[0] == "$":#if the expression is a variabel it is important to use the value of the variabel
                if expression[1] in self.variabels:
                    return self.variabels[expression[1]]
                else: # if the variabel does not exist return 0
                    return 0

            result = self.__interpret_arithmetic_expression(expression[1])#calculate first part of the expression
            for exp in expression[2:]:#calculate the rest of expression by its operator(from the left the to right)
                if expression[0] == "+":
                    result += self.__interpret_arithmetic_expression(exp)
                elif expression[0] == "-":
                    result -= self.__interpret_arithmetic_expression(exp)
                elif expression[0] == "*":
                    result *= self.__interpret_arithmetic_expression(exp)
                elif expression[0] == "/":
                    result /= self.__interpret_arithmetic_expression(exp)
                elif expression[0] == "%":
                    result %= self.__interpret_arithmetic_expression(exp)
                elif expression[0] == "^":
                    result **= self.__interpret_arithmetic_expression(exp)
            return result
        else:#if the expression is not a tupel we dont need to calculate
            return expression

    def __interpret_logical_expression(self,expression):
        """
        Interprets a logical expression
        """
        
        if isinstance(expression,tuple):#if the expression is a tupel we have to calculate
            if expression[0] == ".":#if the expression is a method it is important to call this
                return self.__interpret_method(expression)
            elif expression[0] == "$":#if the expression is a variabel it is important to use the value of the variabel
                if expression[1] in self.variabels:
                    return self.variabels[expression[1]]
                else: # if the variabel does not exist return 0
                    return 0

            #apply the correct operator
            if expression[0] == "!":
                return not self.__interpret_logical_expression(expression[1])
            elif expression[0] == "&":
                result = self.__interpret_logical_expression(expression[1])#calculate the first part of the expression

                for exp in expression[2:]:#than calculate the rest
                    if not result:
                        return False
                    result = result and self.__interpret_logical_expression(exp)

                return result

            elif expression[0] ==  "|":
                result = self.__interpret_logical_expression(expression[1])#calculate the first part of the expression

                for exp in expression[2:]:#than calculate the rest
                    if result:
                        return True
                    result = result or self.__interpret_logical_expression(exp)

                return result
            #In case of comparison operators like = and != we need to call the interpret expression method(you can also compare boolean)
            #In case of comparison operators like <, >, <=, >= we only need to call the interpret arithmetic expression)
            elif expression[0] == "=":
                return self.__interpret_expression(expression[1]) == self.__interpret_expression(expression[2])
            elif expression[0] == "!=":
                return self.__interpret_expression(expression[1]) != self.__interpret_expression(expression[2])
            elif expression[0] == "<=":
                return self.__interpret_arithmetic_expression(expression[1]) <= self.__interpret_arithmetic_expression(expression[2])
            elif expression[0] == ">=":
                return self.__interpret_arithmetic_expression(expression[1]) >= self.__interpret_arithmetic_expression(expression[2])
            elif expression[0] == "<":
                return self.__interpret_arithmetic_expression(expression[1]) < self.__interpret_arithmetic_expression(expression[2])
            elif expression[0] == ">":
                return self.__interpret_arithmetic_expression(expression[1]) > self.__interpret_arithmetic_expression(expression[2])
        else:#if the expression is not a tupel we dont need to calculate
            return expression

    def __interpret_variabel(self,variabel):
        """
        Save the variabel in the dictionary variabels
        """
        self.variabels[variabel[1]] = self.__interpret_expression(variabel[2])

    def __interpret_method(self,method):
        """
        Get the parameters from the Tupel and than call the call_method method to manipulate the given instance
        """
        new_parameters = ()
        if len(method) > 2:#than we have parameters

            for para in method[2:]:
                new_parameters += (self.__interpret_expression(para),)

        return self.instance.call_method(method[1],new_parameters)

    def __interpret_condition(self,condition):
        """
        Interpret the condition
        """
        if self.__interpret_logical_expression(condition[1]):#if the logical expression is true, the right sequence have to be interpreted
            self.__interpret(condition[2])
        elif len(condition) == 4:#there is an else(more Arguments)
            self.__interpret(condition[3])






