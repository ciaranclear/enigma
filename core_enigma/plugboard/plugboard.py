from core_enigma.plugboard.shorting_bar import ShortingBar
from core_enigma.connector.connector import Connector

class PlugboardCharacterError(Exception):
  def __init__(self, character):
    super().__init__("{} is not a valid plugboard character".format(character))


class PlugboardPinTypeError(Exception):
  def __init__(self, pin_type):
    super().__init__("{} is not a valid pin type")


class Plugboard(object):
  
  _characters = [chr(i) for i in range(65, 91)]
  _sockets = len(_characters)

  @classmethod
  def plugboardChars(cls):
    return Plugboard._characters

  @classmethod
  def plugboardSockets(cls):
    return Plugboard._sockets

  def __init__(self):
        
    self._plugboard = {}
    self.clearPlugboard()
    super(Plugboard, self).__init__()

  # PUBLIC METHODS ------------------------------------------------------------------
  def __str__(self):
    def connected(char):
      conn = None
      if plugboard[char]["CONNECTED_DEVICE"] == "SHORTING_BAR":
        conn = char
      elif plugboard[char]["CONNECTED_DEVICE"] == "STECKER_PLUG":
        conn = plugboard[char]["SM"]
      elif plugboard[char]["CONNECTED_DEVICE"] == "UHR_BOX_PLUG":
        conn = plugboard[char]["CONNECTED_DEVICE_ID"]
      if len(conn) == 1:
        conn = ' ' + conn + ' '
      return conn

    plgbrdStr = f"{'-'*99}"
    plugboard = self.plugboardDict()
    for i in range(13):
      char1 = self._characters[i]
      char2 = self._characters[i+13]
      conn1 = connected(char1)
      conn2 = connected(char2)
      if i == 6:
        plgbrdStr += f"\nPLUGBOARD {'-'*10}"
      else:
        plgbrdStr += f"\n{' '*20}"
      plgbrdStr += f":{' '*20}{char1} --> {conn1}{' '*20}{char2} --> {conn2}"
    return plgbrdStr

  def clearPlugboard(self):
    new_dict = {}
    for character in self._characters:
      socket = Connector(character,"PLUGBOARD",self)
      shorting_bar = ShortingBar(character)
      socket.connect(shorting_bar)
      new_dict[character] = socket
    self._plugboard = new_dict

  def connectPlug(self, character, plug):
    character = self.validCharacter(character)
    self.disconnectPlug(character)
    self._plugboard[character].connect(plug)
    return True

  def disconnectPlug(self, character):
    character = self.validCharacter(character)
    if self._plugboard[character].deviceType != "SHORTING_BAR":
      self._plugboard[character].disconnect()
      self._plugboard[character].connect(ShortingBar(character))
      return True
    return False

  def connectedDevice(self, character):
    character = self.validCharacter(character)
    return self._plugboard[character].connectedDeviceType()

  def connectedDeviceId(self, character):
    character = self.validCharacter(character)
    return self._plugboard[character].connectedDeviceId()

  def connectedTo(self, character, pin_type):
    character = self.validCharacter(character)
    if self.validPinType(pin_type):
      return self._plugboard[character].outerPinValue(pin_type)
    else:
      raise PlugboardPinTypeError(pin_type)

  def pinValue(self, character, pin_type):
    return character

  def numberOfConnections(self):
    connected = 0
    for character in self._plugboard:
      if self._plugboard[character].deviceType != "SHORTING_BAR":
        connected += 1
    return connected 

  def validPlugboard(self):
    for character in self._plugboard:
      if not self._plugboard[character].deviceValid():
        return False
    return True

  valid = validPlugboard

  def validCharacter(self, character):
    if character.upper() in self._characters:
      return character.upper()
    else:
      raise PlugboardCharacterError(character)

  @staticmethod
  def validPinType(pin_type):
    pin_type = pin_type.upper()
    return pin_type if pin_type in ["SM","LG"] else False

  def plugboardDict(self):
    plugboard = {}
    for character in self._plugboard:
      plugboard[character] = self._charactersDict(character)
    return plugboard

  # PRIVATE METHODS ----------------------------------------------------------------

  def _charactersDict(self, char):
    char_dict = {}
    char_dict["SM"] = self._plugboard[char].outerPinValue("SM")
    char_dict["LG"] = self._plugboard[char].outerPinValue("LG")
    char_dict["CONNECTED_DEVICE"] = self.connectedDevice(char)
    char_dict["CONNECTED_DEVICE_ID"] = self.connectedDeviceId(char)
    return char_dict