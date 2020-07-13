

class Reflector(object):

  reflector_chars = [chr(i) for i in range(65, 91)]

  def __init__(self, ref_id, wire_list):
    self.ref_id = ref_id
    self.flag = "F_REF"
    self.wire_chrs = self.validWiring(wire_list, ref_id)

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

    return (f"REFLECTOR ID -------: {self.ref_id}\n"
            f"WIRING CHARACTERS --: {listStr(self.wire_chrs)}")

  @property
  def reflectorID(self):
    return self.ref_id

  @staticmethod
  def validWiring(wire_chrs, ref_id=''):
    ref_chrs = Reflector.reflector_chars

    if type(wire_chrs) != list:
      raise Exception(f"{ref_id} wire list is type "
        f"{type(wire_chrs)}. Must be type list")

    if len(wire_chrs) != len(ref_chrs):
      raise Exception(f"{ref_id} wire list is length "
        f"{len(wire_chrs)}. Must be length {len(ref_chrs)}")

    for i in range(len(ref_chrs)):
      char = ref_chrs[i]

      if char not in wire_chrs and char.lower() not in wire_chrs:
        raise Exception(f"{ref_id} wire list does not contain "
          f"required character {char}")

      if wire_chrs[i] in [char, char.lower()]:
        raise Exception(f"Wire Error! {ref_id} character {char} "
          f"is self wired at index {i}")

    wire_chrs = [char.upper() for char in wire_chrs]

    return wire_chrs

  def output(self, index):
    try:
      index = self.wire_chrs.index(chr(index + 65))
    except IndexError:
      raise IndexError(f"Invalid index '{index}' in reflector "
        f"{self.ref_id}. Must be in range 0 to {len(reflector_chars)}")
    else:
      return index

  def reflectorDict(self):
    return {
      "REFLECTOR_ID": self.ref_id,
      "WIRE_CHARACTERS": self.wire_chrs
    }


class RewireableReflector(Reflector):
    
  def __init__(self, ref_id, wire_list):
    self.flag = "F_REF"
    super(RewireableReflector, self).__init__(ref_id, wire_list)

  def re_wire(self, wire_list):
    self.wire_chrs = self.validWiring(wire_list, self.ref_id)

class RotatingReflector(Reflector):

  def __init__(self, ref_id, wire_list):
    super(RotatingReflector, self).__init__(ref_id, wire_list)
    self.offset = 0
    self.flag = "R_REF"

  def output(self, index):
    index += self.offset
    if index >= len(self.wire_chrs):
      index -= len(self.wire_chrs)
    try:
      index = self.wire_chrs.index(chr(index + 65))
    except IndexError:
      raise IndexError(f"Invalid index '{index}' in reflector "
        f"{self.ref_id}. Must be in range 0 to {len(self.wire_chrs)}")
    else:
      return index

  def incSetting(self):
    if self.offset == len(self.wire_chrs) - 1:
      self.offset = 0
    else:
      self.offset += 1

  def decSetting(self):
    if self.offset == 0:
      self.offset = len(self.wire_chrs) - 1
    else:
      self.offset -= 1

  def defaultRotorSetting(self):
    self.offset = 0

  @property
  def rotorSetting(self):
    return self.reflector_chars[self.offset]

  @rotorSetting.setter
  def rotorSetting(self, setting):
    setting = self.validRingCharacter(setting)
    self.offset = self.reflector_chars.index(setting)

  def validRingCharacter(self, setting):
    err_msg = None

    if type(setting) != str:
      err_msg = (f"Reflector setting type error!. "
        f"Setting is type '{type(setting)}'. Must be type 'str'")
    if setting.upper() not in self.reflector_chars:
      err_msg = (f"Reflector setting value error!. "
        f"'{setting}' is not a valid reflector setting")
    if err_msg:
      raise Exception(err_msg)

    return setting.upper()

  def reflectorDict(self):
    return {
      "REFLECTOR_ID": self.ref_id,
      "WIRE_CHARACTERS": [*self.wire_chrs[self.offset:],
                          *self.wire_chrs[0:self.offset]],
      "RING_CHARACTERS": [*self.reflector_chars[self.offset:],
                          *self.reflector_chars[0:self.offset]],
      "REFLECTOR_SETTING": self.reflector_setting
      }

if __name__ == "__main__":
  ref_id = "UKW-B"
  wires = ['Z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']
  reflector = Reflector(ref_id, wires)
  print(reflector.output(0))
    
  new_wires = ['Z','C','A','B','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']
  rewire = RewireableReflector(ref_id, wires)
  rewire.re_wire(new_wires)

  print(help(RotatingReflector))
  reflector = RotatingReflector(ref_id, wires)
  print(reflector.output(25))
  reflector.inc_setting()
  print(reflector.output(25))
  print(reflector.reflector_dict())