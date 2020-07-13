import unittest
from rotor import Rotor,\
					RotorCharacterSetCharacterError,\
					RotorCharacterSetValueError,\
					RotorCharacterSetRepeatedError,\
					RotorCharacterSetTypeError
"""
To run test in command line type
python -m unittest test_rotor.py

    @classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp():
		pass

	def tearDown():
		pass

	def test_function(self):
		self.assertEqual(self.instance.prop, correct_result)
"""


class TestRotor(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		self.rotor = Rotor()

	def tearDown(self):
		pass

	def test_rotor_chars(self):
		self.rotor.set_rotor_chars(["A","B","C","D"])
		self.assertEqual(self.rotor.get_rotor_chars(), ["A","B","C","D"])		
		self.assertRaises(RotorCharacterSetCharacterError, self.rotor.set_rotor_chars, ["A","B","CC","D"])
		self.assertRaises(RotorCharacterSetValueError, self.rotor.set_rotor_chars, ["A",1,"B","C"])
		self.assertRaises(RotorCharacterSetRepeatedError, self.rotor.set_rotor_chars, ["A","B","C","C","D","D"])
		self.assertRaises(RotorCharacterSetTypeError, self.rotor.set_rotor_chars, ("A","B","C","D"))

if __name__ == "__main__":

	unittest.main()