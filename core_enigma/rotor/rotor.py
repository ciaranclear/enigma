

class RotorRingCharacterError(Exception):
  def __init__(self, character):
    super().__init__(f"{character} is not a valid ring character")


class RotorInputIndexError(Exception):
  def __init__(self, index):
    super().__init__(f"{index} is not a valid input index. "
      f"Must be between 0 and {Rotor.rotor_positions}")


class Rotor(object):
  """
  Rotor class represents an enigma rotor
  """

  _rotor_char_set = [chr(i) for i in range(65, 91)]
  _rotor_positions = len(_rotor_char_set)

  @classmethod
  def rotorChars(cls):
    return Rotor._rotor_char_set

  @classmethod
  def rotorPositions(cls):
    return Rotor._rotor_positions

  def __init__(self, ring_characters,
               wiring_characters,
               turnover_characters=None,
               rotor_id=None):

    super(Rotor, self).__init__()
    self.rotor_ID = rotor_id
    self.rng_chrs = ring_characters
    self.wir_chrs = wiring_characters
    self.trn_chrs = turnover_characters or []
    self.flag = "R_ROT" if self.canTurnover() else "F_ROT"
    self.rng_offset = 0	# offset from core position
    self.rot_offset = 0   # offset from static reference
    self.entry_wheel_rotor_hash = {}
    self.reflector_rotor_hash = {}
    self._validateRotorLists()
    self._makeRotorHashTables()

  def __repr__(self):
    return (f"ROTOR ID : {self.rotor_ID}\n"
            f"RING CHARACTERS : {self.rng_chrs}\n"
            f"WIRING CHARACTERS : {self.wir_chrs}\n"
            f"TURNOVER CHARACTERS : {self.trn_chrs}\n")

  def __str__(self):
    def listStr(_list):
      if len(_list) != 0:
        char = _list[0]
        if len(char) == 1:
          char += ' '
        string = f"{char}"
        for i in range(1, len(_list)):
          char = _list[i]
          if len(char) == 1:
            char += ' '
          string += f",{char}"
        return string
      else:
        return ''

    return (f"ROTOR ID -----------: {self.rotor_ID}\n"
            f"ROTOR SETTING ------: {self.rotorSetting}\n"
            f"RING SETTING -------: {self.ringSetting}\n"
            f"RING CHARACTERS ----: {listStr(self.rng_chrs)}\n"
            f"WIRING CHARACTERS --: {listStr(self.wir_chrs)}\n"
            f"TURNOVER CHARACTERS : {listStr(self.trn_chrs)}\n")
    
  @property
  def ringCharacters(self):
    return self.rng_chrs

  @property
  def wiringCharacters(self):
    return self.wir_chrs

  @property
  def turnoverCharacters(self):
    return self.trn_chrs

  @property
  def rotorId(self):
    return self.rotor_ID

  @property
  def ringSetting(self):
    return self.rng_chrs[self.rng_offset]

  @ringSetting.setter
  def ringSetting(self, ring_setting):
    ring_setting = self.validRingCharacter(ring_setting)
    self.rng_offset = self.rng_chrs.index(ring_setting)

  @property
  def rotorSetting(self):
    index = (self.rng_offset + self.rot_offset) % (self.rotorPositions() - 1)
    return self.rng_chrs[index]

  @rotorSetting.setter
  def rotorSetting(self, rotor_setting):
    rotor_setting = self.validRingCharacter(rotor_setting)
    rotor_offset = self.rng_chrs.index(rotor_setting)-self.rng_offset
    if rotor_offset < 0:
      rotor_offset = self.rotor_positions - rotor_offset
    self.rot_offset = rotor_offset

  def canTurnover(self):
    return True if len(self.trn_chrs) != 0 else False

  def incRingSetting(self):
    self.rng_offset = self._changeOffset(self.rng_offset, 1)

  def decRingSetting(self):
    self.rng_offset = self._changeOffset(self.rng_offset, -1)

  def incRotorSetting(self):
    self.rot_offset = self._changeOffset(self.rot_offset, 1)

  def decRotorSetting(self):
    self.rot_offset = self._changeOffset(self.rot_offset, -1)

  def keyedRotor(self):
    turnover = self.onTurnover()
    self.incRotorSetting()
    return turnover

  def lhOutput(self, input_index):
    if self.validInputIndex(input_index):
      return self.entry_wheel_rotor_hash[self.rot_offset][input_index]

  def rhOutput(self, input_index):
    if self.validInputIndex(input_index):
      return self.reflector_rotor_hash[self.rot_offset][input_index]

  def onTurnover(self):
    return True if self.rotorSetting in self.trn_chrs else False
	
  @property
  def rotorDict(self):
    return {
            "ROTOR_TYPE": self.rotor_ID,
            "ROTOR_SETTING": self.rotorSetting,
            "RING_SETTING": self.ringSetting,
            "RING_CHARACTERS": self._currentRingChars(),
            "ROTOR_CHARACTERS": self._currentRotorChars(),
            "TURNOVER_CHARACTERS": self.trn_chrs
            }

  def resetRotor(self):
    self.rng_offset = 0
    self.rot_offset = 0

  def defaultRotorSetting(self):
    self.rot_offset = 0

  def validRingCharacter(self, character):
    character = character.upper()
    if character in self.rng_chrs:
      return character
    else:
      raise RotorRingCharacterError(character)

  @staticmethod
  def validInputIndex(index):
    if 0 <= index <= Rotor._rotor_positions:
      return True
    raise RotorInputIndexError(index)

  # PRIVATE METHODS --------------------------------------------------------------- 

  def _validateRotorLists(self):
    self._validateRingCharacters()
    self._validateWireCharacters()
    self._validateTurnoverList()
    self._setTurnoverChars()

  def _validateRingCharacters(self):
    self._validList(self.rotor_ID, "ring characters", self.rng_chrs)
    self._validSize(self.rotor_ID, "ring characters", self.rng_chrs)
    self._validType(self.rotor_ID, "ring characters", self.rng_chrs)
    self._listToUpper(self.rng_chrs)
    self._nonRepeat(self.rotor_ID, "ring characters", self.rng_chrs)

  def _validateWireCharacters(self):
    self._validList(self.rotor_ID, "wiring characters", self.wir_chrs)
    self._validSize(self.rotor_ID, "wiring characters", self.wir_chrs)
    self._validType(self.rotor_ID, "wiring characters", self.wir_chrs)
    self._listToUpper(self.wir_chrs)
    self._validWireChars()
    self._nonRepeat(self.rotor_ID, "wiring characters", self.wir_chrs)       

  def _validateTurnoverList(self):
    self._validList(self.rotor_ID, "turnover characters", self.trn_chrs)
    self._validType(self.rotor_ID, "turnover characters", self.trn_chrs)
    self._listToUpper(self.trn_chrs)
    self._validTurnoverChars()

  def _validWireChars(self):
    for char in self.wir_chrs:
      if char not in self.rotorChars():
        raise Exception(f"Rotor {self.rotor_ID} wire error!. "
          f"Character '{char}' is not a valid wire character")

  def _validTurnoverChars(self):
    for char in self.trn_chrs:
      if char not in self.rotorChars():
        raise Exception(f"Rotor {self.rotor_ID} character {char} is "
          f"not a valid turnover character.")

  @staticmethod
  def _validList(rotor_id, list_type, _list):
    if type(_list) != list:
      raise Exception(f"Rotor {rotor_id} {list_type} list is of type "
        f"'{type(_list)}'. Must be of type 'list'")

  @staticmethod
  def _validSize(rotor_id, list_type, _list):
    if len(_list) != Rotor._rotor_positions:
      raise Exception(f"Rotor {rotor_id} {list_type} list is length "
        f"{len(_list)}. Must be length {Rotor._rotor_positions}.")

  @staticmethod
  def _nonRepeat(rotor_id, list_type, _list):
    if len(_list) != len({*_list}):
      repeated = [char for char in {*_list} if _list.count(char) > 1]
      raise Exception(f"Rotor {rotor_id} {list_type} list contains "
        f"repeated characters '{','.join(repeated)}'.\n"
        f"All characters must be unique.")

  @staticmethod
  def _validType(rotor_id, list_type, _list):
    for char in _list:
      if type(char) != str:
        raise Exception(f"Rotor {rotor_id}. Character in {list_type} "
          f"list at index {_list.index(char)} is type "
          f"{type(char)}.\nMust be type 'str'.")

  @staticmethod
  def _listToUpper(_list):
    _list = [char.upper() for char in _list]
    return _list

  def _setTurnoverChars(self):
    chars = []
    for char in self.trn_chrs:
      chars.append(self.rng_chrs[Rotor._rotor_char_set.index(char)])
    self.trn_chrs = chars

  def _makeRotorHashTables(self):
    for i in range(Rotor._rotor_positions):
      wir_chrs = [*self.wir_chrs[i:], *self.wir_chrs[0:i]]
      letters = [*Rotor._rotor_char_set[i:], *Rotor._rotor_char_set[0:i]]
            
      entry_wires = [letters.index(char) for char in wir_chrs]
      self.entry_wheel_rotor_hash[i] = entry_wires

      reflector_wires = [wir_chrs.index(char) for char in letters]
      self.reflector_rotor_hash[i] = reflector_wires

  def _ringCharsOffset(self):
    ring_chars_offset = self.rot_offset + self.rng_offset
    if ring_chars_offset > Rotor._rotor_positions-1:
      ring_chars_offset = ring_chars_offset - Rotor.rotor_positions
    return ring_chars_offset

  def _currentRingChars(self):
    ring_chars_offset = self._ringCharsOffset()
    slice1 = self.rng_chrs[ring_chars_offset:]
    slice2 = self.rng_chrs[0:ring_chars_offset]
    return [*slice1, *slice2]

  def _currentRotorChars(self):
    slice1 = self.wir_chrs[self.rot_offset:]
    slice2 = self.wir_chrs[0:self.rot_offset]
    return [*slice1, *slice2]

  @staticmethod
  def _changeOffset(value, direction):
    if direction == 1:
      if value == Rotor._rotor_positions-1:
        value = 0
      else:
        value += 1
    elif direction == -1:
      if value == 0:
        value = Rotor._rotor_positions-1
      else:
        value -= 1
    return value

