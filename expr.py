from variable import *
global DEBUG
DEBUG = False

"""
A <val> should not have " and a digit in it, in any circumstance
"""
def val_valid(val):
    #checks if only valid characters are used
    for char in val:
        if char != '"' and not char.isalnum() and char!=" " and char!="~":
            return False
    
    string_lit = False
    is_int = False
    if val.find("\"")!=-1:
        string_lit = True
    #int
    if any(char.isdigit() for char in val):
        is_int = True
    if string_lit and is_int:
        return False
    return True

"""
A var_name should not have a digit in it, in any circumstance
"""
def var_valid(var_name):
    contains_alpha = any(char.isalpha() for char in var_name)
    contains_digit = any(char.isdigit() for char in var_name)
    if contains_alpha and contains_digit:
        return False
    return True

"""
determine if the val is a var_name or not.
True, if it is a var_name
"""
def is_var(val):
    return (val.find("\"")==-1) and \
            not(any(char.isdigit() for char in val)) and \
            (val!="true" and val!="false") and val!="~"

"""parse_expr_to_type(expr): INPUTS a single EXPR, and return the type as a STRING.
                             Valid types of expr are: "<val>", <math_expr>, <comp_expr>.
                             if no operators >> <val>
                             if both operators >> error string
"""
def parse_expr_to_type(expr):
    type_retval = ""
    comp_ops = ["==",  "/=",  ">=", "<=", "<<", ">>"]
    math_ops = ["+", "-", "*","/", "%","&&","||"]
    for op in comp_ops:
        if expr.find(op)!=-1:
            type_retval = "<comp_expr>"
    for op in math_ops:
        if expr.find(op)!=-1:
            if type_retval =="":
                type_retval = "<math_expr>"
            else:
                print("ERROR: both types of ops found in >>"+str(expr)+"<<")
                return None
    if type_retval=="":
        if "~" in expr:
            if (expr[0]!="~") or not(expr[0]=="~" and all(char.isdigit() for char in expr[1:])):
                print("ERROR: Incorrect syntax for negative number >>"+str(expr)+"<<")
                return None

        type_retval = "<val>"
    if(DEBUG):
        print(str(expr),"is being parsed as a",str(type_retval))
    return type_retval
"""
helps gather left and right variables for an expression with an operator
"""
def parse_var_to_lookup_helper(expr,ops):
    ret_val = []
    for op in ops:
        if expr.find(op)!=-1:
            expr = expr.split(op)
            left = expr[0].strip()
            right = expr[1].strip()
            # if left not string literal, int or bool
            if is_var(left):
                if var_valid(left):
                    ret_val.append(left)
                else:
                    print("ERROR",str(left),"is not a valid variable name.")
                    return None
            # if right not string literal, int or bool
            if is_var(right):
                if var_valid(right):
                    ret_val.append(right) 
                else:
                    print("ERROR:", str(right),"is not a valid variable name.")
                    return None
            if DEBUG:
                print("Looking up the variables in this list ->",str(ret_val))
            return ret_val
"""
parse_var_to_lookup(expr): INPUTS a single EXPR, and returns a list of variables to look up.
                           Eg. "{x + y}" should return ["x", "y"].

                           if expr type cannot be determined >> error string returned
"""
def parse_var_to_lookup(expr):
    expr = expr.strip()
    lookup = []
    expr_type = parse_expr_to_type(expr)
    if expr_type is None:
        return None
    if expr_type=="<val>":
        #invalid val
        if not(val_valid(expr)):
            print("ERROR: <val> type contains invalid combination-of-characters/character(s) in >>"+str(expr)+"<<")
            return None
        #string_literal
        if expr.find("\"")!=-1:
            if expr[0]=="\"" and expr[-1]=="\"":
                return lookup
            else:
                print("ERROR: string literal not in correct format: "+str(expr))
                return None
        #int
        if all(char.isdigit() for char in expr[1:]) and ((expr[0].isdigit()) or (expr[0]=="~" and expr[1:].strip()!="")):
            return lookup
        #bool
        if expr=="true" or expr=="false":
            return lookup
        #var_name
        if var_valid(expr):
            lookup.append(expr)
            if DEBUG:
                print("Looking up the variables in this list ->",str(lookup))
            return lookup
        else:
            print("ERROR:",str(expr),"is not a valid variable name.")
            return None
    elif expr_type == "<comp_expr>":
        to_add = parse_var_to_lookup_helper(expr,["==",  "/=",  ">=", "<=", "<<", ">>"]) 
        if to_add is None:
            return None
        lookup += to_add

    elif expr_type == "<math_expr>":
        to_add = parse_var_to_lookup_helper(expr,["+", "-", "*","/", "%","&&","||"]) 
        if to_add is None:
            return None
        lookup += to_add 
    # error case
    else: 
        print("ERROR: Ran into an uncaught error with expression: "+str(expr))
        return None
    return lookup
