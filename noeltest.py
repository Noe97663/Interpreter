from expr import *

expr="asda23s"
print(parse_var_to_lookup(expr))
expr = "x+3"
print(parse_var_to_lookup(expr))
expr = "x>>t"
print(parse_var_to_lookup(expr))
expr = "t&&x"
print(parse_var_to_lookup(expr))
expr = "1222>&&=="
print(parse_var_to_lookup(expr))