if __name__ == "__main__":
    # passing set
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"

    rotor = Rotor(rng, wir, trn, rid)
    print(help(Rotor))

    # RING CHARACTER TESTS
    # RotorListValueError for ring char type int
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListValueError failing test ring char type int")
        print(e)
        pass
    else:
        print("## FAILED: RotorListValueError failing test ring char type int")
    # RotorListRepeatedError for repeated ring char
    rng = ['A','A','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListRepeatedError failing test repeated ring char")
        print(e)
        pass
    else:
        print("## FAILED: RotorListRepeatedError failing test repeated ring char")
    # RotorListTypeError for ring char non list type
    rng = ('A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListTypeError failing test ring char non list type")
        print(e)
        pass
    else:
        print("## FAILED: RotorListTypeError failing test ring char non list type")
    # RotorListLengthError for ring chars length 27
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','#']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListLengthError failing test ring char list length 27")
        print(e)
        pass
    else:
        print("## FAILED: RotorListLengthError failing test ring char list length 27")
    
    # WIRING CHARACTER TESTS
    # RotorListTypeError for wiring chars non list type
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ('C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E')
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListTypeError failing test for wiring char non list type")
        print(e)
        pass
    else:
        print("## FAILED: RotorListTypeError failing test for wiring char non list type")

    # RotorListLengthError for wiring chars length 27
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E','#']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListLengthError failing test for wiring char list length 27")
        print(e)
        pass
    else:
        print("## FAILED: RotorListLengthError failing test for wiring char list length 27")

    # RotorListValueError for wiring chars with int typpe
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = [1,'J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListValueError failing test for wiring char list with int type")
        print(e)
        pass
    else:
        print("## FAILED: RotorListValueError failing test for wiring char list with int type")

    # RotorWiringError for wiring chars with char length 2
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['CA','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorWiringError failing test for wiring chars with char length 2")
        print(e)
        pass
    else:
        print("## FAILED: RotorWiringError failing test for wiring chars with char length 2")

    # RotorWiringError for non valid wire char
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','#','E']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorWiringError failing test for wiring chars non valid wire char")
        print(e)
        pass
    else:
        print("## FAILED: RotorWiringError failing test for wiring chars non valid wire char")

    # RotorListRepeatedError for repeated wire char
    rng = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
           'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    wir = ['C','J','G','D','P','S','H','K','T','U','R','A','W',
           'Z','X','F','M','Y','N','Q','O','B','V','L','I','I']
    trn = ['Q','Z']
    rid = "III"
    try:
        rotor = Rotor(rng, wir, trn, rid)
    except Exception as e:
        print("## PASSED: RotorListRepeatedError failing test for repeated wiring char")
        print(e)
        pass
    else:
        print("## FAILED: RotorListRepeatedError failing test for repeated wiring char")