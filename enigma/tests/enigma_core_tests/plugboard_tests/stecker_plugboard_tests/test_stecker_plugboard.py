import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.plugboard.stecker_plugboard import SteckerPlugboard
from enigma_core.plugboard.exceptions import SocketIDError


class TestSteckerPlugboard(unittest.TestCase):

    def make_plugboard(self, char_set_flag='L'):
        """
        
        """
        return SteckerPlugboard(char_set_flag)
    
    def test_connect(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A','B')

    def test_disconnect(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A','B')
        pb.disconnect('A')

    def test_is_connected(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A', 'B')

        self.assertEqual(pb.is_connected('A'), True)
        self.assertEqual(pb.is_connected('B'), True)
        self.assertEqual(pb.is_connected('C'), False)

    def test_connected_to(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A', 'B')

        self.assertEqual(pb.connected_to('A'), 'B')
        self.assertNotEqual(pb.connected_to('A'), 'C')

    def test_clear_plugboard(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A', 'B')

        self.assertEqual(pb.connected_to('A'), 'B')

        pb.clear()

        self.assertEqual(pb.connected_to('A'), 'A')

    def test_number_of_connections(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A', 'B')

        self.assertEqual(pb.number_of_connections(), 2)


    def test_connected(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A', 'B')
        pb.connect('C', 'D')

        self.assertEqual(len(pb.connected()), 2)

    def test_unconnected(self):
        """
        
        """
        pb = self.make_plugboard('L')

        pb.connect('A', 'B')

        self.assertEqual(len(pb.unconnected()), 24)

    def test_make_connections(self):
        """
        
        """
        pb = self.make_plugboard('L')

        conns = [[LETTERS[i], LETTERS[i+1]] for i in range(0, 26, 2)]

        for conn in conns:
            pb.connect(*conn)

        self.assertEqual(pb.number_of_connections(), 26)

        pb.clear()

        self.assertEqual(pb.number_of_connections(), 0)

    def test_valid_socket_id(self):
        """
        
        """
        pb = self.make_plugboard('L')

        self.assertEqual(pb.valid_socket_id('A'), 'A')

        self.assertRaises(SocketIDError, pb.valid_socket_id, '01')

    def test_valid_plugboard(self):
        """
        
        """
        pb = self.make_plugboard('L')

        conns = [[LETTERS[i], LETTERS[i+1]] for i in range(0, 26, 2)]

        for conn in conns:
            pb.connect(*conn)

        self.assertEqual(pb.valid_plugboard(), True)

        pb.clear()

        self.assertEqual(pb.valid_plugboard(), True)

    def test_settings(self):
        """
        
        """
        pb = self.make_plugboard('L')

        conns = [[LETTERS[i], LETTERS[i+1]] for i in range(0, 26, 2)]

        settings = {
            "connections":conns,
            "character_set_flag":'L'
        }

        pb.settings = settings

        settings = pb.settings

    def test_character_set(self):
        """
        
        """
        pb = self.make_plugboard('L')

        self.assertEqual(pb.character_set, LETTERS)

        self.assertEqual(pb.character_set_flag, 'L')

        pb.character_set_flag = 'N'

        self.assertEqual(pb.character_set, NUMBERS)

        self.assertEqual(pb.character_set_flag, 'N')
