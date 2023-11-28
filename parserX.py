"""
This file contains functions that parse the input string into blocks, statements, and types.
"""

"""
This function takes in a string and returns a list of blocks.
"""
def parse_string_to_blocks(string):
    string = string.replace("\n", "")
    string = ' '.join(string.split())
    retval = []
    block = ""
    count = 0
    for char in string:
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
        block += char
        if count == 0:
            if (len(block) > 0 and block[0] == "{"):
                retval.append(block)
            block = ""
    return retval

"""
This function takes in a block and returns a list of statements.
"""
def parse_block_to_statements(block):
    block = block.strip()
    block = block[1:-1]
    block = block.strip()
    retval = []
    statement = ""
    count = 0
    for char in block:
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
        statement += char
        if char == "?" and count == 0:
            statement = statement.strip()
            retval.append(statement)
            statement = ""
    if statement != "":
        print("ERROR: statement does not end with '?'")
        print("ERROR: " + statement)
        print("ERROR: " + block)
        return None
    if count != 0:
        print("ERROR: incorrect number of '{' or '}' in block")
        print("ERROR: " + block)
        return None
    return retval

"""
INPUTS a single STATEMENT, and return the type as a STRING.
Valid types of statements are: "<var_assign>", "<if_statement>", "<while_statement>", "<print_statement>".
Perform error checking HERE (using helpers once the type is detected). CHECK IF ALL THE CHARACTERS ARE LEGAL
ONLY 0-9, a-Z is supported so far.
A statement can be a block (a list of statements), but we don't handle it here. This is only for single statements.
"""
def parse_statement_to_type(statement):
    statement = statement.strip()
    if len(statement) <= 1:
        return None
    if statement[0:2] == "if":
        return "<if_statement>"
    if statement[0:5] == "while":
        return "<while_statement>"
    if statement[0] == "!":
        return "<print_statement>"
    if "=" in statement:
        return "<var_assign>"
    else:
        print("ERROR: statement type not recognized")
        print("ERROR: " + statement)
    

"""
This function takes in an if statement and error checks it.
"""
def if_statement_err_checking(statement):
    if statement[0:2] != "if":
        print("ERROR: if statement should start with 'if'")
        print("ERROR: " + statement)
        return False
    if statement[-1] != "?":
        print("ERROR: if statement should end with '?'")
        print("ERROR: " + statement)
        return False
    return True

"""
This function takes in a while statement and error checks it.
"""
def while_statement_err_checking(statement):
    if statement[0:5] != "while":
        print("ERROR: while statement should start with 'while'")
        print("ERROR: " + statement)
        return False
    if statement[-1] != "?":
        print("ERROR: while statement should end with '?'")
        print("ERROR: " + statement)
        return False
    return True

"""
This function takes in a print statement and error checks it.
"""
def print_statement_err_checking(statement):
    if len(statement) <= 2:
        print("ERROR: missing argument in print statement")
        print("ERROR: " + statement)
    if statement[0] != "!":
        print("ERROR: print statement should start with '!'")
        print("ERROR: " + statement)
        return False
    if statement[-1] != "?":
        print("ERROR: print statement should end with '?'")
        print("ERROR: " + statement)
        return False
    return True

"""
This function takes in a variable assignment statement and error checks it.
"""
def var_assign_err_checking(statement):
    if statement[-1] != "?":
        print("ERROR: variable assignment statement should end with '?'")
        print("ERROR: " + statement)
        return False
    # check if equals sign is present
    if "=" not in statement:
        print("ERROR: variable assignment statement should contain '='")
        print("ERROR: " + statement)
        return False
    # check if type is valid
    if ["int", "bool", "str"].count(statement.split()[0]) == 0:
        print("ERROR: variable assignment statement should contain a valid type")
        print("ERROR: " + statement)
        print("ERROR: " + statement.split()[0] + " is not a valid type")
        return False
    # check if variable name is valid
    if statement.split()[1].isalnum() == False:
        print("ERROR: variable assignment statement should contain a valid variable name")
        print("ERROR: " + statement)
        print("ERROR: " + statement.split()[1] + " is not a valid variable name. Only alphanumeric characters are allowed.")
        return False
    return True