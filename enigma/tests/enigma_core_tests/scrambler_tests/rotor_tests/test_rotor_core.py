import unittest
from enigma_core.scrambler.devices.rotor.rotor import Rotor
from enigma_core.scrambler.devices.rotor.rotor_core import RotorInputIndexError
from enigma_core.settings.settings import LETTERS, NUMBERS


class TestRotorCore(unittest.TestCase):

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
    
    def test_wiring_characters_function(self):
        """
        Test wiring_characters function.
        """
        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Z'
        ]

        rotor = self.make_rotor(wire_list=wire_list)

        self.assertEqual(rotor.core.wiring_characters, wire_list)

    def test_rotor_dict(self):
        """
        Test rotor_dict function.
        """
        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Z'
        ]

        rotor = self.make_rotor(wire_list=wire_list)

        rotor_dict = rotor.core.rotor_dict

        rd = {
            "ROTOR_TYPE": "TEST_ROTOR",
            "ROTOR_SETTING": "A",
            "RING_SETTING": "A",
            "RING_CHARACTERS": LETTERS,
            "WIRING_CHARACTERS": wire_list,
            "TURNOVER_CHARACTERS": []
        }

        self.assertEqual(rotor_dict, rd)

    def test_output_index(self):
        """
        This is a failing test for an invalid rotro core input index.
        """
        rotor = self.make_rotor()

        self.assertRaises(RotorInputIndexError, rotor.core.lh_output, 26)
        self.assertRaises(RotorInputIndexError, rotor.core.lh_output, -1)
        self.assertRaises(RotorInputIndexError, rotor.core.rh_output, 26)
        self.assertRaises(RotorInputIndexError, rotor.core.rh_output, -1)

    def test_current_wiring(self):
        """
        Tests that the correct wiring list is returned.
        """
        wire_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Z'
        ]

        rotor = self.make_rotor(wire_list=wire_list)

        self.assertEqual(rotor.core.current_wiring_characters(), wire_list)