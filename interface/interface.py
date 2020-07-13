import types
import re
from core_enigma.settings.settings import MORSE_CODE
from core_enigma.stecker_cable.stecker_cable import SteckerCable
from display.histogram import histogramString
from core_enigma.reflectors.reflectors import RewireableReflector

def addInterfaces(machine):
  mc = machine
  mc.menu = types.MethodType( menu, mc )
  mc.machineSetup = types.MethodType( machineSetup, mc )
  mc.machineInput = types.MethodType( machineInput, mc )
  mc.encodeDecode = types.MethodType( encodeDecode, mc )
  mc.convertFile = types.MethodType( convertFile, mc )
  mc.machineString = types.MethodType( machineString, mc )
  mc.displayMachine = types.MethodType( displayMachine, mc )
  mc.rotorsSetup = types.MethodType( rotorsSetup, mc )
  mc.reflectorSetup = types.MethodType( reflectorSetup, mc )
  mc.selectRotors = types.MethodType( selectRotors, mc )
  mc.ringSettings = types.MethodType( ringSettings, mc )

  mc._formatString = types.MethodType( _formatString, mc )
  mc._formatInput = types.MethodType( _formatInput, mc )
  mc._morseString = types.MethodType( _morseString, mc )
  if hasattr(mc, "plugboard"):
    if hasattr(mc, "uhr_box"):
      mc.uhrBoxPlugboardSetup = types.MethodType( uhrBoxPlugboardSetup, mc )
      mc.uhrBoxSetup = types.MethodType( uhrBoxSetup, mc )
    else:
      mc.steckerPlugboardSetup = types.MethodType( steckerPlugboardSetup, mc )

def menu(self):
  while True:
    print(f"Enter a number to select an option"
          f"\n1. Machine Setup"
          f"\n2. Machine Input"
          f"\n3. Display Machine"
          f"\n4. Quit")
    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Must be a number")
    else:
      if inpt == 1:
        self.machineSetup()
      elif inpt == 2:
        self.machineInput()
      elif inpt == 3:
        self.displayMachine()
      elif inpt == 4:
        break
      else:
        print("Invalid input!. Try again")

def machineSetup(self):
  while True:
    escape = 3
    print(f"Enter a number to select an option"
    	  f"\n1. Rotor Setup"
    	  f"\n2. Reflector Setup")
    if hasattr(self, "plugboard"):
      print("3. Plugboard Setup")
      escape = 4
    if hasattr(self, "uhr_box"):
      print("4. Uhr Box Setup")
      escape = 5
    print(f"{escape}. Return to main menu")
    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Must be a number")
    else:
      if inpt == 1:
        self.rotorsSetup()
      elif inpt == 2:
      	self.reflectorSetup()
      elif inpt == 3 and hasattr(self, "plugboard"):
      	if hasattr(self, "uhr_box"):
      	  self.uhrBoxPlugboardSetup()
      	else:
      	  self.steckerPlugboardSetup()
      elif inpt == 4 and hasattr(self, "uhr_box"):
        self.uhrBoxSetup()
      elif inpt == escape:
      	break
      else:
        print("Invalid input!. Try again")

def machineInput(self):
  print("CALLED MACHINE INPUT")
  while True:
    print(f"Enter a number to select an option"
    	  f"\n1. Encode/Decode"
        f"\n2. Convert file"
    	  f"\n3. Return to main menu")
    try:
      inpt = int(input())
    except Exception:
      print("Invalid Input!. Must be a number")
    else:
      if inpt == 1:
      	self.encodeDecode()
      elif inpt == 2:
        self.convertFile()
      elif inpt == 3:
      	break
      else:
      	print("Invalid input!. Try again")

