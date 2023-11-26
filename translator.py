#scope_name goes up by 1 whenever new scope is entered (leaving a scope just keeps the earlier scopes name)
#gives each scope a unique name
scope_name = 0
#scope_level goes up by 1 whenever a new scope is entered and goes down by 1 whenever it is exited
#at program end check if scope_level == 0 to verify blocks are closed
scope_level = 0 

# as blocks are entered the scope_name is put at the end
scope_stack = []
# variable dict has variables of the form variable name:variable object
variable_dict = {}
class variable:
    def __init__(self, name, value, scope_name, scope_parents):
        self.name = name
        self.value = value
        # name of the scope 
        self.scope_name = scope_name
        # list of scopes that are parents of this scope, it will be the current scope stack
        self.scope_parents = scope_parents

def processLine(line,vars,scope):
    pass

def main():
    vars ={}
    with open("input.txt", 'r') as file:
        char = file.read(1)

        # if first character is a ?
        if char=="?":
            line=""
        else:
            line += char
        print(line)
        while char:
            char = file.read(1)
            line+=char
            print(line)
            if char==";":
                vars,scope = processLine(line,vars,scope)

            

if (__name__ == "__main__"):
    main()