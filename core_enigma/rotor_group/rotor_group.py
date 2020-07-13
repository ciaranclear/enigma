from core_enigma.entry_wheel.entry_wheel import EntryWheel

class CompatabilityError(Exception):
  def __init__(self, flag, device):
    err_msg = (f"Device {type(device)} flag {device.flag} "
               f"is not compatible for cell with flag {flag}")
    super(CompatabilityError, self).__init__(err_msg)


class Cell(object):
  flags = ["R_ROT",
           "F_ROT",
           "F_REF",
           "R_REF"]

  def __init__(self, flag):
    self.flag = self.validFlag(flag)
    self.device = None

  def __str__(self):
    if self.device:
      return self.device.__str__()
    elif self.flag in ["R_ROT","F_ROT"]:
      return f"EMPTY ROTOR POSITION\n"
    elif self.flag in ["R_REF","F_REF"]:
      return f"EMPTY REFLECTOR POSITION\n"

  def compatible(self, device):
    return device.flag == self.flag

  @classmethod
  def validFlag(cls, flag):
    if flag.upper() in cls.flags:
      return flag.upper()
    raise ValueError(f"Flag error!. '{flag}' is not a valid flag. "
      f"Needs to be flag in {cls.flags}")

  def getDevice(self):
    return self.device

  def setDevice(self, device):
    if self.compatible(device):
      self.device = device
    else:
      raise CompatabilityError(self.flag, device)
    
  def removeDevice(self):
    _device = self.device
    self.device = None
    return _device


class RotorGroup(object):
  def __init__(self, etw_list, cells_map):
    self.etw = EntryWheel(etw_list)
    self.rotors = {}
    self.reflector = Cell(cells_map["REF"])
    self._validCellsMap(cells_map)
    self._setRotorCells(cells_map)
    super(RotorGroup, self).__init__()

  def __str__(self):
    groupStr = f"{'-'*99}\n"
    groupStr += self.etw.__str__()
    for cell in self.rotors:
      groupStr += f"{'-'*99}\n"
      groupStr += f"ROTOR POSITION {cell} --:\n"
      groupStr += self.rotors[cell].__str__()
    groupStr += f"{'-'*99}\n"
    groupStr += self.reflector.__str__()
    groupStr += f"\n{'-'*99}"
    return groupStr

  def rotorFlag(self, position):
    self.validRotorPosition(position)
    return self.rotors[position].flag

  def reflectorFlag(self):
    return self.reflector.flag

  def rotorPositions(self):
    return len(self.rotors)

  def addRotor(self, position, rotor):
    self.validRotorPosition(position)
    self.rotors[position].setDevice(rotor)

  def removeRotor(self, position):
    self.validRotorPosition(position)
    self.rotors[position].removeDevice()

  def queryRotor(self, position):
    self.validRotorPosition(position)
    return self.rotors[position].getDevice()

  def addReflector(self, reflector):
    self.reflector.setDevice(reflector)

  def removeReflector(self):
    self.reflector.removeDevice()

  def queryReflector(self):
    return self.reflector.getDevice()

  def validRotorPosition(self, position):
    if position not in self.rotorSettings():
      raise Exception(f"{position} is not a valid rotor position")
    return True

  def rotors(self):
    rotors_dict = {}
    for rotor_cell in self.rotors:
      rotor = self.rotors[rotor_cell].get_device()
      if rotor:
        rotors_dict[rotor_cell] = rotor.rotor_id
      else:
        rotors_dict[rotor_cell] = None
    return rotors_dict

  def rotorSettings(self):
    rotor_settings = {}
    for rotor_cell in self.rotors:
      rotor = self.rotors[rotor_cell].getDevice()
      if rotor:
        rotor_settings[rotor_cell] = rotor.rotorSetting
      else:
        rotor_settings[rotor_cell] = None
    if self.reflector.flag == "R_REF":
      reflector = self.reflector.getDevice()
      if reflector:
        rotor_settings["REF"] = reflector.rotorSetting
      else:
        rotor_settings["REF"] = None
    return rotor_settings

  def ringSettings(self):
    ring_settings = {}
    for rotor_cell in self.rotors:
      rotor = self.rotors[rotor_cell].getDevice()
      if rotor:
        ring_settings[rotor_cell] = rotor.ringSetting
      else:
        ring_settings[rotor_cell] = None
    return ring_settings

  def reflector(self):
    reflector = self.reflector["REF"].getDevice()
    if reflector:
      return reflector.reflector_ID
    else:
      return None

  def output(self, character):
    index = self.etw.lhOutput(character)
    for i in range(self.rotorPositions()):
      rotor = self.rotors[f"R{i+1}"].getDevice()
      index = rotor.lhOutput(index)
    reflector = self.reflector.getDevice()
    index = reflector.output(index)
    for i in range(self.rotorPositions(),0,-1):
      rotor = self.rotors[f"R{i}"].getDevice()
      index = rotor.rhOutput(index)
    return self.etw.rhOutput(index)

  def rotorTurnover(self):
  	if self.rotors["R2"].getDevice().onTurnover():
  	  self.rotors["R2"].getDevice().keyedRotor()
  	  self.rotors["R3"].getDevice().keyedRotor()
  	if self.rotors["R1"].getDevice().keyedRotor():
  	  self.rotors["R2"].getDevice().keyedRotor()

  def validGroup(self):
  	if not self.reflector.getDevice():
  	  return False
  	for rotor_cell in self.rotors:
  	  if not self.rotors[rotor_cell].getDevice():
  	  	return False
  	return True

  def defaultSettings(self):
    for rotor_cell in self.rotors:
      rotor = self.rotors[rotor_cell].getDevice()
      if rotor:
        rotor.defaultRotorSetting()
    reflector = self.reflector.getDevice()
    if reflector:
      reflector.defaultRotorSetting()

  def _setRotorCells(self, cells_map):
    for cell in cells_map:
      if cell != "REF":
        self.rotors[cell] = Cell(cells_map[cell])

  @staticmethod
  def _validCellsMap(cells_map):
    cells = ["R1","R2","R3","R4","REF"]
    if type(cells_map) != dict:
      raise Exception("Cells map error!. Is type {}. "
      	"Must be type 'dict'.".format(type(cells_list)))

    if not 4 <= len(cells_map) <= 5:
      raise Exception("Cells map length error!. "
      	"Cells map must be length 4 or 5")

    for cell in cells_map:
      if cell not in cells:
        raise KeyError(f"Invalid cells map key. "
          f"{cell} is not a valid cell key. "
          f"Cell key must be in {cells}")

    reflector_flag = cells_map["REF"]
    reflector_flags = ["F_REF","R_REF"]
    if reflector_flag not in reflector_flags:
      raise Exception(f"Invalid reflector flag. "
        f"{reflector_flag} is not a valid reflector flag. "
      	f"Must be in {reflector_flags}")
    
    rotor_flags = ["F_ROT","R_ROT"]
    for cell in cells_map:
      if cell != "REF":
        rotor_flag = cells_map[cell]
        if rotor_flag not in rotor_flags:
          raise Exception(f"Invalid rotor flag. "
            f"{rotor_flag} at rotor position {cell} "
          	f"is not a valid rotor flag. Must be in {rotor_flags}")
    return cells_map