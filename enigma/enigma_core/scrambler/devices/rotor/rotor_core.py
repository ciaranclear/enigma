from typing import Optional, Dict, List
from collections import deque
from enigma_core.settings.settings import LETTERS, NUMBERS
from enigma_core.scrambler.devices.validators.valid_wiring import WiringCharactersDescriptor
from enigma_core.scrambler.devices.device_base.device_base import DeviceBase
from enigma_core.scrambler.exceptions.exceptions import RotorInputIndexError


class RotorCore(DeviceBase):
    """
    
    """

    _wire_chars = WiringCharactersDescriptor(self_wired=True)

    def __init__(
            self, 
            rotor, 
            device_id: str, 
            wiring_characters: List[str], 
            charset_flag: Optional[str]='L'
        ) -> None:
        """
        
        """
        self._rotor = rotor
        self._device_id = device_id
        self._wire_chars = wiring_characters
        self._charset_flag = None
        self._charset: Optional[List[str]] = None
        self.character_set_flag: List[str] = charset_flag
        self._lh_translation_map: Dict[int, List[int]] = {}
        self._rh_translation_map: Dict[int, List[int]] = {}
        self._make_translation_maps()

    def __repr__(self) -> str:
        """
        Returns a string with the 'ROTOR_ID' 'RING CHARACTERS'
        'WIRING CHARACTERS' and 'TURNOVER CHARACTERS'. The parameters
        are the same as those used to initialize the rotor.
        """

        rot_str = (f"ROTOR ID : {self._device_id}\n"
                   f"RING CHARACTERS : {self._rotor.ring_characters}\n"
                   f"WIRING CHARACTERS : {self._wire_chars}\n"
                   f"TURNOVER CHARACTERS : {self._rotor.turnover_characters}\n")

        rot_str += "LH_TRANSLATION_TABLE\n"
        for position, translation in self._lh_translation_map.items():
            trans_str = ""
            for i in translation:
                trans_str += f"{LETTERS[i]} "
            rot_str += f"{str(position).rjust(2, '0')} {trans_str}\n"

        rot_str += "RH_TRANSLATION_TABLE\n"
        for position, translation in self._rh_translation_map.items():
            trans_str = ""
            for i in translation:
                trans_str += f"{LETTERS[i]} "
            rot_str += f"{str(position).rjust(2, '0')} {trans_str}\n"

        return rot_str

    def __str__(self) -> str:
        """
        Returns a string with the 'ROTOR ID' 'ROTOR SETTING'
        'RING SETTING' 'RING CHARACTERS' 'WIRING CHARACTERS'
        and 'TURNOVER CHARACTERS'. The rotor setting and ring
        setting are the current settings. The rest of the 
        parameters are the same as those used to initialize
        the rotor.
        """
        def list_to_string(list_):
            return ','.join(['{:<2}'.format(char) for char in list_])

        return (f"ROTOR ID -----------: {self._device_id}\n"
                f"ROTOR SETTING ------: {self._rotor.rotor_setting}\n"
                f"RING SETTING -------: {self._rotor.ring_setting}\n"
                f"RING CHARACTERS ----: {list_to_string(self._rotor.ring_characters)}\n"
                f"WIRING CHARACTERS --: {list_to_string(self.wiring_characters)}\n"
                f"TURNOVER CHARACTERS : {list_to_string(self._rotor.turnover_characters)}\n")

    @property
    def wiring_characters(self) -> List[str]:
        """
        Returns a list of the wiring characters.
        """
        char_map = { LETTERS[i] : self._charset[i] for i in range(26) }
        return [char_map[l] for l in self._wire_chars]

    @property
    def rotor_dict(self) -> Dict:
        """
        Returns a dictionary object with 'ROTOR_TYPE' 'ROTOR_SETTING'
        'RING_SETTING' 'RING_CHARACTERS' 'ROTOR_CHARACTERS' and
        'TURNOVER_CHARACTERS'. The ring characters list and rotor characters
        list are shifted to reflect there current values for the current ring
        and rotor settings.
        """
        return {
            "ROTOR_TYPE": self.device_id,
            "ROTOR_SETTING": self._rotor.rotor_setting,
            "RING_SETTING": self._rotor.ring_setting,
            "RING_CHARACTERS": self._rotor.current_ring_characters(),
            "WIRING_CHARACTERS": self.current_wiring_characters(),
            "TURNOVER_CHARACTERS": self._rotor.turnover_characters
            }

    def lh_output(self, index: int) -> int:
        """
        Returns an integer value for the output index for the left hand 
        output of the rotor core.
        """
        if self.valid_input_index(index):
            offset = self._rotor.core_offset()
            return self._lh_translation_map[offset][index]

    def rh_output(self, index: int) -> int:
        """
        Returns an integer value for the output index for the right hand
        output of the rotor core.
        """
        if self.valid_input_index(index):
            offset = self._rotor.core_offset()
            return self._rh_translation_map[offset][index]

    def valid_input_index(self, index: int) -> bool:
        """
        Takes an index integer value and returns True if valid else raises
        a RotorInputIndexError.
        """
        if index not in range(26):
            msg = f"{index} is not a valid index for rotor {self.device_id}"
            raise RotorInputIndexError(msg)
        else:
            return True

    def current_wiring_characters(self) -> List[str]:
        """
        Returns a list of wiring characters that are offset to the current 
        core offset.
        """
        char_map = { i : self._charset[i] for i in range(26) }
        return [char_map[i] for i in self._lh_translation_map[self._rotor.core_offset()]]

    def _make_translation_maps(self) -> None:
        """
        Makes the translation maps for left hand and right hand output.
        Each translation map maps rotor core position to an integer list
        of the output indexes for that rotor core position.
        """
        lh_translation_map = {}
        rh_translation_map = {}

        connections = deque(self._wire_chars)
        letters = deque(LETTERS)

        for i in range(26):
            lh_translation_arr = [letters.index(l) for l in connections]
            rh_translation_arr = [connections.index(l) for l in letters]
            lh_translation_map[i] = lh_translation_arr
            rh_translation_map[i] = rh_translation_arr
            connections.rotate(-1)
            letters.rotate(-1)
        self._lh_translation_map = lh_translation_map
        self._rh_translation_map = rh_translation_map