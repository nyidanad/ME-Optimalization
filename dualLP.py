import json, random, time, os, sys

primal = {'target': [], 'constraints': [], 'coefficients': []}
dual = {'target': [], 'constraints': [], 'coefficients': []}


with open('dualLP-table.json', 'r') as file:
  table = json.load(file)

def printError(msg):
  input(f"\nError: {msg}")
  sys.stdout.write(("\033[F\033[K")*3)
  sys.stdout.flush()


# Setting up dualLP parameters
def Setup():
  try:
    global direction, var_amount, con_amount

    # direction input
    print("Please enter the direction you want to count on")
    while(1):
      try:
        direction = input("> direction [Min/Max]: ").lower()
        
        if direction in ['min', 'minimize', 'max', 'maximize']:
          direction = direction[:3]
          direction = 'max' if direction == 'min' else 'min'    # inverting direction for coefficients
          break
        else:
          printError("Please enter the correct direction Min or Max!")
      except:
        printError("Something went wrong during direction setup!")

    # vaiables amount input
    print("\nPlease enter the number of variables & constraints")
    while(1):
      try:
        var_amount = int(input("> vars: "))
        if(var_amount > 0):
          break
        else:
          printError("Variables amount cannot be less than 0!")
      except:
        printError("Please enter a valid number!")

    # constraints amount input
    while(1):
      try:
        con_amount = int(input("> cons: "))
        if(con_amount > 0):
          break
        else:
          printError("Constraints amount cannot be less than 0!")
      except:
        printError("Please enter a valid number!")

    print("\n*Setup completed")
  except:
    printError("Something went wrong during setup launch!")


# Generating Primal
def GeneratePrimal():
  try:
    # generate primal target function
    for _ in range(var_amount):
      primal['target'].append(random.randint(-10, 10))
    
    # generate primal constraints
    for i in range(con_amount):
      tmp = {
        'variables': random.sample(range(1, 9), var_amount),
        'operator': random.choice(list(table[direction]['constraints'].keys())),
        'result': random.randint(-10, 25)
      }
      primal['constraints'].append(tmp)

    # generate primal coefficients
    for _ in range(var_amount):
      primal['coefficients'].append(random.choice(list(table[direction]['variables'].keys())))

    time.sleep(1)
    print("*Generation completed")
  except:
    printError("Something went wrong during PRIMAL generation!")


# Calculating Dual
def CalculateDual():
  try:
    # calculating dual target function
    for const in primal['constraints']:
      dual['target'].append(const['result'])

    # calculating dual constraints
    for i in range(var_amount):
      tmp = {
        'variables': [],
        'operator': table[direction]['variables'][primal['coefficients'][i]],
        'result': primal['target'][i]
      }
      for j in range(con_amount):
        tmp['variables'].append(primal['constraints'][j]['variables'][i])
        
      dual['constraints'].append(tmp)

    # calculating dual coefficients
    for const in primal['constraints']:
      dual['coefficients'].append(table[direction]['constraints'][const['operator']])

    time.sleep(1)
    print("*Dual calculation completed")
  except Exception as e:
    printError("Something went wrong during dual calculation!")
    print(str(e))


# Printing the target and constraints
def Print(data: dict, target: str):
  try:
    tmp = []
    symbol = 'x' if target == 'primal' else 'y'
    direct = direction
    global latex

    if(target == 'dual'):
      direct = 'max' if(direct == 'min') else 'min'

    # print target function
    for i, var in enumerate(data['target'], start=1):
      tmp.append(f"{var}{symbol}_{(i)}")

    latex += "\\textbf{" + f"{direct}imize" + "}\n"
    latex += "\\begin{align*}\n"
    latex += f"\t& {" + ".join(tmp)}\n"
    latex += "\\end{align*}\n\n"

    # print constraints
    latex += "\\textbf{subject to}\n"
    latex += "\\begin{align*}\n"

    for i, const in enumerate(data['constraints']):
      tmp = []
      for j in range(len(const['variables'])):
        tmp.append(f"{const['variables'][j]}{symbol}_{(j+1)}")
      latex += f"\t{" + ".join(tmp)} {const['operator']} {const['result']} \\\\\n"

    # print coefficients
    for i, coeff in enumerate(data['coefficients'], start=1):
      latex += f"\t{symbol}_{(i)} {coeff} \\\\\n"

    latex += "\\end{align*}\n\n"
  except Exception as e:
    printError(f"Something went wrong during {(target)} generation!" + str(e))


# Creating LaTeX file
def CreateLaTeX():
  try:
    time.sleep(1)
    print("\nCreating LaTeX file...")

    global latex
    f = open("dualLP.tex", 'w', encoding='utf-8')

    latex = \
      "\\documentclass[a4paper,12pt]{article}\n" \
      "\\usepackage{amsmath}\n" \
      "\\usepackage{amsfonts}\n" \
      "\\title{Primal and Dual Linear Programs}\n" \
      "\\begin{document}\n" \
      "\\maketitle\n"
    
    Print(primal, "primal")
    Print(dual, "dual")

    latex += "\\end{document}"
    f.write(latex)
    f.close()

    time.sleep(2)
    print("*LaTeX file creation completed")
  except Exception as e:
    printError("Something went wrong during LaTeX generation!" + str(e))


class main:
  def __init__(self):
    try:
      os.system('cls')
      print(f"\n{'-'*8} DUAL LINEAR PROGRAM {'-'*8}\n")

      Setup()
      GeneratePrimal()
      CalculateDual()
      CreateLaTeX()
    except:
      printError("Something went wrong during main calls!")

main()