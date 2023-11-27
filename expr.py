import sys
from variable import *
"""
expr.py:
convert_to_python(expr): INPUTS an EXPR, and returns a string of python code that will evaluate the expression.
                         This is for when we run in compiler mode.
                         This is for when we run in compiler mode.
"""

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

def comp_expr_exe(expr,lookup_dict):
    for op in ["==",  "/=",  ">=", "<=", "<<", ">>"]:
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
            elif :
            
            """if expr.find("\"")!=-1:
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
            return lookup"""
            # if right not string literal, int or bool
            if (right.find("\"")==-1) and \
            not(all(char.isdigit() for char in right)) and \
            (right!="true" and right!="false"):
                if var_valid(right):
                    ret_val.append(right) 
                else:
                    print("ERROR:", right,"is not a valid variable name.")
                    sys.exit(0)
            return ret_val

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
                return Value(expr,"str_literal")
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
        else:
            print("ERROR:",expr,"is not a valid variable name.")
            sys.exit(0)

    elif expr_type == "<comp_expr>":
        vars = parse_var_to_lookup(expr)
        for var in vars:
            if var not in lookup_dict:
                print("ERROR:",var,"has not been defined yet.")
        return Value(comp_expr_exec(expr,lookup_dict),"bool")
        
        

    elif expr_type == "<math_expr>":
        to_add = parse_var_to_lookup_helper(expr,["+", "-", "*","/", "%","&&","||"]) 
        lookup += to_add 
    # error case
    else: 
        print("ERROR: Ran into an unknown error with expression: "+expr)
    return lookup

def convert_to_python(expr):
    pass