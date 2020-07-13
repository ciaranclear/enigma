from core_enigma.connector.connector import Connector


class UhrBox(object):
  
  rotor_positions = 40

  def __init__(self, uhr_dict):
    self._rotor_position = 0
    self._side_A_rotor_hash = {}
    self._side_B_rotor_hash = {}
    self._plug_list = uhr_dict["PLUGS_LIST"]
    self._plug_A_map = self._extendPlugMap(uhr_dict["PLUG_A_MAP"])
    self._plug_B_map = self._extendPlugMap(uhr_dict["PLUG_B_MAP"])
    self._uhr_plugs_dict = {}
    self._setUhrPlugsDict()
    self._makeRotorHashTables(uhr_dict)
    super(UhrBox, self).__init__()

  # PUBLIC METHODS ------------------------------------------------------------------

  def __str__(self):
    return f"{'-'*99}\nUHR BOX SETTING ----: {self.uhrBoxSetting}"

  def validUhrPlugId(self, plug_id):
    if plug_id in self._plug_list:
      return plug_id
    else:
      raise Exception(f"{plug_id} is not a valid uhr plug id.")

  def uhrBoxPlugList(self):
    return self._plug_list

  def uhrPlugsDict(self):
    return self._uhr_plugs_dict

  @property
  def uhrBoxSettingRange(self):
    return UhrBox.rotor_positions-1

  def validUhrBoxSetting(self, setting):
    if isinstance(setting, int) and 0 <= setting < UhrBox.rotor_positions:
      return True
    else:
      raise Exception(f"Invalid Uhr Box setting {setting}. "
      	              f"\nMust be in range of 0 to {self.uhrBoxSettingRange}")
  
  def incUhrBoxSetting(self):
    if self._rotor_position + 1 == UhrBox.rotor_positions:
      self._rotor_position = 0
    else:
      self._rotor_position += 1

  def decUhrBoxSetting(self):
    if self._rotor_position == 0:
      self._rotor_position = UhrBox.rotor_positions-1
    else:
      self._rotor_positions -= 1

  @property
  def uhrBoxSetting(self):
    return self._rotor_position

  @uhrBoxSetting.setter
  def uhrBoxSetting(self, setting):
    self.validUhrBoxSetting(setting)
    self._rotor_position = setting

  def uhrBoxConnected(self):
    for plug_id in self._plug_list:
      if not self._uhr_plugs_dict[plug_id].connected():
        return False
    return True

  valid = uhrBoxConnected

  def uhrBoxDisconnected(self):
    for plug_id in self._plug_list:
      if self._uhr_plugs_dict[plug_id].connected():
        return False
    return True

  def pinValue(self, plug_id, pin_type):
    plug_id = self.validUhrPlugId(plug_id)
    pin = plug_id + pin_type
    return self.correspondingChar(pin)

  def correspondingPin(self, pin):
    plug_type = self._getPlugType(pin)

    corresponding_pin = ''
    if plug_type == 'A':
      term = self._plug_A_map[pin]
      corresponding_term = self._side_A_rotor_hash[self._rotor_position][term]
      corresponding_pin = self._plug_B_map[corresponding_term]
    elif plug_type == 'B':
      term = self._plug_B_map[pin]
      corresponding_term = self._side_B_rotor_hash[self._rotor_position][term]
      corresponding_pin = self._plug_A_map[corresponding_term]
    return corresponding_pin

  def correspondingChar(self, pin):
    connected_pin = self.correspondingPin(pin)
    plug_id = self._getPlugId(connected_pin)
    character = self._uhr_plugs_dict[plug_id].outerPinValue(pin)

    return character

  def uhrBoxDict(self):
    uhr_dict = {}

    for plug_id in self._plug_list:
      plug_dict = self._getPlugDict(plug_id)
      uhr_dict[plug_id] = plug_dict
    return uhr_dict

  # PRIVATE METHODS ----------------------------------------------------------------

  def _validateUhrDict(self, uhr_dict):

    connections = uhr_dict['CONNECTIONS_LIST']
    # check connections list length equal to rotor positions
    if len(connections) != UhrBox.rotor_positions:
      raise Exception(f"Uhr box connections list length not equal to rotor positions."
                      f"\nConnections list length is {len(connections)}. "
                      f"\nRequired length is {UhrBox.rotor_positions}")
    # check connections list numbers are unique
    if len(connections) != len(set(connections)):
      raise Exception(f"Uhr box connections list contains repeated values."
                      f"\n{connections}")
    # check connections list numbers are in range of rotor positions
    in_range_numbers = [num for num in connections if num < UhrBox.rotor_positions]
    if len(connections) != len(in_range_numbers):
      raise Exception(f"Uhr box connections list contains numbers out of range "
                      f"of rotor position {connections}")
    # check even index has even num and odd index has odd num
    for i in range(len(connections)):
      if (i % 2 == 0 and connections[i] % 2 != 0)\
        or (i % 2 != 0 and connections[i] % 2 == 0):
        raise Exception(f"Uhr box connections list connection error. "
                        f"\nConnection numbers at even indexes must be even. "
                        f"\nConnection numbers at odd indexes must be odd."
                        f"\n{connections}")

  def _makeRotorHashTables(self, uhr_dict):
    connections = uhr_dict["CONNECTIONS_LIST"]
    self._side_A_rotor_hash = self._makeRotorHashTable(connections)
    corresponding = self._corresponding(connections)
    self._side_B_rotor_hash = self._makeRotorHashTable(corresponding)

  @staticmethod
  def _makeRotorHashTable(connections):
    hashTable = {}

    for i in range(UhrBox.rotor_positions):
      num_list = []
      for num in connections:
        new_num = num + i
        if new_num >= UhrBox.rotor_positions:
          new_num -= UhrBox.rotor_positions
        num_list.append(new_num)
      hashTable[i] = num_list
      connections = [*connections[1:],connections[0]]
    return hashTable

  @staticmethod
  def _corresponding(connections):
    corresponding = [None for i in range(UhrBox.rotor_positions)]

    for i in range(UhrBox.rotor_positions):
      index = connections[i]
      corresponding[index] = i
    return corresponding

  @staticmethod
  def _getPlugType(pin):      
    return pin[2]

  @staticmethod
  def _getPlugId(pin):     
    return pin[0:3]

  def _setUhrPlugsDict(self):
    for plug_id in self._plug_list:
      self._uhr_plugs_dict[plug_id] = Connector(plug_id, "UHR_BOX_PLUG", self)

  def _getPlugDict(self, plug_id):

    plug_dict = {}
    pin_type = plug_id + "LG"
    pin_dict = self._getPinDict(pin_type)
    plug_dict[pin_type] = pin_dict
    pin_type = plug_id + "SM"
    pin_dict = self._getPinDict(pin_type)
    plug_dict[pin_type] = pin_dict
    character = self._uhr_plugs_dict[plug_id].outerPinValue(pin_type)
    plug_dict["CHAR"] = character

    return plug_dict

  def _getPinDict(self, pin_type):
    pin_dict = {}
    corresponding_pin = self.correspondingPin(pin_type)
    character = self.correspondingChar(pin_type)
    pin_dict["CONNECTED_PIN_ID"] = corresponding_pin
    pin_dict["CONNECTED_CHAR"] = character

    return pin_dict

  @staticmethod
  def _extendPlugMap(plug_map):
    new_map = plug_map.copy()
    for connection in plug_map:
      plug = plug_map[connection]
      new_map[plug] = connection
    return new_map


if __name__ == "__main__":
  pass
