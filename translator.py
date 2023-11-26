"""GLOBAL VARIABLES"""
#scope_name goes up by 1 whenever new scope is entered (leaving a scope just keeps the earlier scopes name)
#gives each scope a unique name, if the scope_stack is empty tho just give scope_name = 0
SCOPE_NAME = 0
#scope_level goes up by 1 whenever a new scope is entered and goes down by 1 whenever it is exited
#at program end check if scope_level == 0 to verify blocks are closed
SCOPE_LEVEL = 0 

# as blocks are entered the scope_name is put at the end
SCOPE_STACK = []
# a dictionary whose key is a scope, and values are the child scopes
SCOPE_DICT = {0:[]}
# var dict has variables of the form variable (scope_name,name):value
# a global var x would be (0,x):12
VAR_DICT = {}

def parse_math_expr(expr, scope_name):
    #check the current scope by peeking the SCOPE_STACK, empty means global

    # you can check if variable names are defined in the scope_name

    # Write a function to collect all the varibales from the variable dict in
    # a given scope, check parent scopes if not found
    # this funciton will see reuse
    pass

def processLine(line):
    original_line = line

    #var assign case
    if line[-1]=="?":
        line = line.split("=")
        if len(line)!=2:
            print("Error parsing variable assignment line:\n")
            print(original_line)
        line = [x.strip() for x in line]
        var_info = line[0].split(" ")
        if len(var_info)!=2:
            print("Error parsing variable assignment line:\n")
            print(original_line)
        var_type,var_name = var_info[0],var_info[1]
        #check var type to determine the value properly
        #check var name
        #check scope name ()
        if SCOPE_STACK==[]:
            scope = 0

        value_info = line[1].strip("?")
        VAR_DICT[(scope,var_name)] = value_info
        print(VAR_DICT)
        return line

#UNUSED
class variable:
    # the type of the variable can be checked by checking
    # the type of the value itself
    def __init__(self, name, value, scope_name):
        self.name = name
        self.value = value
        # name of the scope 
        self.scope_name = scope_name


def main():
    global SCOPE_NAME, SCOPE_LEVEL, SCOPE_STACK,SCOPE_DICT, VAR_DICT

    x=int(input("1 - interpreter\n2 - read and convert input.txt\n"))
    if x==1:
        line =""
        while line!="stop":
            line = input(">>")
            #if a line starts with ? it is a variable search
            if line[0]=="?":
                #check scope
                scope = 0
                print(VAR_DICT[(scope,line[1:])])
            else:
                py_line = processLine(line)
                #exec(py_line)
                print(py_line)
        
    else:
        with open("input.txt", 'r') as file:
            # list of lines that will contain the lines of the python file
            final_py = []
            line=""
            char = file.read(1)
            line+=char
            # FORGOT WHY I DID THIS - if first character is a ?, 
            #if char=="?":
            #    line=""
            #else:
            #    line += char
            print(line)
            while char:
                char = file.read(1)
                #ignore new lines
                if char=="\n":
                    char=""
                line+=char
                print(line)
                # line ends in ?, var assign statement
                if char=="?":
                    py_line = processLine(line)
                    line=""
                    final_py.append(py_line)
                # line ends in block start, loop or conditional
                elif char=="{":
                    py_line = processLine(line)
                    line=""
                    final_py.append(py_line)
                elif char=="}":
                    py_line = processLine(line)
                    line=""
                    final_py.append(py_line)
            if line!="":
                print("Your file ends incorrectly.")
                    

            

if (__name__ == "__main__"):
    main()