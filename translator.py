import argparse
import os
import sys
import parserX
import statement

global DEBUG
DEBUG = False

def translate_file(filename, lookup_dict):
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
    if DEBUG:
        if len(lookup_dict) > 0:
            print("Command line variables passed in:")
    for arg in lookup_dict:
        if DEBUG:
            print("arg:", arg, "value:", lookup_dict[arg])
        python_code += arg + " = " + str(lookup_dict[arg]) + "\n"
        
    for block in blocks:
        stmts = parserX.parse_block_to_statements(block)
        for stmt in stmts:
            python_code += statement.convert_to_python(stmt)
    print(python_code)

def run_interpreter(lookup_dict):
    print("Running in interpreter mode")
    print("{")

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Custom Code to Python Translator/Interpreter")

    # Define the flags
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--translate', type=str, metavar='FILENAME', help='Translate a file to Python')
    group.add_argument('-i', '--interpreter', action='store_true', help='Run in interpreter mode')
    parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode')

    # Add an argument for arbitrary number of positional arguments
    parser.add_argument('args', nargs='*', help='Additional arguments to pass to the program')

    # Parse the arguments
    args = parser.parse_args()

    # Map positional arguments to a dictionary
    lookup_dict = {f'arg{i}': arg for i, arg in enumerate(args.args)}

    DEBUG = args.debug
    statement.DEBUG = args.debug
    parserX.DEBUG = args.debug
    if DEBUG:
        print("DEBUG MODE ON")
    # Implement the logic based on the arguments
    if args.translate:
        translate_file(args.translate, lookup_dict)
    elif args.interpreter:
        run_interpreter(lookup_dict)

if __name__ == '__main__':
    main()
