import sys
"""
expr.py:
exec_expr(expr, lookup_dict): inputs an EXPR, and a dictionary of variables. 
                            Return the value of that expression as a VARIABLE type. Perform error checking here.
                            Check if a variable is not defined. 
                            Check if a variable is not of the right type. Check if the types are right.
                            This is only for when we run in interpreter mode.

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
                if (left.find("\"")==-1) and \
                not(all(char.isdigit() for char in left)) and \
                (left!="true" and left!="false"):
                    if var_valid(left):
                        ret_val.append(left)
                    else:
                        print("ERROR",left,"is not a valid variable name.")
                        sys.exit(0)
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

def exec_expr(expr,lookup_dict):
    pass

def convert_to_python(expr):
    pass