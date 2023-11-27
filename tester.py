from parserX import *
from statement import *
#open test_case1.txt, and save the entire file as a string

input_file = open("test_case4.txt", "r")
input_string = input_file.read()
input_file.close()

print(input_string)

output = parse_string_to_blocks(input_string, debug=True)
for block in output:
    temp = parse_block_to_statements(block, debug=True)
    print(temp)
    x,y,z = parse_if_statement(temp[1])
    print(x)
    print(y)
    print(z)