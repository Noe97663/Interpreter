class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def type(self):
        return self.value.type

"""
possibilities:
value = "xyz", type = "str" 
value = 123, type = "int" 
value = True, type = "bool" 
"""
class Value:
    def __init__(self, value, type):
        self.value = value
        self.type = type
    def __str__(self):
        if self.type=="bool":
            return str(self.value).lower()
        return str(self.value)