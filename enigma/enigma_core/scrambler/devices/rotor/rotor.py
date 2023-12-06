from typing import Optional, List
from enigma_core.scrambler.devices.rotor.rotor_ring import RotorRing
from enigma_core.scrambler.devices.rotor.rotor_core import RotorCore
from enigma_core.scrambler.devices.validators.valid_turnover import TurnoverListDescriptor


class Rotor(RotorRing):
    """
    
    """

    POSITIONS = 26
    _turn_chars = TurnoverListDescriptor()

    def __init__(self,
            device_id: str,
            wiring_characters: List[str],
            turnover_characters: Optional[List[str]]=None,
            charset_flag: str='L'
        ) -> None:
        """
        Takes a string value for the rotor id, wiring characters list, 
        optional turnover characters list and optional character set flag
        of 'L' or 'N' defaults to 'L'.
        """
        self.core = RotorCore(self, device_id, wiring_characters, charset_flag)
        self._rng_offset = 0
        self._rot_offset = 0
        self._turn_chars = turnover_characters or []
        self._charset_flag: Optional[str] = None
        self._charset: Optional[List[str]] = None
        self.character_set_flag = charset_flag

    def __repr__(self) -> str:
        """
        Returns the string repressentation of the rotor core.
        """
        return self.core.__repr__()

    def __str__(self) -> str:
        """
        Returns the string repressentation of the rotor core.
        """
        return self.core.__str__()

    @property
    def device_id(self) -> str:
        """
        Returns the device id from the rotor core.
        """
        return self.core._device_id

    @property
    def rotor_id(self) -> str:
        """
        Returns the device id from the rotor core.
        """
        return self.core._device_id

    @property
    def flag(self) -> str:
        """
        Returns the rotating rotor 'R_ROT' or fixed rotor 'F_ROT' flag for 
        this rotor.
        """
        return "R_ROT" if self.can_turnover() else "F_ROT"

    @property
    def turnover_characters(self) -> List[str]:
        """
        Returns a list of turnover characters or an empty list if no turnover.
        """
        return [self._charset[i] for i in self._turn_chars]

    def can_turnover(self) -> bool:
        """
        Returns a boolean value indicating if the rotor can be turned over
        by the stepping mechanism for the current rotor setting.
        """
        return True if len(self._turn_chars) != 0 else False

    def on_turnover(self) -> bool:
        """
        Returns a boolean reflecting if the rotor is at a rotor setting which
        will allow it to turn over.
        """
        return True if self.rotor_setting in self.turnover_characters else False

    def keyed_rotor(self) -> bool:
        """
        Increments the the rotor setting one step and returns the on_turnover
        state before the rotor setting was incremented.
        """
        turnover = self.on_turnover()
        self.inc_rotor_setting()
        return turnover
    