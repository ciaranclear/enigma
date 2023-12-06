import unittest
from enigma_core.scrambler.devices.rotor.rotor import Rotor
from enigma_core.scrambler.collection.collection import RingCharacterError
from enigma_core.settings.settings import LETTERS, NUMBERS


class TestRotorRing(unittest.TestCase):

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
    
    def test_ring_characters(self):
        """
        Tests that the rotor ring_character property returns the correct
        ring character list for the char_set_flag that the rotor was
        initialized with.
        """
        rotor = self.make_rotor(char_set_flag='L')

        # test for LETTERS character set with charset flag 'L'
        self.assertEqual(rotor.ring_characters, LETTERS)

        rotor = self.make_rotor(char_set_flag='N')

        # test for NUMBERS character set with charset flag 'N'
        self.assertEqual(rotor.ring_characters, NUMBERS)

    def test_rotor_setting_property(self):
        """
        Tests that the rotor_setting property returns the correct rotor setting
        value.
        """
        rotor = self.make_rotor()

        self.assertEqual(rotor.rotor_setting, 'A')

        rotor.inc_rotor_setting()

        self.assertEqual(rotor.rotor_setting, 'B')

    def test_rotor_setting_setter(self):
        """
        Test that the rotor_setting setter sets the correct rotor setting
        value.
        """
        rotor = self.make_rotor()

        rotor.rotor_setting = 'Z'

        self.assertEqual(rotor.rotor_setting, 'Z')

    def test_ring_setting_property(self):
        """
        Test that the ring_setting property returns the correct ring settting
        value.
        """
        rotor = self.make_rotor()

        self.assertEqual(rotor.ring_setting, 'A')

        rotor.inc_ring_setting()

        self.assertEqual(rotor.ring_setting, 'B')

    def test_ring_setting_setter(self):
        """
        
        """
        rotor = self.make_rotor()

        self.assertEqual(rotor.ring_setting, 'A')

        rotor.ring_setting = 'B'

        self.assertEqual(rotor.ring_setting, 'B')

    def test_valid_ring_character_function(self):
        """
        Test correct exception is raised for an invalid ring character.
        """
        rotor = self.make_rotor()

        self.assertRaises(RingCharacterError, rotor.valid_ring_character, '#')

    def test_inc_dec_rotor_setting_functions(self):
        """
        
        """
        rotor = self.make_rotor()

        rotor.inc_rotor_setting()

        self.assertEqual(rotor.rotor_setting, 'B')

        rotor.dec_rotor_setting()

        self.assertEqual(rotor.rotor_setting, 'A')

    def test_inc_dec_ring_setting_functions(self):
        """
        
        """
        rotor = self.make_rotor()

        rotor.inc_ring_setting()

        self.assertEqual(rotor.ring_setting, 'B')

        rotor.dec_ring_setting()

        self.assertEqual(rotor.ring_setting, 'A')

    def test_reset_rotor_function(self):
        """
        Test reset_rotor function.
        """
        rotor = self.make_rotor()

        rotor.rotor_setting = "Z"
        rotor.ring_setting = 'Z'

        rotor.reset_rotor()

        self.assertEqual(rotor.rotor_setting, 'A')
        self.assertEqual(rotor.ring_setting, 'A')

    def test_default_rotor_setting_function(self):
        """
        Test default_rotor_setting function.
        """
        rotor = self.make_rotor()

        rotor.rotor_setting = "Z"

        rotor.default_rotor_setting()

        self.assertEqual(rotor.rotor_setting, 'A')

    def test_core_offset_function(self):
        """
        Test core_offset function.
        """
        rotor = self.make_rotor()

        self.assertEqual(rotor.core_offset(), 0)