"""
exec_expr(expr, lookup_dict): inputs an EXPR, and a dictionary of the form var_name: value (the class value). 
                            Return the value of that expression as a VALUE type. Perform error checking here.
                            Check if a variable is not defined. 
                            Check if a variable is not of the right type. Check if the types are right.
                            This is only for when we run in interpreter mode.


class Value:
    def __init__(self, value, type):
        self.value = value
        self.type = type

value = "xyz", type = "str" 
<int> | <bool> | <str_literal>
"""

def operator_expr_exec(expr,lookup_dict,ops,is_comp):
    original_expr = expr
    for op in ops:
        if expr.find(op)!=-1:
            if DEBUG:
                print("Parsing",str(expr),"using the",str(op),"operator.")
            expr = expr.split(op)
            left = expr[0].strip()
            right = expr[1].strip()
            # if left not string literal, int or bool
            if is_var(left):
                if var_valid(left):
                    if left in lookup_dict:
                        left = lookup_dict[left].value
                    else:
                        print("ERROR:",str(left),"has not been defined yet."+"(in "+str(original_expr)+")")
                        return None
                else:
                    print("ERROR",str(left),"is not a valid variable name." +"(in "+str(original_expr)+")")
                    return None
            # left is a string literal
            elif left.find("\"")!=-1:
                if left[0]=="\"" and left[-1]=="\"":
                    left = left.strip("\"")
                else:
                    print("ERROR: string literal not in correct format: "+str(left) +" in "+str(original_expr))
                    return None
            # left is an int
            elif all(char.isdigit() for char in left[1:]) and (left[0].isdigit() or left[0]=="~" and left[1:].strip()!=""):
                left = left.replace("~","-")
                left = int(left)
            # left is a bool
            elif left=="true":
                left = True
            elif left=="false":
                left = False
            elif left=="~":
                pass
            else:
                print("ERROR: Trouble parsing "+str(left)+ " in "+str(original_expr))
                return None
            # if right not string literal, int or bool
            if is_var(right):
                if var_valid(right):
                    if right in lookup_dict:
                        right = lookup_dict[right].value
                    else:
                        print("ERROR:",str(right),"has not been defined yet."+"(in "+str(original_expr)+")")
                        return None
                else:
                    print("ERROR",str(right),"is not a valid variable name." +"(in "+str(original_expr)+")")
                    return None
            # right is a string literal
            elif right.find("\"")!=-1:
                if right[0]=="\"" and right[-1]=="\"":
                    right = right.strip("\"")
                else:
                    print("ERROR: string literal not in correct format: "+str(right) +" in "+str(original_expr))
                    return None
            # right is an int
            elif all(char.isdigit() for char in right[1:]) and ((right[0].isdigit()) or (right[0]=="~" and right[1:].strip()!="")):
                right = right.replace("~","-")
                right = int(right)
            # right is a bool
            elif right=="true":
                right = True
            elif right=="false":
                right = False
            else:
                print("ERROR: Trouble parsing "+str(right)+ " in >>"+str(original_expr)+"<<.")
                return None
            if DEBUG:
                if type(left)==str and left!="~":
                    print("Determined left hand side to be -> \""+str(left)+'"')
                else:
                    print("Determined left hand side to be ->",str(left))
                print("Operator used is",str(op))
                if type(right)==str:
                    print("Determined right hand side to be -> \""+str(right)+'"\n')
                else:
                    print("Determined right hand side to be ->",str(right)+"\n")
            # HERE IS WHERE MATH EXPR AND COMP EXPR PARSE BRANCHES
            # different checking if math expr
            if not(is_comp):
                if left=="~":
                    if type(right)!=bool:
                        print("ERROR: Cannot negate non boolean",str(right)+".")
                        return None
                elif type(left)!=type(right):
                    print("ERROR: Types on both sides of the operator are not the same in expr>>",str(original_expr)+"<<.")
                    return None
                #types on right sides determine type

                #str operations
                if type(right)==str:
                    if op!="+":
                        print("ERROR: Cannot perform",str(op),"operation between strings",str(left),"and",str(right)+".")
                        return None
                    return left+right
                    
                #bool operation
                #["~ &&","&&","||"]
                elif type(right)==bool:
                    if op=="&&":
                        if left=="~":
                            return not(right)
                        else:
                            return (left and right)
                    elif op=="||":
                        return (left or right)
                    else:
                        print("ERROR: Cannot perform",str(op),"operation between booleans",str(left),"and",str(right)+".")
                        return None
                #int operation
                #["+", "-", "*","/", "%"]
                #assuming types of left and right are int
                else:
                    if op=="+":
                        return left+right
                    elif op=="-":
                        return left-right
                    elif op=="*":
                        return int(left*right)
                    elif op=="/":
                        return int(left/right)
                    elif op=="%":
                        return left%right
                    else:
                        print("ERROR: Cannot perform",str(op),"operation between integers",str(left),"and",str(right)+".")
                        return None

            #comp expr, left and right defined now use operator
            #["==",  "/=",  ">=", "<=", "<<", ">>"]
            else:
                try:
                    if op=="==":
                        return left==right
                    elif op=="/=":
                        return left!=right
                    elif op==">=":
                        return left>=right
                    elif op=="<=":
                        return left<=right
                    elif op=="<<":
                        return left<right
                    else:
                        return left>right
                except:
                    print("ERROR: Values",str(left),"and",str(right),"cannot be compared using comparison operators in",str(original_expr)+".")
                    return None

            

