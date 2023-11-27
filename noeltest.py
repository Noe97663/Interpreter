from expr import *


# TESTS for exec_expr(expr,lookup_dict)











# TESTS for parse_var_to_lookup and parse_expr_to_type (+dependent functions)
expr = "x+3"
print(parse_var_to_lookup(expr))
expr = "x>>t"
print(parse_var_to_lookup(expr))
expr = "t&&x"
print(parse_var_to_lookup(expr))
expr="\"asdas\""
print(parse_var_to_lookup(expr))


#ERROR CASES

#invalid string literal
expr="\"asda\"s"
#print(parse_var_to_lookup(expr))

#invalid val type
expr="\"asda23s"
#print(parse_var_to_lookup(expr))

#invalid variable name
expr="asda23s"
#print(parse_var_to_lookup(expr))

#invalid variable name left
expr = "asdqqex1+3"
print(parse_var_to_lookup(expr))

#invalid variable name right
expr = "asdqqx+asda231s"
#print(parse_var_to_lookup(expr))

#invalid variable name both
expr = "as12dqqx+asda231s"
#print(parse_var_to_lookup(expr))

#both types of ops found in expr
expr = "1222>&&=="
#print(parse_var_to_lookup(expr))