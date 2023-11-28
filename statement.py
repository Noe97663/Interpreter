import sys
from parserX import *
import expr as expr_module
global DEBUG
DEBUG = False

"""
This function is given a statement. It identifies the type of statement and
calls the appropriate function to execute the statement.
"""
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
        return

"""
This function is given a statement. It identifies the type of statement and
calls the appropriate function to convert the statement to Python code.
"""
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
        print("ERROR: " + statement)
        sys.exit()


"""
This function is given an if statement. It checks for errors in the if statement.
If there are no errors, the statement is executed.
"""
def exec_if_statement(if_statement, lookup_dict):
    if_statement = if_statement.strip()
    if(if_statement_err_checking(if_statement) == False):
        return
    # parse the if statement into its components
    expr, if_block, else_block = parse_if_statement(if_statement)
    if expr is None:
        print("ERROR: cannot parse if statement expression")
        print("ERROR: " + if_statement)
        return
    if if_block is None:
        print("ERROR: cannot parse if statement if block")
        print("ERROR: " + if_statement)
        return
    
    if (DEBUG):
        print("Parsing if statement:")
        print("if_statement: " + if_statement)
        print("expr: " + expr)
        print("if_block: " + if_block)
        print("else_block: " + else_block)
    # evaluate the expression
    result = expr_module.exec_expr(expr, lookup_dict)
    if result is None:
        return
    if (DEBUG):
        print("expr result: " + str(result))
    if result.type == "bool":
        if result.value == True:
            if (DEBUG):
                print("Executing if block")
                print(">>>>>>>>>>>>>>")
            # execute the if block
            to_exec = parse_block_to_statements(if_block)
            if to_exec == None:
                return
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
        else:
            # execute the else block
            if else_block is None:
                print("No else block found. Continuing ...")
                return
            if (DEBUG):
                print("Executing else block")
                print(">>>>>>>>>>>>>>")
            to_exec = parse_block_to_statements(else_block)
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
    else:
        print("ERROR: if statement expression should evaluate to a boolean")
        print("ERROR: " + if_statement)

"""
This function is given an if statement. It checks for errors in the if statement.
If there are no errors, the statement is converted to Python code. If there are
errors, the program exits.
"""
def convert_if_statement(if_statement, lookup_dict, indent):
    if_statement = if_statement.strip()
    if(if_statement_err_checking(if_statement) == False):
        sys.exit()
    # parse the if statement into its components
    python_code = ""
    expr, if_block, else_block = parse_if_statement(if_statement)
    if expr is None:
        print("ERROR: cannot parse if statement expression")
        print("ERROR: " + if_statement)
        sys.exit()
    if if_block is None:
        print("ERROR: cannot parse if statement if block")
        print("ERROR: " + if_statement)
        sys.exit()

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
    if to_convert == None:
        sys.exit()
    for statement in to_convert:
        python_code += convert_to_python(statement,lookup_dict, indent+4)
    # convert the else block
    if else_block.strip() == "":
        return python_code
    else:
        python_code += " "*indent + "else:\n"
        to_convert = parse_block_to_statements(else_block)
        if to_convert == None:
            sys.exit()
        for statement in to_convert:
            python_code += convert_to_python(statement,lookup_dict, indent+4)
        return python_code


"""
This function is given an if statement. It parses the if statement into its
components and returns the components. Performs error checking.
"""
def parse_if_statement(if_statement):
    # parse the if statement into its components
    expr_start = if_statement.find("(")
    expr_end = if_statement.find(")")
    expr_start_count = if_statement.count("(")
    expr_end_count = if_statement.count(")")
    if expr_start_count != expr_end_count:
        print("ERROR: mismatched parentheses in if statement")
        return None, None, None
    if expr_start == -1 or expr_end == -1:
        return None, None, None
    # parse the expression
    expr = if_statement[expr_start+1:expr_end]

    # parse the if block
    if_block = ""
    count = 0
    cur = if_statement.find("{")
    if cur == -1:
        return "", None, None
    for char in if_statement[if_statement.find("{"):]:
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
        if_block += char
        cur += 1
        if count == 0:
            break

    # parse the else block
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

"""
This function is given a while statement. It checks for errors in the while statement.
If there are no errors, the statement is executed.
"""
def exec_while_statement(while_statement, lookup_dict):
    while_statement = while_statement.strip()
    if (while_statement_err_checking(while_statement) == False):
        return None
    expr, block = parse_while_statement(while_statement)
    if expr is None:
        print("ERROR: cannot parse while statement expression")
        print("ERROR: " + while_statement)
        return None
    if block is None:
        print("ERROR: cannot parse while statement block")
        print("ERROR: " + while_statement)
        return None
    
    if (DEBUG):
        print("Parsing while statement:")
        print("while_statement: " + while_statement)
        print("expr: " + expr)
        print("block: " + block)
        print()
    result = expr_module.exec_expr(expr, lookup_dict)
    if result is None:
        return None
    if result.type == "bool":
        if result.value == True:
            to_exec = parse_block_to_statements(block)
            if to_exec == None:
                return None
            for statement in to_exec:
                exec_statement(statement, lookup_dict)
            exec_while_statement(while_statement, lookup_dict)
        else:
            if (DEBUG):
                print("While statement expression evaluated to False. Continuing ...")
    else:
        print("ERROR: while statement expression should evaluate to a boolean")
        print("ERROR: " + while_statement)

