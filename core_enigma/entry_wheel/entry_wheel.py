
class EntryWheelCharacterError(Exception):
  def __init__(self, character):
    super().__init__("{} is not a valid entry wheel character"
      .format(character))


class EntryWheelIndexError(Exception):
  def __init__(self, index, max_index):
    super().__init__("{} index is out of range of entry wheel list. "
      "Max value {}".format(index, max_index))


class EntryWheel(object):
  
  _ew_char_set = [chr(i) for i in range(65, 91)]
  _ew_positions = len(_ew_char_set)

  def __init__(self, etw_list):
    self._ew = self._validEtwList(etw_list)
    super(EntryWheel, self).__init__()

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
        
    return f"ENTRY WHEEL --------: {listStr(self._ew)}\n"

  def lhOutput(self, character):
    try:
      output = self._ew.index(character)
    except ValueError:
      raise EntryWheelCharacterError(character)
    else:
      return output

  def rhOutput(self, index):
    try:
      output = self._ew[index]
    except IndexError:
      raise EntryWheelIndexError(index, self._ew_positions)
    else:
      return output

  @property
  def entryWheelList(self):
    return self._ew

  def _validEtwList(self, etw_list):
    if len(set(etw_list)) != len(etw_list):
      raise Exception("Entry wheel list has repeated characters. "
        "Must be list of unique characters")
    if len(etw_list) != self._ew_positions:
      raise Exception("Entry wheel list is length {}. "
        "Must be length {}".format(len(etw_list), self._ew_positions))
    for character in etw_list:
      if type(character) != str or character.upper() not in self._ew_char_set:
        raise Exception("Entry wheel list contains invalid character {}"
          .format(character))
    return [char.upper() for char in etw_list]