import sys
from parserX import *
from expr import *

global DEBUG
DEBUG = True

def exec_statement(statement, lookup_dict):
    pass
    # check if statement is an if statement
    if "if" in statement:
        # execute the if statement
        exec_if_statement(statement, lookup_dict)
    # check if statement is a while statement
    elif "while" in statement:
        # execute the while statement
        exec_while_statement(statement, lookup_dict)
    # check if statement is a print statement
    elif "!" in statement:
        # execute the print statement
        exec_print_statement(statement, lookup_dict)
    # default to variable assignment
    else:
        # execute the variable assignment
        exec_var_assign(statement, lookup_dict)
    
def exec_if_statement(if_statement, lookup_dict):
    # parse the if statement into its components
    expr, if_block, else_block = parse_if_statement(if_statement)
    # evaluate the expression
    result = exec_expr(expr, lookup_dict)
    if result.type == "bool":
        if result.value == "true":
            # execute the if block
            to_exec = parse_block_to_statements(if_block)
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
        else:
            # execute the else block
            if else_block is None:
                return
            to_exec = parse_block_to_statements(else_block)
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
"""
if ( <expr> ) <block> <else_clause>? | if (<expr>) <block>?
"""
def parse_if_statement(if_statement):
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
    if (DEBUG):
        print("Parsing if statement:")
        print("if_statement: " + if_statement)
        print("expr: " + expr)
        print("if_block: " + if_block)
        print("else_block: " + else_block)
    return expr, if_block, else_block

def exec_while_statement(while_statement, lookup_dict):
    expr, block = parse_while_statement(while_statement)
    result = exec_expr(expr, lookup_dict)
    if result.type == "bool":
        if result.value == "true":
            to_exec = parse_block_to_statements(block)
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
            exec_while_statement(while_statement, lookup_dict)

"""
<while_statement> ::= while ( <expr> ) <block>
"""
def parse_while_statement(while_statement, DEBUG=False):
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

    if (DEBUG):
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

def exec_var_assign(var_assign, lookup_dict):
    # parse the variable assignment into its components
    var_name, expr = parse_var_assign(var_assign)
    # evaluate the expression
    result = exec_expr(expr, lookup_dict)
    # assign the variable
    lookup_dict[var_name] = result
    return None

def parse_var_assign(var_assign, DEBUG=False):
    # parse the variable assignment into its components
    var_name = var_assign[:var_assign.find("=")]
    expr = var_assign[var_assign.find("=")+1:-1]
    if (DEBUG):
        print("Parsing variable assignment:")
        print("var_assign: " + var_assign)
        print("var_name: " + var_name)
        print("expr: " + expr)
    return var_name, expr



