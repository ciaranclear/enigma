
class Connector(object):

  def __init__(self, connector_id, device_type, device):
    self.conn_id = connector_id
    self.device_type = device_type or None
    self.device = device
    self.connector = None
    self.connected = False
    self._validateDevice()

  def connect(self, connector):
    """Takes a connector instance and connects this connector 
       to the other connector and connects the other connector
       to this connector if it is not currently connected"""
    self.connector = connector
    self.connected = True
    if not connector.connected:
      connector.connect(self)

  def disconnect(self):
    """Calls the disconnect on its connected connector 
       and then disconnects this connector"""
    self.connected = False
    if self.connector.connected:
      self.connector.disconnect()
    self.connector = None

  def connected(self):
    """Returns boolean indicating connection status"""
    return self.connected

  def innerPinValue(self, pin_id):
    """Returns the value in this connectors parent device
       for the pin_id given"""
    return self.device.pinValue(self.conn_id, pin_id)

  def outerPinValue(self, pin_id):
    """Returns the value from this connectors connected
       connector for the given pin_id"""
    if self.connected:
      return self.connector.innerPinValue(pin_id)
    else:
      raise Exception(f"Connection error!. {self.conn_id} not connected")

  def deviceValid(self):
    """Returns boolean indicating if this connectors parent
       device is in a valid operating state"""
    return self.device.valid(self.conn_id)

  def connectorValid(self):
    """Returns boolean indicating if this connectors connected
       connector parent device is in a valid operating state"""
    if self.connected:
      return self.connector.valid(self.conn_id)
    else:
      raise Exception(f"Connection error!. {self.conn_id} not connected")

  def deviceId(self):
    """Returns this connectors id"""
    return self.conn_id

  def deviceType(self):
    """Returns this connectors parent device type"""
    return self.device_type

  def connectedDeviceId(self):
    if self.connected:
      return self.connector.deviceId()

  def connectedDeviceType(self):
    if self.connected:
      return self.connector.deviceType()

  def _validateDevice(self):
    if not hasattr(self.device, "valid"):
      raise NotImplementedError(f"valid method not implemented in {type(self.device)}")
    if not hasattr(self.device, "pinValue"):
      raise NotImplementedError(f"pinValue method not implemented {type(self.device)}")


if __name__ == "__main__":
  print(dir(Connector))
  print(help(Connector))