def exec_expr(expr,lookup_dict):
    if(DEBUG):
        print("\nParsing expression:",str(expr))
    expr = expr.strip()
    expr_type = parse_expr_to_type(expr)
    if expr_type is None:
        return None
    if expr_type=="<val>":
        #invalid val
        if not(val_valid(expr)):
            print("ERROR: <val> type contains invalid combination-of-characters/character(s) or in >>"+str(expr)+"<<")
            return None
        #string_literal
        if expr.find("\"")!=-1:
            if expr[0]=="\"" and expr[-1]=="\"":
                if DEBUG:
                    print(str(expr),"was found to be a string_literal.\n")
                return Value(expr.strip("\""),"str")
            else:
                print("ERROR: string literal not in correct format: "+str(expr))
                return None
        #int
        if all(char.isdigit() for char in expr[1:]) and ((expr[0].isdigit()) or (expr[0]=="~" and expr[1:].strip()!="")):
            if DEBUG:
                print(str(expr),"was found to be an int.\n")
            if expr[0]=="~":
                expr = expr.replace("~","-")
            return Value(int(expr),"int")
        #bool
        if expr=="true" or expr=="false":
            if DEBUG:
                print(str(expr),"was found to be a bool.\n")
            if(expr=="true"):
                return Value(True,"bool")
            else:
                return Value(False,"bool")
        #var_name
        if var_valid(expr):
            if expr in lookup_dict:
                if DEBUG:
                    print(str(expr),"was found to be a variable name.\n")
                return lookup_dict[expr]
            else:
                print("ERROR:",str(expr),"has not been defined yet.")
                return None
        else:
            print("ERROR:",str(expr),"is not a valid variable name.")
            return None

    elif expr_type == "<comp_expr>":
        vars = parse_var_to_lookup(expr)
        if vars is None:
            return None
        if DEBUG:
            print("Going to look up vars in ->",str(vars))
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",str(var),"has not been defined yet.")
                return None
        actual_val = operator_expr_exec(expr,lookup_dict,["==",  "/=",  ">=", "<=", "<<", ">>"],True)
        if actual_val is None:
            return None
        return Value(actual_val,"bool")
        
        

    elif expr_type == "<math_expr>":
        vars = parse_var_to_lookup(expr)
        if vars is None:
            return None
        if DEBUG:
            print("Going to look up vars in ->",str(vars))
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",str(var),"has not been defined yet.")
                return None
        ret_val = operator_expr_exec(expr,lookup_dict,["+", "-", "*","/", "%","&&","||"],False)
        if ret_val is None:
            return None
        if type(ret_val)==str:
            return Value(ret_val,"str")
        elif type(ret_val)==bool:
            return Value(ret_val,"bool")
        #assuming int
        else:
            return Value(ret_val,"int")
        #check the type of the return value, then return a value type
    # error case
    else: 
        print("ERROR: Ran into an unknown error with expression: "+str(expr))
        return None



