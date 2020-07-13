from core_enigma.connector.connector import Connector

class SteckerCable(object):
  def __init__(self):
    self._plugs = {"P1": Connector("P1", "STECKER_PLUG", self),
                   "P2": Connector("P2", "STECKER_PLUG", self)}

  def plugs(self):
    """Returns dictionary object with two stecker plug
       objects. Key is plug_id 'P1' or 'P2' and the
       paired value is the corresponding plug object"""
    return self._plugs

  def pinValue(self, plug_id, pin_type):
    """Returns the value of the connected pin on the
       opposing plug"""
    pin_type = self._correspondingPinType(pin_type)
    if plug_id == "P1":
      return self._plugs["P2"].outerPinValue(pin_type)
    elif plug_id == "P2":
      return self._plugs["P1"].outerPinValue(pin_type)
    else:
      raise Exception(f"{plug_id} is not a valid stecker plug id."
      	              f"\nMust be 'P1' or 'P2'")

  def valid(self):
    """Returns boolean indicating if both plugs are
       connected"""
    for plug in self._plugs:
      if not self._plugs[plug].connected():
        return False
    return True

  def _correspondingPinType(self, pin_type):
    """Returns the opposing pin_type"""
    pin_type = self._validPinType(pin_type)
    return "SM" if pin_type == "LG" else "LG"

  @staticmethod
  def _validPinType(pin_type):
    """Raises an exception if the pin_type is not valid"""
    if pin_type not in ["SM","LG"]:
      raise Exception(f"{pin_type} is not a valid stecker pin type")

if __name__ == "__main__":

  print(dir(SteckerCable))
  print(help(SteckerCable))