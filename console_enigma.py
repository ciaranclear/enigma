import core_enigma.factory as fct
from enigma_factory.enigma_factory import makeConsoleEnigma

def selectMachine():

  def printBadInput():
    print(f"Invalid input!. Must enter a number "
      	  f"between 1 and {len(machines)}.")

  while True:
    print("Enter a number to select an enigma machine")
    machines = fct.machines()
    for i in range(len(machines)):
      print(f"{i+1}. {machines[i]}")
  
    try:
      inpt = int(input())
    except Exception:
      printBadInput()
    else:
      if 0 < inpt <= len(machines):
        machine = machines[inpt-1]
        machine = fct.makeMachine(machine)
        machine = makeConsoleEnigma(machine)

        break
      else:
        printBadInput()
  
  return machine

def enigma():
  machine = selectMachine()
  machine.menu()
  while True:
    print(f"Enter 'q' to quit or any other key "
    	  f"to select a new enigma machine.")
    inpt = input()
    if inpt == 'q' or inpt == 'Q':
      break
    else:
      machine = selectMachine()
      machine.menu()

enigma()