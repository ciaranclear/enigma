import unittest
from enigma_core.scrambler.devices.rotor.rotor import Rotor
from enigma_core.scrambler.devices.validators.valid_wiring import WiringError
from enigma_core.scrambler.devices.validators.valid_turnover import TurnoverListError
from enigma_core.settings.settings import LETTERS, NUMBERS


class TestRotor(unittest.TestCase):

    def make_rotor(self, rotor_id="TEST_ROTOR", wire_list=None, turn_list=None, char_set_flag='L'):
        """
        Initializes an enigma machine with the parameters provided or with a
        default parameter if none is provided. Returns the enigma machine
        instance.        
        """
        if wire_list == None:
            wire_list = [
                'A','B','C','D','E','F',
                'G','H','I','J','K','L',
                'M','N','O','P','Q','R',
                'S','T','U','V','W','X',
                'Y','Z'
            ]

        if turn_list == None:
            turn_list = []

        rotor = Rotor(rotor_id, wire_list, turn_list, char_set_flag)

        return rotor

    # ROTOR TESTS

    def test_rotor(self):
        """
        This is a passing rotor test
        """

        rotor_id = "TEST_ROTOR"

        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Z'
        ]

        turn_list = ['Q','Z']

        Rotor(rotor_id, wire_list, turn_list, 'L')

    def test_incorrect_wire_list_type(self):
        """
        This is a failing test for incorrect wire list type.
        """
        wire_list = {}

        try:
            self.make_rotor(wire_list=wire_list)
        except WiringError as e:
            self.assertEqual(e.error_code, 1)

    def test_incorrect_wire_list_length(self):
        """
        This is a failing test for incorrect wire list length.
        """
        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y'
        ]

        try:
            self.make_rotor(wire_list=wire_list)
        except WiringError as e:
            self.assertEqual(e.error_code, 2)

    def test_bad_wire_character(self):
        """
        This is a failing test for an invalid wire character.
        """
        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','#'
        ]

        try:
            self.make_rotor(wire_list=wire_list)
        except WiringError as e:
            self.assertEqual(e.error_code, 3)

    def test_repeated_wire_list_character(self):
        """
        This is a failing test for a repeated wire character.
        """
        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Y'
        ]

        try:
            self.make_rotor(wire_list=wire_list)
        except WiringError as e:
            self.assertEqual(e.error_code, 4)

    def test_invalid_turnover_character(self):
        """
        This is a failing test for an invalid turnover character.
        """
        rotor_id = "TEST_ROTOR"

        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Z'
        ]

        turn_list = ['Q','#']

        char_flag = 'L'

        params = [rotor_id, wire_list, turn_list, char_flag]

        self.assertRaises(TurnoverListError, Rotor, *params)

    def test_turnover_flag(self):
        """
        This is a test to assert that a "R_ROT" flag is produced when the rotor
        object is initialized with a non empty turnover list and that a "F_ROT"
        flag is produced when the rotor object is initialized with an empty
        turnover list.        
        """
        turn_list = ['Q','Z']

        rotor = self.make_rotor(turn_list=turn_list)

        self.assertEqual(rotor.flag, "R_ROT")

        turn_list = []

        rotor = self.make_rotor(turn_list=turn_list)

        self.assertEqual(rotor.flag, "F_ROT")

    def test_rotor_returns_turnover_characters(self):
        """
        Test the rotor turnover property returns a turnover list.
        """
        turn_list = ['Q','Z']

        rotor = self.make_rotor(turn_list=turn_list)

        # test for non empty turnover list
        self.assertEqual(rotor.turnover_characters, ['Q','Z'])

        turn_list = []

        rotor = self.make_rotor(turn_list=turn_list)

        # test for empty turnover list
        self.assertEqual(rotor.turnover_characters, [])

    def test_can_turnover_function(self):
        """
        Tests that the can_turnover function returns the correct turnover
        boolean value.
        """
        turn_list = ['Q','Z']

        rotor = self.make_rotor(turn_list=turn_list)

        # test for non empty turnover list
        self.assertEqual(rotor.can_turnover(), True)

        turn_list = []

        rotor = self.make_rotor(turn_list=turn_list)

        # test for empty turnover list
        self.assertEqual(rotor.can_turnover(), False)

    def test_on_turnover_function(self):
        """
        Test that the on_turnover function return the correct boolean
        value.
        """
        turn_list = ['A']

        rotor = self.make_rotor(turn_list=turn_list)

        # test for True output
        self.assertEqual(rotor.on_turnover(), True)

        turn_list = ['Q','Z']

        rotor = self.make_rotor(turn_list=turn_list)

        # test for False output
        self.assertEqual(rotor.on_turnover(), False)

    def test_keyed_rotor_function(self):
        """
        Test that the rotro turns over.
        """
        turn_list = ['A']

        rotor = self.make_rotor(turn_list=turn_list)

        # test for True output
        self.assertEqual(rotor.keyed_rotor(), True)

        # test for False output
        self.assertEqual(rotor.keyed_rotor(), False)
