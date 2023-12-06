from typing import Optional, Any, Union, Dict, List, Tuple
from enigma_core.scrambler.exceptions.exceptions import (CellFlagError,
                                                         CompatibilityError,
                                                         CellDeviceError)


class Cell:

    @classmethod
    def valid_flag(cls, flag: str) -> str:
        """
        Returns the flag if valid. If not a valid flag raises a CellFlagError.
        """
        if flag not in ["REF","F_ROT","R_ROT"]:
            msg = (f"{flag} is not a valid scrambler cell flag. "
                   f"Must be 'REF','F_ROT' or 'R_ROT'.")
            raise CellFlagError(msg)
        else:
            return flag

    def __init__(self, position: str, flag: str) -> None:
        """
        Takes a cell position and a cell flag to initialize the cell object.
        The cell flag must be 'REF','F_ROT' or 'R_ROT'.
        """
        self.position = position
        self._flag = self.valid_flag(flag)
        self._device = None

    def __str__(self) -> str:
        """
        If a device is set returns the device string.
        """
        if self._device:
            return self._device.__str__()

    def compatible(self, device_obj):
        """
        Takes a Rotor or Reflector device object and compares its flag to the
        cell flag. The device object is returned if the flags are equal. If the
        flags are not equal raises a CompatibilityError.
        """
        if device_obj.flag != self._flag:
            msg = (f"{device_obj.device_id} is not compatible "
                   f"with {self.position} {self._flag} flag.")
            raise CompatibilityError(msg)
        else:
            return device_obj

    @property
    def flag(self) -> str:
        """
        Returns the cell flag.
        """
        return self._flag

    def set_device(self, device_obj) -> None:
        """
        Takes a Rotor or Reflector device to be set in the cell. If cell is
        already occupied raises a CellDeviceError.
        """
        self.compatible(device_obj)

        if self._device != None:
            msg = (f"Cell {self.position} is already occupied with "
                   f"{self._device.device_id}. Cannot accept "
                   f"{device_obj.device_id}")
            raise CellDeviceError(msg)
        else:
            self._device = device_obj

    def get_device(self):
        """
        Returns the device object but does not remove it from the cell. If no
        device object to return raises a CellDeviceError.        
        """
        if self._device != None:
            return self._device
        else:
            msg = f"Cell {self.position} does not currently have a device set."
            raise CellDeviceError(msg)

    def remove_device(self):
        """
        Returns the device object after removing it. If no device object to
        return raises a CellDeviceError.        
        """
        if self._device != None:
            device = self._device
            self._device = None
            return device
        else:
            msg = f"Cell {self.position} does not currently have a device set."
            raise CellDeviceError(msg)