def encodeDecode(self):
  if self.validEnigma():
    inpt = input().upper()
    outp = ""
    validInpt = ""
    displayStr = ""
    f = open("ENIGMA.txt","w+")
    f.write(self.machineString())
    for char in inpt:
      outpChar = self.getOutput(char)
      if outpChar:
        validInpt += char.upper()
        outp += outpChar
    hist = histogramString(validInpt, outp)
    print(hist)
    displayStr += f"\n{'-'*99}"
    displayStr += f"\nFORMATTED INPUT\n"
    displayStr += f"\n{self._formatInput(inpt)}"
    displayStr += f"\n{'-'*99}"
    displayStr += f"\nFILTERED INPUT\n"
    displayStr += f"\n{self._formatString(validInpt)}"
    displayStr += f"\n{'-'*99}"
    displayStr += f"\nMACHINE OUTPUT\n"
    displayStr += f"\n{self._formatString(outp)}"
    displayStr += f"\n{'-'*99}"
    displayStr += f"\nMORSE OUTPUT"
    displayStr += f"\n{self._morseString(outp)}"
    displayStr += f"\n{'-'*99}"
    print(displayStr)
    f.write(hist)
    f.write(displayStr)
    f.close()
  else:
    print("Machine setup is not complete")

def convertFile(self):
  f = open("CONVERT.txt", "r")
  inpt = f.read().upper()
  outp = ""
  validInpt = ""
  displayStr = ""
  f = open("ENIGMA.txt","w+")
  f.write(self.machineString())
  for char in inpt:
    outpChar = self.getOutput(char)
    if outpChar:
      validInpt += char.upper()
      outp += outpChar
  hist = histogramString(validInpt, outp)
  print(hist)
  displayStr += f"\n{'-'*99}"
  displayStr += f"\nFORMATTED INPUT\n"
  displayStr += f"\n{self._formatInput(inpt)}"
  displayStr += f"\n{'-'*99}"
  displayStr += f"\nFILTERED INPUT\n"
  displayStr += f"\n{self._formatString(validInpt)}"
  displayStr += f"\n{'-'*99}"
  displayStr += f"\nMACHINE OUTPUT\n"
  displayStr += f"\n{self._formatString(outp)}"
  displayStr += f"\n{'-'*99}"
  displayStr += f"\nMORSE OUTPUT"
  displayStr += f"\n{self._morseString(outp)}"
  displayStr += f"\n{'-'*99}"
  print(displayStr)
  f.write(hist)
  f.write(displayStr)
  f.close()

def machineString(self):
  def machineHeader(self):
    name = ' ' + self.machineType + ' '
    padding = int(len(name)/2)
    string = f'{"-"*(49-padding)}{name}{"-"*(49-padding)}'
    return string

  machineStr = machineHeader(self)
  machineStr += '\n'
  if hasattr(self, "plugboard"):
    machineStr += self.plugboard.__str__()
    machineStr += '\n'
  if hasattr(self, "uhr_box"):
    machineStr += self.uhr_box.__str__()
  machineStr += self.rotor_group.__str__()
  return machineStr

def displayMachine(self):

  print(self.machineString())

def steckerPlugboardSetup(self):
  
  def connectPlugs(self):
    print(f"Enter comma seperated plug pairs ie 'AB,CD,EF'."
  	  f"\nPlug pairs containing non alpha characters will be"
  	  f"\nignored. Up to 13 plug pairs can be entered."
  	  f"\nThe plugboard is cleared every time a new plug pair"
  	  f"\nlist is entered.")
    while True:
      self.plugboard.clearPlugboard()
      inpt = input()
      pat = re.compile(r'([a-zA-Z])\s*([a-zA-Z])\s*')
      matches = pat.finditer(inpt)
      pairs = []
      pat = re.compile(r'[a-zA-Z]')
      for match in matches:
        pair = re.findall(pat, match.group())
        pairs.append(pair)
      chars = []
      for pair in pairs:
        chars+=pair
      if len(chars) != len(set(chars)):
        print("Plugboard connection error!. All letters must be unique")
      else:
        connections = "PLUGBOARD CONNECTIONS "
        for pair in pairs:
          char1 = pair[0].upper()
          char2 = pair[1].upper()
          cable = SteckerCable()
          plugs = cable.plugs()
          self.plugboard.connectPlug(char1, plugs["P1"])
          self.plugboard.connectPlug(char2, plugs["P2"])
          connections += f"{char1}{char2} "
        print(connections)
        break

  while True:
    print(f"Enter a number to select an option"
          f"\n1. Connect Plugs"
          f"\n2. Clear Plugboard"
          f"\n3. Return to machine setup")

    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Must be a number")
    else:
      if inpt == 1:
        connectPlugs(self)
      elif inpt == 2:
        self.plugboard.clearPlugboard()
      elif inpt == 3:
        break
      else:
        print("Invalid input!. Try again")

