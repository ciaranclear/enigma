from typing import Optional, List
from collections import deque
from enigma_core.scrambler.devices.device_base.device_base import DeviceBase
from enigma_core.scrambler.exceptions.exceptions import RingCharacterError


class RotorRing(DeviceBase):

    def __init__(self):
        pass

    @property
    def ring_characters(self) -> List[str]:
        """
        Returns the ring characters list.
        """
        return self._charset

    @property
    def rotor_setting(self) -> str:
        """
        Returns the current rotor setting.
        """
        return self._charset[self._rot_offset]

    @rotor_setting.setter
    def rotor_setting(self, rotor_setting: str) -> None:
        """
        Takes a rotor setting and sets that value if valid.
        """
        rotor_setting = self.valid_ring_character(rotor_setting)
        self._rot_offset = self._charset.index(rotor_setting)

    @property
    def ring_setting(self) -> str:
        """
        Returns the current ring setting.
        """
        return self._charset[self._rng_offset]

    @ring_setting.setter
    def ring_setting(self, ring_setting: str) -> None:
        """
        Takes a ring setting and sets that value if valid.
        """
        ring_setting = self.valid_ring_character(ring_setting)
        self._rng_offset = self._charset.index(ring_setting)

    def valid_ring_character(self, character: str) -> str:
        """
        Returns a valid ring character or raises RotorRingCharacterError
        if not a valid ring character.
        """
        if character in self._charset:
            return character
        else:
            msg = f"{character} is not a valid ring character."
            raise RingCharacterError(msg)

    def inc_rotor_setting(self) -> None:
        """
        Increments the rotor setting by one step.
        """
        self._rot_offset = self._change_offset(self._rot_offset, 1)

    def dec_rotor_setting(self) -> None:
        """
        Decrements the rotor setting by one step.
        """
        self._rot_offset = self._change_offset(self._rot_offset, -1)

    def inc_ring_setting(self) -> None:
        """
        Increments the ring setting by one step.
        """
        self._rng_offset = self._change_offset(self._rng_offset, 1)

    def dec_ring_setting(self) -> None:
        """
        Decrements the ring setting by one step.
        """
        self._rng_offset = self._change_offset(self._rng_offset, -1)

    def reset_rotor(self) -> None:
        """
        Resets the ring and rotor settings to their default values
        which is the same values they had at rotor initialization.
        """
        self._rng_offset = 0
        self._rot_offset = 0

    def default_rotor_setting(self) -> None:
        """
        Resets rotor setting to its default value which is the value
        it had at rotor initialization.
        """
        self._rot_offset = 0

    def core_offset(self) -> int:
        """
        Returns the rotor core offset.
        """
        offset = self._rot_offset - self._rng_offset
        if offset < 0:
            offset = offset + 26
        return offset
    
    def current_ring_characters(self):
        """
        
        """
        ring_chars = deque(self._charset)
        ring_chars.rotate(self._rng_offset)
        ring_chars = list(ring_chars)
        return ring_chars

    def _change_offset(self, value: int, direction: int) -> int:
        """
        Returns a new offset value within the limits of the rotor positions.
        """
        if direction == 1:
            if value >= self.POSITIONS-1:
                value = 0
            else:
                value += 1
        elif direction == -1:
            if value == 0:
                value = self.POSITIONS-1
            else:
                value -= 1
        return value