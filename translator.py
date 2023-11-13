class variable:
    def __init__(self, name, value, scope):
        self.name = name
        self.value = value
        """if 
        self.type = """
        self.scope = scope

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