def uhrBoxPlugboardSetup(self):

  def getConnections(side):
    letters = [chr(i) for i in range(65,91)]
    while True:
      print(f"Enter 10 connections for uhr box {side} plugs"
    	    f"Connection order is 01{side} -> 10{side}")
      inpt = input()
      inpt = [char.upper() for char in inpt]
      connections = [char for char in inpt if char in letters]
      if len(connections) != len(set(connections)):
        print("Repeated character. All characters must be unique")
      elif len(connections) < 10:
        print("To few connections entered")
      elif len(connections) > 10:
        print("Not enough connections entered")
      else:
        return connections
  
  def connectPlugs(self):
    self.plugboard.clearPlugboard()
    plug_ids = self.uhr_box.uhrBoxPlugList()
    while True:
      aConnections = getConnections("A")
      print(f"LETTERS ALREADY USED {aConnections}")
      bConnections = getConnections("B")
      # ensure no shared characters between two lists
      allConns = aConnections + bConnections
      if len(allConns) != len(set(allConns)):
        print(f"Repeated character between A and B connections. "
        	  f"Try again")
      else:
        connections = zip(plug_ids, allConns)
        plugs = self.uhr_box.uhrPlugsDict()
        for conn in connections:
          plug = plugs[conn[0]]
          self.plugboard.connectPlug(conn[1], plug)
        return

  while True:
    print(f"Enter a number to select an option"
    	  f"\n1. Connect uhr box plugs"
    	  f"\n2. Clear plugboard"
    	  f"\n3. Return to machine setup")

    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Must be a number")
    else:
      if inpt == 1:
        connectPlugs(self)
      elif inpt == 2:
        self.plugboard.clearPlugboard()
        self.uhr_box.disconnectUhrPlugs()
      elif inpt == 3:
        break
      else:
        print("Invalid input!. Try again")

def uhrBoxSetup(self):
  print(f"CURRENT UHR BOX SETTING {self.uhr_box.uhrBoxSetting}")
  while True:
    print("ENTER A NEW UHR BOX SETTING 0 -> 39")
    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Try again")
    else:
      try:
        self.uhr_box.validUhrBoxSetting(inpt)
      except Exception:
        print(f"Invalid input!. Out of range")
      else:
      	self.uhr_box.uhrBoxSetting = inpt
      	print(f"UHR BOX SETTING IS {inpt}")
      	break

def rotorsSetup(self):
  while True:
    print(f"Enter a number to select an option"
    	  f"\n1. Select Rotors"
    	  f"\n2. Ring Settings"
    	  f"\n3. Rotor Settings"
    	  f"\n4. Return to machine setup")
    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Must be a number")
    else:
      if inpt == 1:
        self.selectRotors()
      elif inpt == 2:
      	self.ringSettings()
      elif inpt == 3:
        self.rotorSettings()
      elif inpt == 4:
      	break
      else:
      	print("Invalid input!. Try again")

def reflectorSetup(self):

  def getReflectorWireList(reflector):
    while True:
      print("Enter 26 unique characters A -> Z for reflector wire list")
      inpt = input()
      pat = re.compile(r'([a-zA-Z])*[\s,;]')
      subbed = pat.sub(r'\1', inpt)
      wire_list = [char.upper() for char in subbed]
      unique = set(wire_list)
      try:
        reflector.validWiring(wire_list, reflector.ref_id)
      except Exception as e:
        print(e)
      else:
        reflector.re_wire(wire_list)
        break

  def rewireableReflectorMenu(reflector):
    # display current wiring
    print(f"The current wiring for reflector {reflector.ref_id}"
      f" is {','.join(map(str, reflector.wire_chrs))}")
    # ask user if they wish to modify wiring
    print("Enter Y to modify reflector wiring or any other key to continue")
    inpt = input()
    if inpt.upper() == 'Y':
      # if yes to modify get user to input valid wiring list
      getReflectorWireList(reflector)
    print(f"The reflector wiring is {','.join(map(str, reflector.wire_chrs))}")

  reflectors = self.rotor_group_collection.reflectorsList()
  while True:
    print(f"Enter a number to select a reflector")
    for i in range(len(reflectors)):
      print(f"{i+1}. {reflectors[i]}")
    try:
      inpt = int(input())
    except Exception:
      print("Invalid input!. Must be a number")
    else:
      if 0 < inpt <= len(reflectors):
        reflector_type = reflectors[inpt-1]
        reflector = self.rotor_group_collection.initializeReflector(reflector_type)
        if isinstance(reflector, RewireableReflector):
          rewireableReflectorMenu(reflector)
        self.rotor_group.addReflector(reflector)
        break
      else:
        print("Invalid input!. Try again")

