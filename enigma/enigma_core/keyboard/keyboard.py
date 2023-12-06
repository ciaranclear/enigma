from enigma_core.settings.settings import LETTERS


class Keyboard:

    def __init__(self) -> None:
        """

        """
        self._translation_map = {}
        self._make_translation_map()

    def __repr__(self) -> str:
        """

        """
        kb_str = ""
        for k, v in self._translation_map.items():
            kb_str += f"{k} -> {v}"
        return kb_str

    def integer_input(self, index: int) -> int:
        """

        """
        if not isinstance(index, int):
            raise TypeError(f"")
        if not (index < 26 and index >= 0):
            msg = "Invalid keyboard integer input!. "
            msg += f"{index} is not a valid keyboard input. Must be 0-25"
            raise ValueError(msg)
        return index

    def character_input(self, char: str) -> str:
        """

        """
        try:
            char = self._translation_map[char.upper()]
            char = LETTERS.index(char)
        except KeyError:
            msg = "Invalid keyboard character input!. "
            msg += f"{char} is not a valid enigma character. Must ne a-zA-Z0-9"
            raise ValueError(msg)
        else:
            return char

    def clean_input_string(self, input_string: str) -> str:
        """

        """
        clean_str = ""
        for char in input_string:
            char = char.upper()
            if char in self._translation_map:
                clean_str += char
        return clean_str

    def _make_translation_map(self) -> None:
        """

        """
        self._translation_map = {
            '0':'P','1':'Q',
            '2':'W','3':'E',
            '4':'R','5':'T',
            '6':'Z','7':'U',
            '8':'I','9':'O'
            }
        for l in LETTERS:
            self._translation_map[l] = l
