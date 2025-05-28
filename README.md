Link to Project Presentation: [youtu.be/7cr2uXpp6NQ](https://www.youtube.com/watch?v=7cr2uXpp6NQ)

# Interpreter
How to use:
usage: translator.py [-h] (-t FILENAME | -i [FILENAME]) [-d] [args ...]

TRANSLATE A FILE:
python translator.py -t FILENAME 
python translator.py -t FILENAME > output.py (do this to save the translated code)

When using > to save the translated code to a file, if the original code has mistakes
the error messages are saved to the file. So, make sure that before you save the code to a 
file, you translate it normally to check for any mistakes.

INTERPRETOR MODE:
python translator.py -i FILENAME (This is the line by line interpreter)
python translator.py -i (This is the interactive interpeter)

When a file name is specified for interpretor mode, the interpretor will run that file line by line.

You can add a -d flag to see parsing/debug information for both MODES. Don't do this if you want to run
the translated code. This is the explicit parsing additional feature.
python translator.py -t FILENAME -d
python translator.py -i -d

You can add additional arguments at the end. Each argument will be stored as
variable arga, argb, argc ...

Example programs:
test_cases[n].txt -- n ranges from 1 to 4 and demonstrate language syntax.
triangle.txt
-- Given the length of three sides of a triangle, determine whether the triangle is a valid triangle using
-- the triangle inequality theorem.
-- Calculate the perimeter.

Example use (depends on local installation - python3 or python): 

python3 translator.py -t example_program/triangle.txt 2 3 4
(or)
python translator.py -t example_program/triangle.txt 2 3 4



Error checking:
Running files in err_testcases provide examples of syntax and type checking.


reserved keywords - true, false, while, if, else

If you use reserved keywords as variable names you will run into unpredictable behaviour.

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

Additional features:

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