"""
This function is given a while statement. It checks for errors in the while statement.
If there are no errors, the statement is converted to Python code. If there are
errors, the program exits.
"""
def convert_while_statement(while_statement, lookup_dict, indent):
    while_statement = while_statement.strip()
    if (while_statement_err_checking(while_statement) == False):
        sys.exit()
    python_code = ""
    expr, block = parse_while_statement(while_statement)
    if expr is None:
        print("ERROR: cannot parse while statement expression")
        print("ERROR: " + while_statement)
        sys.exit()
    if block is None:
        print("ERROR: cannot parse while statement block")
        print("ERROR: " + while_statement)
        sys.exit()
    if (DEBUG):
        print(" "*indent + "Parsing while statement:")
        print(" "*indent + "while_statement: " + while_statement)
        print(" "*indent + "expr: " + expr)
        print(" "*indent + "block: " + block)
        print()
    expr_py = expr_module.convert_to_python(expr, lookup_dict)
    python_code += " "*indent + "while " + expr_py + ":\n"
    to_convert = parse_block_to_statements(block)
    if to_convert == None:
        sys.exit()
    for statement in to_convert:
        python_code += convert_to_python(statement,lookup_dict, indent+4)
    return python_code

"""
This function is given a while statement. It parses the while statement into its
components and returns the components. Performs error checking.
"""
def parse_while_statement(while_statement):
    # parse the while statement into its components
    expr_start = while_statement.find("(")
    expr_end = while_statement.find(")")
    expr_start_count = while_statement.count("(")
    expr_end_count = while_statement.count(")")
    if expr_start_count != expr_end_count:
        print("ERROR: mismatched parentheses in while statement")
        return None, None
    if expr_start == -1 or expr_end == -1:
        return None, None
    expr = while_statement[expr_start+1:expr_end]

    block = ""
    count = 0
    cur = while_statement.find("{")
    if cur == -1:
        return "", None
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

"""
This function is given a print statement. It checks for errors in the print statement.
If there are no errors, the statement is executed.
"""
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
        else:
            print(lookup_dict[print_statement])
    return None

"""
This function is given a print statement. It checks for errors in the print statement.
If there are no errors, the statement is converted to Python code. If there are
errors, the program exits.
"""
def convert_print_statement(print_statement, lookup_dict, indent):
    print_statement = print_statement.strip()
    if (print_statement_err_checking(print_statement) == False):
        sys.exit()
    python_code = ""
    print_statement = print_statement[1:-1]
    if print_statement[0] == "\"":
        python_code += " "*indent + "print(" + print_statement + ")\n"
        return python_code
    else:
        if print_statement not in lookup_dict:
            print("ERROR: variable '" + print_statement + "' not declared")
            sys.exit()
        python_code += " "*indent + "print(" + print_statement + ")\n"
        return python_code

"""
This function is given a variable assignment. It checks for errors in the variable
assignment. If there are no errors, the statement is executed.
"""
def exec_var_assign(var_assign, lookup_dict):
    var_assign = var_assign.strip()
    if (var_assign_err_checking(var_assign) == False):
        return None
    # parse the variable assignment into its components
    type_name, var_name, expr = parse_var_assign(var_assign)
    if (DEBUG):
        print("Parsing variable assignment:")
        print("var_assign: " + var_assign)
        print("type_name: " + type_name)
        print("var_name: " + var_name)
        print("expr: " + expr)
    # evaluate the expression
    result = expr_module.exec_expr(expr, lookup_dict)
    if result is None:
        return None
    if (type_name != result.type):
        print("ERROR: variable type does not match expression type")
        print("ERROR: " + var_name + " has type " + type_name + " but expression has type " + result.type)
        return None
    
    if (DEBUG):
        print("expr result: " + str(result))

    # assign the variable
    lookup_dict[var_name] = result
    return None

"""
This function is given a variable assignment. It checks for errors in the variable
assignment. If there are no errors, the statement is converted to Python code.
If there are errors, the program exits.
"""
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
    if expr_py is None:
        sys.exit()
    python_code += " "*indent + var_name + " = " + expr_py + "\n"
    result = expr_module.exec_expr(expr, lookup_dict)
    if result is None:
        sys.exit()
    if (type_name != result.type):
        print("ERROR: variable type does not match expression type")
        print("ERROR: " + var_name + " has type " + type_name + " but expression has type " + result.type)
        return None
    lookup_dict[var_name] = result
    return python_code

"""
This function is given a statement. It parses the statement into its components
and returns the components. Performs error checking.
"""
def parse_var_assign(var_assign):
    var_assign = var_assign.strip()
    # parse the variable assignment into its components
    left = var_assign[:var_assign.find("=")]
    left = left.split()
    type_name = left[0]
    var_name = left[1]
    expr = var_assign[var_assign.find("=")+1:-1]
    return type_name, var_name, expr



