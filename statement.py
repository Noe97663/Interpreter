import sys
from parserX import *

def exec_statement(statement, lookup_dict):
    pass
    # check if statement is an if statement
    if "if" in statement:
        # execute the if statement
        return exec_if_statement(statement, lookup_dict)
    # check if statement is a while statement
    elif "while" in statement:
        # execute the while statement
        return exec_while_statement(statement, lookup_dict)
    # check if statement is a print statement
    elif "!" in statement:
        # execute the print statement
        return exec_print_statement(statement, lookup_dict)
    # default to variable assignment
    else:
        # execute the variable assignment
        return exec_var_assign(statement, lookup_dict)
    
def exec_if_statement(if_statement, lookup_dict):
    pass

"""
if ( <expr> ) <block> <else_clause>? | if (<expr>) <block>?
"""
def parse_if_statement(if_statement, debug=False):
    # parse the if statement into its components
    expr_start = if_statement.find("(")
    expr_end = if_statement.find(")")
    expr = if_statement[expr_start+1:expr_end]

    if_block = ""
    count = 0
    cur = if_statement.find("{")
    for char in if_statement[if_statement.find("{"):]:
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
        if_block += char
        cur += 1
        if count == 0:
            break

    if_statement = if_statement[cur+1:]
    else_block = ""
    if "else" in if_statement:
        count = 1
        cur = if_statement.find("{")
        for char in if_statement[if_statement.find("{"):]:
            if char == "{":
                count += 1
            elif char == "}":
                count -= 1
            else_block += char
            cur += 1
            if count == 0:
                break
    if (debug):
        print("Parsing if statement:")
        print("if_statement: " + if_statement)
        print("expr: " + expr)
        print("if_block: " + if_block)
        print("else_block: " + else_block)
    return expr, if_block, else_block

def exec_while_statement(while_statement, lookup_dict):
    pass

"""
<while_statement> ::= while ( <expr> ) <block>
"""
def parse_while_statement(while_statement, debug=False):
    # parse the while statement into its components
    expr_start = while_statement.find("(")
    expr_end = while_statement.find(")")
    expr = while_statement[expr_start+1:expr_end]

    block = ""
    count = 0
    cur = while_statement.find("{")
    for char in while_statement[while_statement.find("{"):]:
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
        block += char
        cur += 1
        if count == 0:
            break

    if (debug):
        print("Parsing while statement:")
        print("while_statement: " + while_statement)
        print("expr: " + expr)
        print("block: " + block)
    return expr, block

def exec_print_statement(print_statement, lookup_dict):
    print_statement = print_statement[1:-1]
    # determine if the print statement is a string literal or a variable name
    if print_statement[0] == "\"":
        print(print_statement[1:-1])
    else:
        if print_statement not in lookup_dict:
            print("ERROR: variable '" + print_statement + "' not declared")
            sys.exit()
        print(lookup_dict[print_statement])
    return None

        



