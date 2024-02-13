"""
ENIGMA DESCRIPTION
"""

from typing import Dict, List, Optional
from enigma_core.settings.settings import LETTERS
from enigma_core.keyboard.keyboard import Keyboard
from enigma_core.scrambler.scrambler.scrambler import Scrambler
from enigma_core.plugboard.stecker_plugboard import SteckerPlugboard
from enigma_core.plugboard.uhr_box_plugboard import UhrBoxPlugboard

ROTORS = Dict[str, Dict[str, List[str]]]
REFLECTORS = Dict[str, List[str]]

class Enigma:

    def __init__(self,
            machine_type: str,
            scrambler_char_flag: Optional[str]='L',
            plugboard_char_flag: Optional[str]='L',
            plugboard_mode: Optional[str]='S'
        ) -> None:

        self.machine_type = machine_type
        self.keyboard = Keyboard()
        self.scrambler = Scrambler(machine_type, scrambler_char_flag)
        self.plugboard = None
        self.set_plugboard_mode(plugboard_mode)

    def __str__(self) -> str:
        _str = f"{' '*16}{self.machine_type}\n\n"
        _str += self.scrambler.__str__()
        _str += '\n\n'
        _str += self.plugboard.__str__()
        _str += '\n'
        return _str

    def set_plugboard_mode(self, mode, plugboard_char_flag='L'):
        if mode == 'S' : self.plugboard = SteckerPlugboard(plugboard_char_flag)
        elif mode == 'U' : self.plugboard = UhrBoxPlugboard(plugboard_char_flag)
        else:
            msg = f"{mode} is not a valid plugboard mode. Must be 'S' or 'U'"
            raise ValueError(msg)

    def character_input(self, char: str) -> Optional[str]:
        """

        """
        try:
            index = self.keyboard.character_input(char)
        except ValueError:
            return None
        else:
            index = self.integer_input(index)
            return LETTERS[index]
        
    def non_keyed_input(self, char: str) -> Optional[str]:
        """
        
        """
        try:
            index = self.keyboard.character_input(char)
        except ValueError:
            return None
        else:
            index = self.plugboard.lg_contact_output(index)
            index = self.scrambler.output(index)                
            index = self.plugboard.sm_contact_output(index)    
            return LETTERS[index]

    def integer_input(self, index: int) -> int:
        """

        """
        index = self.plugboard.lg_contact_output(index)
        index = self.scrambler.keyed_input(index)
        index = self.plugboard.sm_contact_output(index)
        return index

    def valid_enigma(self) -> bool:
        """

        """
        return self.scrambler.valid_scrambler() and self.plugboard.valid_plugboard()

    def set_default_settings(self) -> None:
        """

        """
        self.scrambler.default_settings()
        self.plugboard.clear()

    @property
    def settings(self) -> Dict:
        """

        """
        d1 = self.scrambler.settings
        d2 = self.plugboard.settings
        d1.update(d2)
        d1["machine_type"] = self.machine_type
        return d1

    @settings.setter
    def settings(self, settings: Dict) -> None:
        """
        
        """
        #self.scrambler.clear_scrambler()
        self.scrambler.settings = settings
        try:
            self.set_plugboard_mode(settings['plugboard_mode'])
        except KeyError:
            pass
        else:
            self.plugboard.settings = settings

