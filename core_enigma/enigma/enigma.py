

class Enigma(object):
  def __init__(self):
    pass

  @property
  def machineType(self):
    return type(self).__name__

  def getOutput(self, character):
    character = self.keyboard.keyboardInput(character)
    if character:
      self.rotor_group.rotorTurnover()
      if hasattr(self, "plugboard"):
        character = self.plugboard.connectedTo(character, "LG")
      character = self.rotor_group.output(character)
      if hasattr(self, "plugboard"):
        character = self.plugboard.connectedTo(character, "SM")
    return character

  def validEnigma(self):
    valid = True
    if not self.rotor_group.validGroup():
      valid = False
    if hasattr(self, "plugboard"):
      valid = self.plugboard.validPlugboard
    return valid

  def setDefaultSettings(self):
    if hasattr(self, "plugboard"):
      self.plugboard.clearPlugboard()
    self.rotor_group.defaultSettings()