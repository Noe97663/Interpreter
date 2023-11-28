# Interpreter

reserved keywords - true, false
CSC 372 Project 2

These are the basic features that the Interpreter handles: 

● integers, Strings, and booleans

● variables that can be integers, Strings, or booleans

● variable assignment

● basic integer expressions with basic operators: addition, subtraction,
  multiplication, division, modulus
  
● boolean expressions with basic operators: and, not, or

● comparison operators: greater than, less than, equal to

● conditionals: should allow for nesting

● loops: at least one kind of loop; should allow for nesting; should allow for blocks

● printing to output

● command line arguments

Additional features being worked on include:

--Implement an interactive system that allows the user to type in commands in your
  language and see the results. Please note that this would not replace the
  requirement that the translator can translate a full program from a file. (Line by line interpretation)
  
--Implement the translator as an interpreter-like translator instead of a compiler-like
  translator. This is likely to be more difficult due to blocks being allowed inside
  loops. This would vary from the basic requirements in that instead of creating a
  translation file, the translator would translate and run the code line by line. (Line by line interpretation)
  
--Add a typing system.

--Add additional or more explicit error handling–i.e. more informative error
  messages, additional types of errors, etc.
  
--Implement the parser without using regular expressions. (Instead, you would
  likely need to implement your own pattern matching.)
  
--Add an optional feature that explicitly shows the parsing process.

--Add a scoping system.

How to use:
usage: python translator.py [-h] (-t FILENAME | -i) [-d] [args ...]

TRANSLATE A FILE:
python translator.py -t FILENAME 

INTERPRETOR MODE:
python translator.py -i

You can add a -d flag to see parsing/debug information for both MODES.
You can add additional arguments at the end. Each argument will be stored as
variable arga, argb, argc ...

Example programs:
triangle.txt
-- Given the length of three sides of a triangle, determine whether the triangle is a valid triangle using
-- the triangle inequality theorem.
-- Calculate the perimeter.
Example use: python3 translator.py -t example_program/triangle.txt 2 3 4