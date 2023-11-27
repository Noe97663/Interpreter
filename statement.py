import sys
from parserX import *
import expr as expr_module
global DEBUG
DEBUG = False

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

def convert_to_python(statement, lookup_dict, indent=0):
    statement_type = parse_statement_to_type(statement)
    if statement_type == "<if_statement>":
        return convert_if_statement(statement, lookup_dict, indent)
    elif statement_type == "<while_statement>":
        return convert_while_statement(statement, lookup_dict, indent)
    elif statement_type == "<print_statement>":
        return convert_print_statement(statement, lookup_dict, indent)
    elif statement_type == "<var_assign>":
        return convert_var_assign(statement, lookup_dict, indent)
    else:
        print("ERROR: unknown statement type")
        print(statement)
        sys.exit()

    
def exec_if_statement(if_statement, lookup_dict):
    if_statement = if_statement.strip()
    if(if_statement_err_checking(if_statement) == False):
        return
    # parse the if statement into its components
    expr, if_block, else_block = parse_if_statement(if_statement)
    # evaluate the expression
    result = expr_module.exec_expr(expr, lookup_dict)
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

def convert_if_statement(if_statement, lookup_dict, indent):
    if_statement = if_statement.strip()
    if(if_statement_err_checking(if_statement) == False):
        sys.exit()
    # parse the if statement into its components
    python_code = ""
    expr, if_block, else_block = parse_if_statement(if_statement)
    if (DEBUG):
        print(" "*indent + "Parsing if statement:")
        print(" "*indent + "if_statement: " + if_statement)
        print(" "*indent + "expr: " + expr)
        print(" "*indent + "if_block: " + if_block)
        print(" "*indent + "else_block: " + else_block)
        print()
    
    expr_py = expr_module.convert_to_python(expr, lookup_dict)
    python_code += " "*indent + "if " + expr_py + ":\n"
    # convert the if block
    to_convert = parse_block_to_statements(if_block)
    for statement in to_convert:
        python_code += convert_to_python(statement,lookup_dict, indent+4)
    # convert the else block
    if else_block.strip() == "":
        return python_code
    else:
        python_code += " "*indent + "else:\n"
        to_convert = parse_block_to_statements(else_block)
        for statement in to_convert:
            python_code += convert_to_python(statement,lookup_dict, indent+4)
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

    if_statement2 = if_statement[cur+1:]
    else_block = ""
    if "else" in if_statement2:
        count = 0
        cur = if_statement2.find("{")
        for char in if_statement2[if_statement2.find("{"):]:
            if char == "{":
                count += 1
            elif char == "}":
                count -= 1
            else_block += char
            cur += 1
            if count == 0:
                break

    return expr, if_block, else_block

def exec_while_statement(while_statement, lookup_dict):
    while_statement = while_statement.strip()
    if (while_statement_err_checking(while_statement) == False):
        return None
    expr, block = parse_while_statement(while_statement)
    result = expr_module.exec_expr(expr, lookup_dict)
    if result.type == "<bool>":
        if result.value == True:
            to_exec = parse_block_to_statements(block)
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
            exec_while_statement(while_statement, lookup_dict)

def convert_while_statement(while_statement, lookup_dict, indent):
    while_statement = while_statement.strip()
    if (while_statement_err_checking(while_statement) == False):
        sys.exit()
    python_code = ""
    expr, block = parse_while_statement(while_statement)
    if (DEBUG):
        print(" "*indent + "Parsing while statement:")
        print(" "*indent + "while_statement: " + while_statement)
        print(" "*indent + "expr: " + expr)
        print(" "*indent + "block: " + block)
        print()
    expr_py = expr_module.convert_to_python(expr, lookup_dict)
    python_code += " "*indent + "while " + expr_py + ":\n"
    to_convert = parse_block_to_statements(block)
    for statement in to_convert:
        python_code += convert_to_python(statement,lookup_dict, indent+4)
    return python_code

"""
<while_statement> ::= while ( <expr> ) <block>
"""
def parse_while_statement(while_statement):
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
    return expr, block

def exec_print_statement(print_statement, lookup_dict):
    print_statement = print_statement.strip()
    if (print_statement_err_checking(print_statement) == False):
        return None
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

def convert_print_statement(print_statement, lookup_dict, indent):
    print_statement = print_statement.strip()
    if (print_statement_err_checking(print_statement) == False):
        sys.exit()
    python_code = ""
    print_statement = print_statement[1:-1]
    python_code += " "*indent + "print(" + print_statement + ")\n"
    return python_code

def exec_var_assign(var_assign, lookup_dict):
    var_assign = var_assign.strip()
    if (var_assign_err_checking(var_assign) == False):
        return None
    # parse the variable assignment into its components
    type_name, var_name, expr = parse_var_assign(var_assign)
    # evaluate the expression
    result = expr_module.exec_expr(expr, lookup_dict)
    # assign the variable
    lookup_dict[var_name] = result
    return None

def convert_var_assign(var_assign, lookup_dict, indent):
    var_assign = var_assign.strip()
    if (var_assign_err_checking(var_assign) == False):
        sys.exit()
    python_code = ""
    type_name, var_name, expr = parse_var_assign(var_assign)
    if (DEBUG):
        print(" "*indent + "Parsing variable assignment:")
        print(" "*indent + "var_assign: " + var_assign)
        print(" "*indent + "type_name: " + type_name)
        print(" "*indent + "var_name: " + var_name)
        print(" "*indent + "expr: " + expr)
        print()
    expr_py = expr_module.convert_to_python(expr, lookup_dict)
    python_code += " "*indent + var_name + " = " + expr_py + "\n"
    lookup_dict[var_name] = expr_module.exec_expr(expr,lookup_dict)
    return python_code

def parse_var_assign(var_assign):
    var_assign = var_assign.strip()
    # parse the variable assignment into its components
    left = var_assign[:var_assign.find("=")]
    left = left.split()
    type_name = left[0]
    var_name = left[1]
    expr = var_assign[var_assign.find("=")+1:-1]
    return type_name, var_name, expr