def selectRotors(self):
  for rotor_cell in self.rotor_group.rotors:
    flag = self.rotor_group.rotorFlag(rotor_cell)
    rotors = self.rotor_group_collection.rotorsList(flag)
    while True:
      print(f"Enter a number to select a rotor for {rotor_cell}")
      for i in range(len(rotors)):
        print(f"{i+1}. {rotors[i]}")
      try:
      	inpt = int(input())
      except Exception:
        print("Invalid input!. Must be a number")
      else:
        if 0 < inpt <= len(rotors):
          rotor_type = rotors[inpt-1]
          rotor = self.rotor_group_collection.initializeRotor(rotor_type)
          self.rotor_group.addRotor(rotor_cell, rotor)
          break
        else:
          print("Invalid input!. Try again")

def ringSettings(self):
  # allow setting of rings for rotors
  # set default ring settings
  settings = self.rotor_group.ringSettings()
  settings_str = "Current ring settings "
  for position in settings:
    settings_str += f"{position} {settings[position]} "
  print(settings_str)

  for position in settings:
    if settings[position]:
      while True:
        device = self.rotor_group.queryRotor(position)
        print(f"Enter a ring setting for {position}")
        inpt = input()
        try:
          inpt = device.validRingCharacter(inpt)
        except Exception:
          print(f"{inpt} is not a valid ring setting")
        else:
          device.ring_setting = inpt
          break
      else:
        print(f"{position} Has no rotor")

def rotorSettings(self):
  # allow setting of all rotors and reflector if applicable
  # set default rotor settings

  # print current rotor settings
  settings = self.rotor_group.rotorSettings()
  settings_str = "Current rotor settings "
  for position in settings:
    settings_str += f"{position} {settings[position]} "
  print(settings_str)

  # for each rotor position ask user for new setting
  for position in settings:
    if settings[position]:
      while True:
        if position == "REF":
          device = self.rotor_group.queryReflector()
        else:
          device = self.rotor_group.queryRotor(position)
        print(f"Enter a rotor setting for {position}")
        inpt = input()
        try:
          inpt = device.validRingCharacter(inpt)
        except Exception as e:
          #print(f"{inpt} is not a valid rotor setting")
          raise e
        else:
          device.rotorSetting = inpt
          break
    else:
      print(f"{position} Has no rotor")

def _formatString(self, string):
  count = 1
  newStr = ""
  for char in string:
    newStr += char
    if count%5 == 0:
      newStr += ' '
    if count%80 == 0:
      newStr += '\n'
    count += 1
  return newStr

def _formatInput(self, inputString):
  words = inputString.split()
  formatted = ""
  line = ""
  for i in range(len(words)):
    word = words[i]
    if i != len(words)-1:
      next_word = words[i+1]
    else:
      next_word = ''
    line += word
    if len(line) + len(next_word) >= 99:
      line += '\n'
      formatted += line
      line = ""
    else:
      line += ' '
  formatted += line
  return formatted

def _morseString(self, outputString):
  morse = ""
  line = ""
  for i in range(len(outputString)):
    taps = MORSE_CODE[outputString[i]]
    if len(line) + len(taps) + 4 >= 100:
      line += '\n'
      morse += line
      line = ""
    else:
      line += taps
      line += '    '
  morse += line
  return morse