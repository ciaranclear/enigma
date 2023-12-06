from enigma_core.plugboard.uhr_box_plugboard import UhrBoxPlugboard
from enigma_core.plugboard.uhr_box import UhrBox
from enigma_core.plugboard.exceptions import PlugIDError, SocketIDError
from enigma_core.settings.settings import LETTERS, NUMBERS
import unittest


class TestUhrBoxPlugboard(unittest.TestCase):

    def make_uhr_box_plugboard(self, char_set_flag='L'):
        """
        
        """
        return UhrBoxPlugboard(char_set_flag)
    
    def test_rotor_seting(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard()

        self.assertEqual(pb.rotor_setting, 0)

        pb.rotor_setting = 39

        self.assertEqual(pb.rotor_setting, 39)

    def test_connect_disconnect(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard()

        pb.connect("10A", "A")

        self.assertRaises(PlugIDError, pb.connect, "10C","A")

        self.assertRaises(SocketIDError, pb.connect, "10A","#")

        pb.disconnect("A")

    def test_is_connected(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard()

        pb.connect("10A", "A")

        self.assertEqual(pb.is_connected("A"), True)

        self.assertEqual(pb.is_connected("B"), False)

    def test_connected_plug(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard()

        pb.connect("10A", "A")

        self.assertEqual(pb.connected_plug("A"), "10A")

        self.assertEqual(pb.connected_plug("B"), None)

    def test_connected_to(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard()

        pb.connect("10A", "A")

    def test_number_of_connected(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard()

        pb.connect("10A", "A")

    def test_clear(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        charset = [chr(i) for i in range(65, 91)]

        conns = []

        for i in range(10):
            conns.append([UhrBox.PLUG_A_IDS[i], charset.pop()])
            conns.append([UhrBox.PLUG_B_IDS[i], charset.pop()])

        self.assertEqual(pb.number_of_connected(), 0)

        for conn in conns:
            pb.connect(*conn)

        self.assertEqual(pb.number_of_connected(), 20)

        pb.clear()

        self.assertEqual(pb.number_of_connected(), 0)

    def test_make_connections(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        charset = [chr(i) for i in range(65, 91)]

        conns = {}

        for i in range(10):
            conns[UhrBox.PLUG_A_IDS[i]] = charset.pop()
            conns[UhrBox.PLUG_B_IDS[i]] = charset.pop()

        self.assertEqual(pb.number_of_connected(), 0)

        pb.make_connections(conns)

        self.assertEqual(pb.number_of_connected(), 20)

        pb.clear()

        self.assertEqual(pb.number_of_connected(), 0)

    def test_valid_socket_id(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        self.assertEqual(pb.valid_socket_id('A'), 'A')

        self.assertRaises(SocketIDError, pb.valid_socket_id, '#')

        pb = self.make_uhr_box_plugboard('N')

        self.assertEqual(pb.valid_socket_id('01'), '01')

        self.assertRaises(SocketIDError, pb.valid_socket_id, '#')

    def test_valid_plug_id(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        self.assertEqual(pb.valid_plug_id('10A'), '10A')

        self.assertRaises(PlugIDError, pb.valid_plug_id, '#')

    def test_character_set(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        self.assertEqual(pb.character_set_flag, 'L')

        self.assertEqual(pb.character_set, LETTERS)

        pb.character_set_flag = 'N'

        self.assertEqual(pb.character_set_flag, 'N')

        self.assertEqual(pb.character_set, NUMBERS)

    def test_valid_plugboard(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        charset = [chr(i) for i in range(65, 91)]

        conns = {}

        for i in range(10):
            conns[UhrBox.PLUG_A_IDS[i]] = charset.pop()
            conns[UhrBox.PLUG_B_IDS[i]] = charset.pop()

        self.assertEqual(pb.number_of_connected(), 0)

        self.assertEqual(pb.valid_plugboard(), True)

        pb.make_connections(conns)

        self.assertEqual(pb.valid_plugboard(), True)

    def test_settings(self):
        """
        
        """
        pb = self.make_uhr_box_plugboard('L')

        charset = [chr(i) for i in range(65, 91)]

        conns = {}

        for i in range(10):
            conns[UhrBox.PLUG_A_IDS[i]] = charset.pop()
            conns[UhrBox.PLUG_B_IDS[i]] = charset.pop()

        pb.make_connections(conns)

        