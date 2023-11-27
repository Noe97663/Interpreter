"""
INPUTS a LONG string of text and parses it into a list of BLOCKS each block starting with { and ending with }. The blocks can be nested. 
DELETES UNNECESSARY SPACES and NEW LINES.
"""
import sys


def parse_string_to_blocks(string):
    string = string.replace("\n", "")
    ' '.join(string.split())
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
            retval.append(block)
            block = ""
    return retval

"""
INPUTS a BLOCK and parses it into a list of STATEMENTS. In the order they appear in the block. Each statement should end with a ?.
If a block is nested, recurse. We should end up with a list of statements, or a list of lists of statements.
This assumes that block starts with { and ends with }.
"""
def parse_block_to_statements(block):
    block = block.strip()
    block = block[1:-1]
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
        print(statement)
        print(block)
        sys.exit(1)
    if count != 0:
        print("ERROR: incorrect number of '{' or '}' in block")
        print(block)
        sys.exit(1)
    return retval

"""
INPUTS a single STATEMENT, and return the type as a STRING.
Valid types of statements are: "<var_assign>", "<if_statement>", "<while_statement>", "<print_statement>".
Perform error checking HERE (using helpers once the type is detected). CHECK IF ALL THE CHARACTERS ARE LEGAL
ONLY 0-9, a-Z is supported so far.
A statement can be a block (a list of statements), but we don't handle it here. This is only for single statements.
"""
def parse_statement_to_type(statement):
    if "if" in statement:
        return "<if_statement>"
    elif "while" in statement:
        return "<while_statement>"
    elif "!" in statement:
        return "<print_statement>"
    # default to variable assignment
    return "<var_assign>"

"""
<if_statement> ::= if ( <expr> ) <block> <else_clause>? | if (<expr>) <block>?
"""
def if_statement_err_checking(statement):
    if statement[0:2] != "if":
        print("ERROR: if statement should start with 'if'")
        print(statement)
        return False
    if statement[-1] != "?":
        print("ERROR: if statement should end with '?'")
        print(statement)
        return False
    return True

def while_statement_err_checking(statement):
    if statement[0:5] != "while":
        print("ERROR: while statement should start with 'while'")
        print(statement)
        return False
    if statement[-1] != "?":
        print("ERROR: while statement should end with '?'")
        print(statement)
        return False
    return True

def print_statement_err_checking(statement):
    if statement[0] != "!":
        print("ERROR: print statement should start with '!'")
        print(statement)
        return False
    if statement[-1] != "?":
        print("ERROR: print statement should end with '?'")
        print(statement)
        return False
    return True

def var_assign_err_checking(statement):
    if statement[-1] != "?":
        print("ERROR: variable assignment statement should end with '?'")
        print(statement)
        return False
    # check if equals sign is present
    if "=" not in statement:
        print("ERROR: variable assignment statement should contain '='")
        print(statement)
        return False
    # check if type is valid
    if ["int", "bool", "str"].count(statement.split()[0]) == 0:
        print("ERROR: variable assignment statement should contain a valid type")
        print(statement)
        print(statement.split()[0] + " is not a valid type")
        return False
    # check if variable name is valid
    if statement.split()[1].isalnum() == False:
        print("ERROR: variable assignment statement should contain a valid variable name")
        print(statement)
        print(statement.split()[1] + " is not a valid variable name. Only alphanumeric characters are allowed.")
        return False
    return True