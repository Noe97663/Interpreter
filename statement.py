import sys
from parserX import *
from expr import *

global DEBUG
DEBUG = True

def convert_to_python_expr(expr):
    return "<expr>"

def exec_statement(statement, lookup_dict):
    statement_type = parse_statement_to_type(statement)
    if statement_type == "<if_statement>":
        exec_if_statement(statement, lookup_dict)
    elif statement_type == "<while_statement>":
        exec_while_statement(statement, lookup_dict)
    elif statement_type == "<print_statement>":
        exec_print_statement(statement, lookup_dict)
    elif statement_type == "<var_assign>":
        exec_var_assign(statement, lookup_dict)
    else:
        print("ERROR: unknown statement type")
        print(statement)
        sys.exit()

def convert_to_python(statement, indent=0):
    statement_type = parse_statement_to_type(statement)
    if statement_type == "<if_statement>":
        return convert_if_statement(statement, indent)
    elif statement_type == "<while_statement>":
        return convert_while_statement(statement, indent)
    elif statement_type == "<print_statement>":
        return convert_print_statement(statement, indent)
    elif statement_type == "<var_assign>":
        return convert_var_assign(statement, indent)
    else:
        print("ERROR: unknown statement type")
        print(statement)
        sys.exit()

    
def exec_if_statement(if_statement, lookup_dict):
    # parse the if statement into its components
    expr, if_block, else_block = parse_if_statement(if_statement)
    # evaluate the expression
    result = exec_expr(expr, lookup_dict)
    if result.type == "<bool>":
        if result.value == True:
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

def convert_if_statement(if_statement, indent):
    # parse the if statement into its components
    python_code = ""
    expr, if_block, else_block = parse_if_statement(if_statement)
    expr_py = convert_to_python_expr(expr)
    python_code += " "*indent + "if " + expr_py + ":\n"
    # convert the if block
    to_convert = parse_block_to_statements(if_block)
    for statement in to_convert:
        python_code += convert_to_python(statement, indent+4)
    # convert the else block
    if else_block is None:
        return python_code
    else:
        python_code += " "*indent + "else:\n"
        to_convert = parse_block_to_statements(else_block)
        for statement in to_convert:
            python_code += convert_to_python(statement, indent+4)
        return python_code


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
    if result.type == "<bool>":
        if result.value == True:
            to_exec = parse_block_to_statements(block)
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
            exec_while_statement(while_statement, lookup_dict)

def convert_while_statement(while_statement, indent):
    python_code = ""
    expr, block = parse_while_statement(while_statement)
    expr_py = convert_to_python_expr(expr)
    python_code += " "*indent + "while " + expr_py + ":\n"
    to_convert = parse_block_to_statements(block)
    for statement in to_convert:
        python_code += convert_to_python(statement, indent+4)
    return python_code

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

def convert_print_statement(print_statement, indent):
    python_code = ""
    print_statement = print_statement[1:-1]
    python_code += " "*indent + "print(" + print_statement + ")\n"
    return python_code

def exec_var_assign(var_assign, lookup_dict):
    # parse the variable assignment into its components
    var_name, expr = parse_var_assign(var_assign)
    # evaluate the expression
    result = exec_expr(expr, lookup_dict)
    # assign the variable
    lookup_dict[var_name] = result
    return None

def convert_var_assign(var_assign, indent):
    python_code = ""
    var_name, expr = parse_var_assign(var_assign)
    expr_py = convert_to_python_expr(expr)
    python_code += " "*indent + var_name + " = " + expr_py + "\n"
    return python_code

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



