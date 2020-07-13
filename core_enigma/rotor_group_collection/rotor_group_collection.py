from core_enigma.rotor.rotor import Rotor
from core_enigma.reflectors.reflectors import (Reflector,
	                                             RewireableReflector,
	                                             RotatingReflector)


class RotorGroupCollection(object):
  def __init__(self, rotors, ring_chars, reflectors):
    self.rotors = rotors
    self.ring_chars = ring_chars
    self.reflectors = reflectors

  def rotorsList(self, flag):
    rotors = []
    if flag not in ["R_ROT","F_ROT"]:
      raise Exception(f"Rotor flag error!. {flag} is not a valid rotor flag")
    elif flag == "R_ROT":
      for rotor in self.rotors:
        if len(self.rotors[rotor]["turnover_chars"]) != 0:
          rotors.append(rotor)
    elif flag == "F_ROT":
      for rotor in self.rotors:
        if len(self.rotors[rotor]["turnover_chars"]) == 0:
          rotors.append(rotor)
    return rotors

  def reflectorsList(self):
    return [reflector for reflector in self.reflectors]

  def initializeRotor(self, rotorType):
    wire_chars = self.rotors[rotorType]["wiring_chars"]
    turnover_chars = self.rotors[rotorType]["turnover_chars"]
    return Rotor(self.ring_chars, wire_chars, turnover_chars, rotorType)

  def initializeReflector(self, reflectorType):
    mode = self.reflectors[reflectorType]["mode"]
    wire_list = self.reflectors[reflectorType]["wiring_chars"]
    # reflector  mode = fixed
    if mode == "rotating":
      return RotatingReflector(reflectorType, wire_list)
    # rewirable  mode = rewirable
    elif mode == "rewireable":
      return RewireableReflector(reflectorType, wire_list)
    # rotating   mode = rotating
    elif mode == "fixed":
      return Reflector(reflectorType, wire_list)