from core_enigma.connector.connector import Connector
"""
class ShortingBar(Connector):
  def __init__(self):
    super(ShortingBar, self).__init__("SHORTING_BAR", "SHORTING_BAR", self)

  def innerPinValue(self, pin_type):
    
    if pin_type == "LG":
      return self._connector.outerPinValue("SM")
    elif pin_type == "SM":
      return self._connector.outerPinValue("LG")
    else:
      raise Exception(f"{plug_id} is not a valid pin_type."
      	              f"\nMust be 'LG' or 'SM'")

  def valid(self):
    return True

  def pinValue(self):
    pass
"""

class ShortingBar(object):
  def __init__(self, character):
    self.device_type = "SHORTING_BAR"
    self.bar_id = character
    self.connector = None
    self.connected = False

  def connect(self,connector):
    self.connector = connector
    self.connected = True
    if not connector.connected:
      connector.connect(self)

  def disconnect(self):
    self.connected = False
    if self.connector.connected:
      self.connector.disconnect()
    self.connector = None

  def connected(self):
    return self.connected

  def innerPinValue(self, pin_id):
    if pin_id == "SM":
      return self.connector.innerPinValue("LG")
    elif pin_id == "LG":
      return self.connector.innerPinValue("SM")

  def valid(self):
    return True

  def pinValue(self):
    pass

  def deviceId(self):
    return self.bar_id

  def deviceType(self):
    return self.device_type