def convert_to_python_operator_expr_exec(expr,lookup_dict,ops,is_comp):
    original_expr = expr
    left_is_var = False
    right_is_var =False
    for op in ops:
        if expr.find(op)!=-1:
            if DEBUG:
                print("Parsing",str(expr),"using the",str(op),"operator.")
            expr = expr.split(op)
            left = expr[0].strip()
            right = expr[1].strip()
            # if left not string literal, int or bool
            if is_var(left):
                if var_valid(left):
                    if left in lookup_dict:
                        left_is_var = True
                        left_name = left
                        left = lookup_dict[left].value
                    else:
                        print("ERROR:",str(left),"has not been defined yet."+"(in "+str(original_expr)+")")
                        return None
                else:
                    print("ERROR",str(left),"is not a valid variable name." +"(in "+str(original_expr)+")")
                    return None
            # left is a string literal
            elif left.find("\"")!=-1:
                if left[0]=="\"" and left[-1]=="\"":
                    left = left.strip("\"")
                else:
                    print("ERROR: string literal not in correct format: "+str(left) +" in "+str(original_expr))
                    return None
            # left is an int
            elif all(char.isdigit() for char in left[1:]) and ((left[0].isdigit()) or ( left[0]=="~" and left[1:].strip()!="")):
                left = left.replace("~","-")
                print(left)
                left = int(left)
            # left is a bool
            elif left=="true":
                left = True
            elif left=="false":
                left = False
            elif left=="~":
                pass
            else:
                print("ERROR: Trouble parsing "+str(left)+ " in "+str(original_expr))
                return None
            # if right not string literal, int or bool
            if is_var(right):
                if var_valid(right):
                    if right in lookup_dict:
                        right_is_var = True
                        right_name = right
                        right = lookup_dict[right].value
                    else:
                        print("ERROR:",str(right),"has not been defined yet."+"(in "+str(original_expr)+")")
                        return None
                else:
                    print("ERROR",str(right),"is not a valid variable name." +"(in "+str(original_expr)+")")
                    return None
            # right is a string literal
            elif right.find("\"")!=-1:
                if right[0]=="\"" and right[-1]=="\"":
                    right = right.strip("\"")
                else:
                    print("ERROR: string literal not in correct format: "+str(right) +" in "+str(original_expr))
                    return None
            # right is an int
            elif all(char.isdigit() for char in right[1:]) and ((right[0].isdigit()) or (right[0]=="~" and right[1:].strip()!="")):
                right = right.replace("~","-")
                right = int(right)
            # right is a bool
            elif right=="true":
                right = True
            elif right=="false":
                right = False
            else:
                print("ERROR: Trouble parsing "+str(right)+ " in >>"+str(original_expr)+"<<.")
                return None
            if DEBUG:
                if type(left)==str and left!="~":
                    print("Determined left hand side to be -> \""+str(left)+'"')
                else:
                    print("Determined left hand side to be ->",str(left))
                print("Operator used is",str(op))
                if type(right)==str:
                    print("Determined right hand side to be -> \""+str(right)+'"\n')
                else:
                    print("Determined right hand side to be ->",str(right)+"\n")
            # HERE IS WHERE MATH EXPR AND COMP EXPR PARSE BRANCHES
            # different checking if math expr
            if not(is_comp):
                if left=="~":
                    if type(right)!=bool:
                        print("ERROR: Cannot negate non boolean",str(right)+".")
                        return None
                elif type(left)!=type(right):
                    print("ERROR: Types on both sides of the operator are not the same in expr>>",str(original_expr)+"<<.")
                    return None
                #types on right sides determine type

                #str operations
                if type(right)==str:
                    if op!="+":
                        print("ERROR: Cannot perform",str(op),"operation between strings",str(left),"and",str(right)+".")
                        return None
                    left = left_name if left_is_var else f'"{left}"'
                    right = right_name if right_is_var else f'"{right}"'
                    return left + " + " + right
                    
                #bool operation
                #["~ &&","&&","||"]
                elif type(right)==bool:
                    left = left_name if left_is_var else str(left)
                    right = right_name if right_is_var else str(right)
                    if op=="&&":
                        if left=="~":
                            return "not "+right
                        else:
                            return left + " and " + right
                    elif op=="||":
                        return left + " or " + right
                    else:
                        print("ERROR: Cannot perform",str(op),"operation between booleans",str(left),"and",str(right)+".")
                        return None
                #int operation
                #["+", "-", "*","/", "%"]
                #assuming types of left and right are int
                else:
                    left = left_name if left_is_var else str(left)
                    right = right_name if right_is_var else str(right)
                    if op=="+":
                        return left+" + "+right
                    elif op=="-":
                        return left+" - "+right
                    elif op=="*":
                        return "int("+left+" * "+right + ")"
                    elif op=="/":
                        return "int("+left+" / "+right + ")"
                    elif op=="%":
                        return left+" % "+right
                    else:
                        print("ERROR: Cannot perform",str(op),"operation between integers",str(left),"and",str(right)+".")
                        return None

            #comp expr, left and right defined now use operator
            #["==",  "/=",  ">=", "<=", "<<", ">>"]
            else:
                if type(left)!=type(right):
                    print("ERROR: Types on both sides of the operator are not the same in expr>>",str(original_expr)+"<<.")
                    return None
                    #types on both sides are equal
                try:
                    if left_is_var:
                        left=left_name
                    else:
                        if type(left)==str:
                            left = '"'+left+'"'
                        else:
                            left = str(left)
                    if right_is_var:
                        right=right_name
                    else:
                        if type(right)==str:
                            right = '"'+right+'"'
                        else:
                            right = str(right)
                    if op=="==":
                        return left+" == "+right
                    elif op=="/=":
                        return left+" != "+right
                    elif op==">=":
                        return left+" >= "+right
                    elif op=="<=":
                        return left+" <= "+right
                    elif op=="<<":
                        return left+" < "+right
                    else:
                        return left+" > "+right
                except:
                    print("ERROR: Values",str(left),"and",str(right),"cannot be compared using comparison operators in",str(original_expr)+".")
                    return None

