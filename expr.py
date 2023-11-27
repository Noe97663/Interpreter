import sys
from variable import *

"""
A <val> should not have " and a digit in it, in any circumstance
"""
def val_valid(val):
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
True, if var_name
"""
def is_var(val):
    return (val.find("\"")==-1) and \
            not(all(char.isdigit() for char in val)) and \
            (val!="true" and val!="false")

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
                print("ERROR: both types of ops found in >>"+expr+"<<")
                sys.exit(1)
    if type_retval=="":
        type_retval = "<val>"
    return type_retval
"""
helps gather left and right variables for an expression with an operator
"""
def parse_var_to_lookup_helper(expr,ops):
    ret_val = []
    for op in ops:
            if expr.find(op)!=-1:
                expr = expr.split(op)
                left = expr[0]
                right = expr[1]
                # if left not string literal, int or bool
                if is_var(left):
                    if var_valid(left):
                        ret_val.append(left)
                    else:
                        print("ERROR",left,"is not a valid variable name.")
                        sys.exit(0)
                # if right not string literal, int or bool
                if is_var(right):
                    if var_valid(right):
                        ret_val.append(right) 
                    else:
                        print("ERROR:", right,"is not a valid variable name.")
                        sys.exit(0)
                return ret_val
"""
parse_var_to_lookup(expr): INPUTS a single EXPR, and returns a list of variables to look up.
                           Eg. "{x + y}" should return ["x", "y"].

                           if expr type cannot be determined >> error string returned
"""
def parse_var_to_lookup(expr):
    lookup = []
    expr_type = parse_expr_to_type(expr)
    if expr_type=="<val>":
        #invaid val
        if not(val_valid(expr)):
            print("ERROR: <val> type contains \" and digits in "+expr)
            sys.exit(0)
        #string_literal
        if expr.find("\"")!=-1:
            if expr[0]=="\"" and expr[-1]=="\"":
                return lookup
            else:
                print("ERROR: string literal not in correct format: "+expr)
                sys.exit(0)
        #int
        if all(char.isdigit() for char in expr):
            return lookup
        #bool
        if expr=="true" or expr=="false":
            return lookup
        #var_name
        if var_valid(expr):
            lookup.append(expr)
            return lookup
        else:
            print("ERROR:",expr,"is not a valid variable name.")
            sys.exit(0)
    elif expr_type == "<comp_expr>":
        to_add = parse_var_to_lookup_helper(expr,["==",  "/=",  ">=", "<=", "<<", ">>"]) 
        lookup += to_add

    elif expr_type == "<math_expr>":
        to_add = parse_var_to_lookup_helper(expr,["+", "-", "*","/", "%","&&","||"]) 
        lookup += to_add 
    # error case
    else: 
        print("ERROR: Ran into an unknown error with expression: "+expr)
        sys.exit(0)
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

value = "xyz", type = "str_literal" 
<int> | <bool> | <str_literal>
"""

def operator_expr_exec(expr,lookup_dict,ops,is_comp):
    for op in ops:
        if expr.find(op)!=-1:
            expr = expr.split(op)
            left = expr[0]
            right = expr[1]
            # if left not string literal, int or bool
            if is_var(left):
                if var_valid(left):
                    if left in lookup_dict:
                        left = lookup_dict[left].value
                    else:
                        print("ERROR:",left,"has not been defined yet."+"(in "+expr+")")
                        sys.exit(0)
                else:
                    print("ERROR",left,"is not a valid variable name." +"(in "+expr+")")
                    sys.exit(0)
            # left is a string literal
            elif left.find("\"")!=-1:
                if left[0]=="\"" and left[-1]=="\"":
                    left = left.strip("\"")
                else:
                    print("ERROR: string literal not in correct format: "+left +" in "+expr)
                    sys.exit(0)
            # left is an int
            elif all(char.isdigit() for char in left):
                left = int(left)
            # left is a bool
            elif left=="true":
                left = True
            elif left=="false":
                left = False
            else:
                print("ERROR: Trouble parsing "+left+ " in "+expr)
                sys.exit(0)
            # if right not string literal, int or bool
            if is_var(right):
                if var_valid(right):
                    if right in lookup_dict:
                        right = lookup_dict[right].value
                    else:
                        print("ERROR:",right,"has not been defined yet."+"(in "+expr+")")
                        sys.exit(0)
                else:
                    print("ERROR",right,"is not a valid variable name." +"(in "+expr+")")
                    sys.exit(0)
            # right is a string literal
            elif right.find("\"")!=-1:
                if right[0]=="\"" and right[-1]=="\"":
                    right = right.strip("\"")
                else:
                    print("ERROR: string literal not in correct format: "+right +" in "+expr)
                    sys.exit(0)
            # right is an int
            elif all(char.isdigit() for char in right):
                right = int(right)
            # right is a bool
            elif right=="true":
                right = True
            elif right=="false":
                right = False
            else:
                print("ERROR: Trouble parsing "+right+ " in >>"+expr+"<<.")
                sys.exit(0)
            # HERE IS WHERE MATH EXPR AND COMP EXPR PARSE BRANCHES
            # different checking if math expr
            if not(is_comp):
                if type(left)!=type(right):
                    print("ERROR: Types on both sides of the operator are not the same in expr>>",expr+"<<.")
                    sys.exit(0)
                #types on both sides are equal

                #str operations
                if type(left)==str:
                    if op!="+":
                        print("ERROR: Cannot perform",op,"operation between strings",left,"and",right+".")
                        sys.exit(0)
                    return left+right
                    
                #bool operation
                #["&&","||"]
                elif type(left)==bool:
                    if op=="&&":
                        return (left and right)
                    elif op=="||":
                        return (left or right)
                    else:
                        print("ERROR: Cannot perform",op,"operation between booleans",left,"and",right+".")
                        sys.exit(0)
                #int operation
                #["+", "-", "*","/", "%"]
                #assuming types of left and right are int
                else:
                    if op=="+":
                        return left+right
                    elif op=="-":
                        return left-right
                    elif op=="*":
                        return left*right
                    elif op=="/":
                        return left/right
                    elif op=="%":
                        return left%right
                    else:
                        print("ERROR: Cannot perform",op,"operation between integers",left,"and",right+".")
                        sys.exit(0)

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
                    print("ERROR: Values",left,"and",right,"cannot be compared using comparison operators in",expr+".")
                    sys.exit(0)

            

