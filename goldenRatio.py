import os, sys
from sympy import sympify, symbols

r = 0.382
tableRows = []


def printError(msg, lno):
  print(f"Error: {msg}")
  input()
  sys.stdout.write(("\033[F\033[K")*lno)
  sys.stdout.flush()


def Expr(eval):
  x = symbols('x')
  expr = sympify(expression)
  res = expr.subs(x, eval)
  return res


# Setting up Golden ratio parameters
def Setup():
  global a, b, n, expression

  # expression input (sympify: used to convert str to math expression)
  while(1):
    try:
      print("Please enter the expression")
      expression = str(input("> exp: "))
      test_expr = expression.replace("x", "1")

      if('x' in expression):
        if(sympify(test_expr).is_real != None):
          break
        else:
          printError("Please enter a correct expression!", 4)

      else:
        printError("Please enter a correct expression that includes 'x' ", 4)
        pass
    except:
      printError("Unexpected error. Please try again.", 5)

  # intervales input
  while(1):
    try:
      print("\nPlease enter the intervals (a, b)")
      a = sympify(input("> a: "))
      b = sympify(input("> b: "))
      if(b > a):
        break
      else:
        printError(f"Interval 'a' cannot be greater than 'b'! ({a},{b})", 6)
    except:
      printError("Please enter a correct number!", 6)

  # number of steps input
  while(1):
    try:
      print("\nPlease enter the number of steps")
      n = int(input("> n: "))
      if(n > 0):
        break
      else:
        printError(f"Number of steps 'n' cannot be less than 0!", 5)
    except:
      printError("Please enter a correct number!", 5)


# Calculate expressions
def Calculate(a, b, n):
  global rba, xk, direction

  for _ in range(n):
    rba = r * (b - a)
    xk = (a+b)/2
    c = a + rba
    d = b - rba
    
    if(Expr(a) > Expr(b)):
      direction = "f(c) > f(d)"
      row = "{:.3f}".format(a) + "\t" + "{:.3f}".format(b) + "\t" + "{:.3f}".format(c) + "\t" + "{:.3f}".format(d) + "\t" + "{:.3f}".format(rba) + "\t" + "{:.3f}".format(xk) + "\t" + str(direction)
      a = c
      c = d
    else:
      direction = "f(c) < f(d)"
      row = "{:.3f}".format(a) + "\t" + "{:.3f}".format(b) + "\t" + "{:.3f}".format(c) + "\t" + "{:.3f}".format(d) + "\t" + "{:.3f}".format(rba) + "\t" + "{:.3f}".format(xk) + "\t" + str(direction)
      b = d
      d = c

    tableRows.append(row)


# Print the headers & rows in a table form
def PrintTable():
  headers = 'a\t' + 'b\t' + 'c\t' + 'd\t' + 'r(b-a)\t' + 'x_k\t' + 'direction'
  print(f"\n{headers}")

  for row in tableRows:
      print(f"{row}")


class main:
  def __init__(self):
    try:
      os.system('cls')
      print(f"\n{'-'*8} GOLDEN RATIO {'-'*8}\n")   # HEADER
      Setup()
      Calculate(a, b, n) 
      PrintTable()
    except:
      print("Warning: Something went wrong")

main()