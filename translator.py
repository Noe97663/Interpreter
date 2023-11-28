import argparse
import os
import sys
import parserX
import statement
import variable

global DEBUG
DEBUG = False

"""
This function translates a file to Python code.
"""
def translate_file(filename, lookup_dict, DEBUG = False):
    # open the file
    if not os.path.exists(filename):
        print("ERROR: file '" + filename + "' does not exist")
        sys.exit(1)
    input_file = open(filename, "r")
    input_string = input_file.read()
    input_file.close()

    blocks = parserX.parse_string_to_blocks(input_string)
    if DEBUG:
        print("Successfully opened file '" + filename + "'")
        print(len(blocks), "blocks found:")

    python_code = ""    
    for arg in lookup_dict:
        python_code += arg + " = " + str(lookup_dict[arg]) + "\n"
        
    for block in blocks:
        stmts = parserX.parse_block_to_statements(block)
        for stmt in stmts:
            #NOEL
            python_code += statement.convert_to_python(stmt,lookup_dict)
    print(python_code)
    # Writing the text to a file named output.py
    with open("output.py", "w") as file:
        file.write(python_code)
    print("Text written to output.py successfully!")
    

"""
This function runs the interpreter.
"""
def run_interpreter(file_name, lookup_dict, DEBUG = False):
    if not os.path.exists(file_name):
        print("ERROR: file '" + file_name + "' does not exist")
        sys.exit(1)
    input_file = open(file_name, "r")
    input_string = input_file.read()
    input_file.close()
    blocks = parserX.parse_string_to_blocks(input_string)
    if DEBUG:
        print("Successfully opened file '" + file_name + "'")
        print(len(blocks), "blocks found")
    if len(blocks) > 0:
        print("Running in line by line mode, enter to continue ...")
        input("")
    else:
        print("No blocks found. Are you sure you've correctly formatted your file?")
    to_run = []
    for block in blocks:
        stmts = parserX.parse_block_to_statements(block)
        if stmts is not None:
            for stmt in stmts:
                to_run.append(stmt)
    while len(to_run) > 0:
        stmt = to_run.pop(0)
        print(">>" + stmt)
        statement.exec_statement(stmt, lookup_dict)
        if DEBUG:
            print()
            print("Lookup dict:")
            lookup_dict_str = ""
            for key in lookup_dict:
                lookup_dict_str += key + ": " + str(lookup_dict[key]) + ", "
            print(lookup_dict_str[:-2])
        input("")

    print("Done executing file '" + file_name + "'")
    print("Transitioning to interactive mode ...")
    run_interpreter_interactive(lookup_dict)

"""
This function runs the interpreter in interactive mode.
"""
def run_interpreter_interactive(lookup_dict):
    print("Running in interactive mode ... 'exit?' to exit")
    print("{")
    statement_buffer = ""
    while True:
        stmt = input(">> ")
        if stmt == "exit?":
            print("}")
            sys.exit()
        stmt = stmt.strip()
        stmt = stmt.replace("\n", "")
        if len(stmt) > 0 and stmt[-1] == "?":
            statement_buffer += stmt
            statement.exec_statement(statement_buffer, lookup_dict)
            statement_buffer = ""
            if DEBUG:
                print()
                print("Lookup dict:")
                lookup_dict_str = ""
                for key in lookup_dict:
                    lookup_dict_str += key + ": " + str(lookup_dict[key]) + ", "
                print(lookup_dict_str[:-2])
        else:
            statement_buffer += stmt
        

"""
This is the main function. It parses the arguments and calls the appropriate functions.
"""
def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Custom Code to Python Translator/Interpreter")

    # Define the flags
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--translate', type=str, metavar='FILENAME', help='Translate a file to Python')
    group.add_argument('-i', '--interpreter', nargs='?', const="NO_FILE", type=str, metavar='FILENAME', help='Run in interpreter mode, optionally with a file')
    parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode')

    # Add an argument for arbitrary number of positional arguments
    parser.add_argument('args', nargs='*', help='Additional arguments to pass to the program')

    # Parse the arguments
    args = parser.parse_args()

    DEBUG = args.debug
    statement.DEBUG = args.debug
    statement.expr_module.DEBUG = args.debug
    parserX.DEBUG = args.debug
    if DEBUG:
        print("DEBUG MODE ON")

    # Map positional arguments to a dictionary
    lookup_dict = {}
    if len(args.args) > 0 and DEBUG:
        print("Additional arguments passed in:")
    for i, arg in enumerate(args.args):
        # arg names are arga, argb, argc, etc.
        var_name = "arg" + chr(ord('a') + i)
        if arg.isnumeric():
            lookup_dict[var_name] = variable.Value(int(arg), "int")
        elif arg == "true":
            lookup_dict[var_name] = variable.Value(True, "bool")
        elif arg == "false":
            lookup_dict[var_name] = variable.Value(False, "bool")
        else:
            lookup_dict[var_name] = variable.Value(arg, "str")
        if DEBUG:
            print("arg:", var_name, "value:", lookup_dict[var_name], "type:", lookup_dict[var_name].type)
    # Implement the logic based on the arguments
    if args.translate:
        translate_file(args.translate, lookup_dict, DEBUG = args.debug)
    elif args.interpreter:
        if args.interpreter == "NO_FILE":
            run_interpreter_interactive(lookup_dict)
        else:
            run_interpreter(args.interpreter, lookup_dict, DEBUG = args.debug)

if __name__ == '__main__':
    main()