def exec_expr(expr,lookup_dict):
    expr_type = parse_expr_to_type(expr)
    if expr_type=="<val>":
        #invalid val
        if not(val_valid(expr)):
            print("ERROR: <val> type contains \" and digits in "+expr)
            sys.exit(0)
        #string_literal
        if expr.find("\"")!=-1:
            if expr[0]=="\"" and expr[-1]=="\"":
                return Value(expr.strip("\""),"str_literal")
            else:
                print("ERROR: string literal not in correct format: "+expr)
                sys.exit(0)
        #int
        if all(char.isdigit() for char in expr):
            return Value(int(expr),"int")
        #bool
        if expr=="true" or expr=="false":
            if(expr=="true"):
                return Value(True,"bool")
            else:
                return Value(False,"bool")
        #var_name
        if var_valid(expr):
            if expr in lookup_dict:
                return lookup_dict[expr]
            else:
                print("ERROR:",expr,"has not been defined yet.")
                sys.exit(0)
        else:
            print("ERROR:",expr,"is not a valid variable name.")
            sys.exit(0)

    elif expr_type == "<comp_expr>":
        vars = parse_var_to_lookup(expr)
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",var,"has not been defined yet.")
                sys.exit(0)
        return Value(operator_expr_exec(expr,lookup_dict,["==",  "/=",  ">=", "<=", "<<", ">>"],True),"bool")
        
        

    elif expr_type == "<math_expr>":
        vars = parse_var_to_lookup(expr)
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",var,"has not been defined yet.")
                sys.exit(0)
        ret_val = operator_expr_exec(expr,lookup_dict,["==",  "/=",  ">=", "<=", "<<", ">>"],False)
        if type(ret_val)==str:
            return Value(ret_val.strip("\""),"str_literal")
        elif type(ret_val)==bool:
            return Value(ret_val,"bool")
        #assuming int
        else:
            return Value(ret_val,"int")
        #check the type of the return value, then return a value type
    # error case
    else: 
        print("ERROR: Ran into an unknown error with expression: "+expr)
        sys.exit(0)

"""
expr.py:
convert_to_python(expr): INPUTS an EXPR, and returns a string of python code that will evaluate the expression.
                         This is for when we run in compiler mode.
                         This is for when we run in compiler mode.
"""
def convert_to_python(expr):
    expr_type = parse_expr_to_type(expr)
    if expr_type=="<val>":
        #invalid val
        if not(val_valid(expr)):
            print("ERROR: <val> type contains \" and digits in "+expr)
            sys.exit(0)
        #string_literal
        if expr.find("\"")!=-1:
            if expr[0]=="\"" and expr[-1]=="\"":
                return Value(expr.strip("\""),"str_literal")
            else:
                print("ERROR: string literal not in correct format: "+expr)
                sys.exit(0)
        #int
        if all(char.isdigit() for char in expr):
            return Value(int(expr),"int")
        #bool
        if expr=="true" or expr=="false":
            if(expr=="true"):
                return Value(True,"bool")
            else:
                return Value(False,"bool")
        #var_name
        if var_valid(expr):
            if expr in lookup_dict:
                return lookup_dict[expr]
            else:
                print("ERROR:",expr,"has not been defined yet.")
                sys.exit(0)
        else:
            print("ERROR:",expr,"is not a valid variable name.")
            sys.exit(0)

    elif expr_type == "<comp_expr>":
        vars = parse_var_to_lookup(expr)
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",var,"has not been defined yet.")
                sys.exit(0)
        return Value(operator_expr_exec(expr,lookup_dict,["==",  "/=",  ">=", "<=", "<<", ">>"],True),"bool")
        
        

    elif expr_type == "<math_expr>":
        vars = parse_var_to_lookup(expr)
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",var,"has not been defined yet.")
                sys.exit(0)
        ret_val = operator_expr_exec(expr,lookup_dict,["==",  "/=",  ">=", "<=", "<<", ">>"],False)
        if type(ret_val)==str:
            return Value(ret_val.strip("\""),"str_literal")
        elif type(ret_val)==bool:
            return Value(ret_val,"bool")
        #assuming int
        else:
            return Value(ret_val,"int")
        #check the type of the return value, then return a value type
    # error case
    else: 
        print("ERROR: Ran into an unknown error with expression: "+expr)
        sys.exit(0)