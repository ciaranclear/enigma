from typing import Optional, List
from enigma_core.settings.settings import LETTERS, NUMBERS
from enigma_core.scrambler.devices.validators.valid_wiring import WiringCharactersDescriptor
from enigma_core.scrambler.exceptions.exceptions import ReflectorIndexError
from enigma_core.scrambler.devices.device_base.device_base import DeviceBase


class Reflector(DeviceBase):
    """
    
    """

    _wire_chars = WiringCharactersDescriptor()

    def __init__(self, reflector_id: str, wiring_characters: List[str], charset_flag: Optional[str]='L') -> None:
        """

        """
        super(Reflector, self).__init__(reflector_id, charset_flag)
        self._reflector_id = reflector_id
        self._flag = "REF"
        self._translation_array = None
        self._wire_chars = wiring_characters
        self._make_translation_array()

    def __repr__(self) -> str:
        """
        Returns the string repressentation of the reflector.
        """
        #return self.__str__()
        return self.reflector_id

    def __str__(self) -> str:
        """
        Returns a string with the reflector id and wiring characters.
        """
        def list_to_string(list_):
            return ','.join(['{:<2}'.format(char) for char in list_])

        return (f"REFLECTOR_ID -------: {self.reflector_id}\n"
                f"WIRING CHARACTERS --: {list_to_string(self.wire_characters)}\n")

    @property
    def flag(self) -> str:
        """
        Returns the reflectors flag.
        """
        return self._flag

    @property
    def reflector_id(self) -> str:
        """
        Returns the device id.
        """
        return self._reflector_id

    @property
    def wire_characters(self) -> List[str]:
        """
        Returns the list of wiring characters.
        """
        return [self._charset[i] for i in self._translation_array]

    def output(self, index: int) -> int:
        """
        Takes an index integer and returns the output index integer from the
        translation array.
        """
        try:
            return self._translation_array[index]
        except IndexError:
            raise ReflectorIndexError(index)

    def _make_translation_array(self):
        """
        Makes the translation array to convert the reflector input index to
        an output index.
        """
        self._translation_array = [LETTERS.index(l) for l in self._wire_chars]

