from parserX import *
from statement import *
from variable import *
#open test_case1.txt, and save the entire file as a string

DEBUG = True

input_file = open("test_case3.txt", "r")
input_string = input_file.read()
input_file.close()

print(input_string)

lookup_dict = {'x' : Value(3, "<int>")}
output = parse_string_to_blocks(input_string, debug=True)
for block in output:
    temp = parse_block_to_statements(block, debug=True)
    print("Statements in block:")
    print(temp)
    print()
    python = ""
    for statement in temp:
        python += convert_to_python(statement)
    
    print("Python statements:")
    print(python)