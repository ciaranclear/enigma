import unittest
from enigma_core.scrambler.devices.reflector.reflector import Reflector
from enigma_core.scrambler.devices.validators.valid_wiring import WiringError


class TestReflector(unittest.TestCase):

    def test_pass(self):
        """
        This is a passing test with a valid wiring list.
        """
        reflector_id = "TEST_REFLECTOR"

        wire_list = [
            'B','C','D','E','F','G',
            'H','I','J','K','L','M',
            'N','O','P','Q','R','S',
            'T','U','V','W','X','Y',
            'Z','A'
        ]

        char_flag = 'L'

        params = [reflector_id, wire_list, char_flag]

        Reflector(*params)

    def test_incorrect_wire_list_type(self):
        """
        This is a failing test for incorrect wire list type.
        """
        reflector_id = "TEST_REFLECTOR"

        wire_list = {}

        char_flag = 'L'

        params = [reflector_id, wire_list, char_flag]

        try:
            Reflector(*params)
        except WiringError as e:
            self.assertEqual(e.error_code, 1)

    def test_incorrect_wire_list_length(self):
        """
        This is a failing test for incorrect wire list length.
        """
        reflector_id = "TEST_REFLECTOR"

        wire_list = [
            'B','C','D','E','F','G',
            'H','I','J','K','L','M',
            'N','O','P','Q','R','S',
            'T','U','V','W','X','Y',
            'Z'
        ]

        char_flag = 'L'

        params = [reflector_id, wire_list, char_flag]

        try:
            Reflector(*params)
        except WiringError as e:
            self.assertEqual(e.error_code, 2)

    def test_bad_wire_character(self):
        """
        This is a failing test for an invalid wire character.
        """
        reflector_id = "TEST_REFLECTOR"

        wire_list = [
            'B','C','D','E','F','G',
            'H','I','J','K','L','M',
            'N','O','P','Q','R','S',
            'T','U','V','W','X','Y',
            'Z','#'
        ]

        char_flag = 'L'

        params = [reflector_id, wire_list, char_flag]

        try:
            Reflector(*params)
        except WiringError as e:
            self.assertEqual(e.error_code, 3)

    def test_repeated_wire_list_character(self):
        """
        This is a failing test for a repeated wire character.
        """
        reflector_id = "TEST_REFLECTOR"

        wire_list = [
            'B','C','D','E','F','G',
            'H','I','J','K','L','M',
            'N','O','P','Q','R','S',
            'T','U','V','W','X','Y',
            'A','A'
        ]

        char_flag = 'L'

        params = [reflector_id, wire_list, char_flag]

        try:
            Reflector(*params)
        except WiringError as e:
            self.assertEqual(e.error_code, 4)

    def test_self_wired(self):
        """
        This is a failing test for a self wired terminal.
        """
        reflector_id = "TEST_REFLECTOR"

        wire_list = [
            'A','C','D','E','F','G',
            'H','I','J','K','L','M',
            'N','O','P','Q','R','S',
            'T','U','V','W','X','Y',
            'Z','B'
        ]

        char_flag = 'L'

        params = [reflector_id, wire_list, char_flag]

        try:
            Reflector(*params)
        except WiringError as e:
            self.assertEqual(e.error_code, 5)