"""
convert_to_python(expr): INPUTS an EXPR, and returns a string of python code that will evaluate the expression.
                         This is for when we run in compiler mode.
                         This is for when we run in compiler mode.
"""
def convert_to_python(expr,lookup_dict):
    if(DEBUG):
        print("\nParsing expression:",str(expr))
    expr = expr.strip()
    expr_type = parse_expr_to_type(expr)
    if expr_type is None:
        return None
    if expr_type=="<val>":
        #invalid val
        if not(val_valid(expr)):
            print("ERROR: <val> type contains invalid combination-of-characters/character(s) in >>"+str(expr)+"<<")
            return None
        #string_literal
        if expr.find("\"")!=-1:
            if expr[0]=="\"" and expr[-1]=="\"":
                if DEBUG:
                    print(str(expr),"was found to be a string_literal.\n")
                return expr
            else:
                print("ERROR: string literal not in correct format: "+str(expr))
                return None
        #int
        if all(char.isdigit() for char in expr[1:]) and ((expr[0].isdigit()) or(expr[0]=="~" and expr[1:].strip()!="")):
            if DEBUG:
                print(str(expr),"was found to be an int.\n")
            if expr[0]=="~":
                expr = expr.replace("~","-")
            return expr
        #bool
        if expr=="true" or expr=="false":
            if DEBUG:
                print(str(expr),"was found to be a bool.\n")
            if(expr=="true"):
                return "True"
            else:
                return "False"
        #var_name
        if var_valid(expr):
            if expr in lookup_dict:
                if DEBUG:
                    print(str(expr),"was found to be a variable name.\n")
                return expr
            else:
                print("ERROR:",str(expr),"has not been defined yet.")
                return None
        else:
            print("ERROR:",str(expr),"is not a valid variable name.")
            return None

    elif expr_type == "<comp_expr>":
        vars = parse_var_to_lookup(expr)
        if vars is None:
            return None
        if DEBUG:
            print("Going to look up vars in ->",str(vars))
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",str(var),"has not been defined yet.")
                return None
        return convert_to_python_operator_expr_exec(expr,lookup_dict,["==",  "/=",  ">=", "<=", "<<", ">>"],True)


    elif expr_type == "<math_expr>":
        vars = parse_var_to_lookup(expr)
        if vars is None:
            return None
        if DEBUG:
            print("Going to look up vars in ->",str(vars))
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",str(var),"has not been defined yet.")
                return None
        return convert_to_python_operator_expr_exec(expr,lookup_dict,["+", "-", "*","/", "%","&&","||"],False)
    # error case
    else: 
        print("ERROR: Ran into an unknown error with expression: "+str(expr))
        return None