import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.scrambler_validators import *


class TestScramblerValidators(unittest.TestCase):

    machines_list = EQUIPMENT_DICT.keys()

    def test_valid_reflector(self):
        """
        
        """

        for machine in self.machines_list:
            reflectors_list = EQUIPMENT_DICT[machine]["REFLECTORS"].keys()

            for reflector in reflectors_list:
                self.assertEqual(reflector, ScramblerValidators.valid_reflector_type(machine, reflector))
                self.assertEqual(reflector, ScramblerValidators.valid_reflector_type(machine, reflector.lower()))

                with self.assertRaises(ReflectorTypeError):
                    ScramblerValidators.valid_reflector_type(machine, "invalid_reflector")

    def test_valid_rotor_types(self):
        """
        
        """
        params = {
            "WEHRMACHT":{
                "PASS":[
                    ["III II I",{"RS":"III","RM":"II","RF":"I"}],
                    ["iii ii i",{"RS":"III","RM":"II","RF":"I"}], 
                    ["II_III_I",{"RS":"II","RM":"III","RF":"I"}],
                    ["[I II III]",{"RS":"I","RM":"II","RF":"III"}],
                    ["I,II,III",{"RS":"I","RM":"II","RF":"III"}]
                ],
                "FAIL":["I I II", "IV III II I"]
            },
            "LUFTWAFFE":{
                "PASS":[
                    ["III II I",{"RS":"III","RM":"II","RF":"I"}],
                    ["iii ii i",{"RS":"III","RM":"II","RF":"I"}], 
                    ["II_III_I",{"RS":"II","RM":"III","RF":"I"}],
                    ["[I II III]",{"RS":"I","RM":"II","RF":"III"}],
                    ["I,II,III",{"RS":"I","RM":"II","RF":"III"}]
                ],
                "FAIL":[]
            },
            "ENIGMA M3 Kriegsmarine":{
                "PASS":[
                    ["III II I",{"RS":"III","RM":"II","RF":"I"}],
                    ["iii ii i",{"RS":"III","RM":"II","RF":"I"}], 
                    ["II_III_I",{"RS":"II","RM":"III","RF":"I"}],
                    ["[I II III]",{"RS":"I","RM":"II","RF":"III"}],
                    ["I,II,III",{"RS":"I","RM":"II","RF":"III"}]
                ],
                "FAIL":[]
            },
            "ENIGMA M4 u-boat":{
                "PASS":[
                    ["Gamma III II I",{"R4":"Gamma","RS":"III","RM":"II","RF":"I"}],
                    ["Beta iii ii i",{"R4":"Beta","RS":"III","RM":"II","RF":"I"}], 
                    ["Gamma II_III_I",{"R4":"Gamma","RS":"II","RM":"III","RF":"I"}],
                    ["[Beta I II III]",{"R4":"Beta","RS":"I","RM":"II","RF":"III"}],
                    ["Gamma I,II,III",{"R4":"Gamma","RS":"I","RM":"II","RF":"III"}]
                ],
                "FAIL":[]
            }
        }

        for machine in self.machines_list:
            rotors = EQUIPMENT_DICT[machine]["ROTORS"]
            cells_map = EQUIPMENT_DICT[machine]["CELLS_MAP"]

            passing_list = params[machine]["PASS"]
            for passing in passing_list:
                self.assertEqual(passing[1], ScramblerValidators.valid_rotor_types(machine, passing[0]))

            failing_list = params[machine]["FAIL"]
        


    def test_valid_rotor_settings(self):
        """
        
        """
        passing = [
            {"input":"a a a","output":{"RS":"A","RM":"A","RF":"A"},"charset_flag":"L","positions":3},
            {"input":"a a a a","output":{"R4":"A","RS":"A","RM":"A","RF":"A"},"charset_flag":"L","positions":4},
            {"input":"01 02 03 04","output":{"R4":"01","RS":"02","RM":"03","RF":"04"},"charset_flag":"N","positions":4},
            {"input":"01 02 03 04","output":{"R4":"01","RS":"02","RM":"03","RF":"04"},"charset_flag":"n","positions":4}
        ]
        failing = [
            {"input":"a a a","output":{"RS":"A","RM":"A","RF":"A"},"charset_flag":"L","positions":4},
            {"input":"a a a","output":{"RS":"B","RM":"A","RF":"A"},"charset_flag":"L","positions":4},
            {"input":"a a a","output":{"RS":"A","RM":"A","RF":"A"},"charset_flag":"N","positions":4},
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output"], ScramblerValidators.valid_rotor_settings(test_dict["input"], test_dict["charset_flag"], test_dict["positions"]))

        for test_dict in failing:
            with self.assertRaises(RotorSettingsError):
                ScramblerValidators.valid_rotor_settings(test_dict["input"], test_dict["charset_flag"], test_dict["positions"])

    def test_valid_ring_settings(self):
        """
        
        """
        passing = [
            {"input":"a a a","output":{"RS":"A","RM":"A","RF":"A"},"charset_flag":"L","positions":3},
            {"input":"a a a a","output":{"R4":"A","RS":"A","RM":"A","RF":"A"},"charset_flag":"L","positions":4},
            {"input":"01 02 03 04","output":{"R4":"01","RS":"02","RM":"03","RF":"04"},"charset_flag":"N","positions":4},
            {"input":"01 02 03 04","output":{"R4":"01","RS":"02","RM":"03","RF":"04"},"charset_flag":"n","positions":4}
        ]
        failing = [
            {"input":"a a a","output":{"RS":"A","RM":"A","RF":"A"},"charset_flag":"L","positions":4},
            {"input":"a a a","output":{"RS":"B","RM":"A","RF":"A"},"charset_flag":"L","positions":4},
            {"input":"a a a","output":{"RS":"A","RM":"A","RF":"A"},"charset_flag":"N","positions":4},
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output"], ScramblerValidators.valid_ring_settings(test_dict["input"], test_dict["charset_flag"], test_dict["positions"]))

        for test_dict in failing:
            with self.assertRaises(RotorSettingsError):
                ScramblerValidators.valid_ring_settings(test_dict["input"], test_dict["charset_flag"], test_dict["positions"])

    def test_valid_rotor_types_dict(self):
        """
        
        """
        passing = [
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"III",
                    "RM":"II",
                    "RF":"I"
                },
                "output_dict":{
                    "RS":"III",
                    "RM":"II",
                    "RF":"I",
                    "REF":None
                },
                "check_positions":["RS","RM","RF"]
            },
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"iii",
                    "RM":"ii",
                    "RF":"i"
                },
                "output_dict":{
                    "RS":"III",
                    "RM":"II",
                    "RF":"I",
                    "REF":None
                },
                "check_positions":["RS","RM","RF"]
            }
        ]

        failing = [
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"III",
                    "RM":"III",
                    "RF":"I"
                },
                "check_positions":[]
            }
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output_dict"], ScramblerValidators.valid_scrambler_types_dict(test_dict["machine"], test_dict["input_dict"], test_dict["check_positions"]))

        for test_dict in failing:
            with self.assertRaises(ScramblerTypesDictError):
                ScramblerValidators.valid_scrambler_types_dict(test_dict["machine"], test_dict["input_dict"], test_dict["check_positions"])

    def test_valid_rotor_settings_dict(self):
        """
        
        """
        passing = [
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"A",
                    "RM":"B",
                    "RF":"C"
                },
                "output_dict":{
                    "RS":"A",
                    "RM":"B",
                    "RF":"C"
                },
                "charset_flag":"L",
                "check_positions":[]
            },
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"01",
                    "RM":"02",
                    "RF":"03"
                },
                "output_dict":{
                    "RS":"01",
                    "RM":"02",
                    "RF":"03"
                },
                "charset_flag":"N",
                "check_positions":[]
            },
            {
                "machine":None,
                "input_dict":{
                    "rs":"a",
                    "rm":"b",
                    "rf":"c"
                },
                "output_dict":{
                    "RS":"A",
                    "RM":"B",
                    "RF":"C"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":None,
                "input_dict":{
                    "r4":"a",
                    "rs":"b",
                    "rm":"c",
                    "rf":"d"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C",
                    "RF":"D"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"a",
                    "rs":"b",
                    "rm":"c",
                    "rf":"d"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C",
                    "RF":"D"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"a",
                    "rm":"c",
                    "rs":"b",
                    "rf":"d"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C",
                    "RF":"D"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"01",
                    "rs":"02",
                    "rm":"03",
                    "rf":"04"
                },
                "output_dict":{
                    "R4":"01",
                    "RS":"02",
                    "RM":"03",
                    "RF":"04"
                },
                "charset_flag":"n",
                "check_positions":None
            }
        ]

        failing = [
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"A",
                    "RM":"A",
                    "RF":"A"
                },
                "charset_flag":"N",
                "check_positions":[]
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"a",
                    "rs":"b",
                    "rm":"c"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C"
                },
                "charset_flag":"l",
                "check_positions":None
            }
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output_dict"], ScramblerValidators.valid_rotor_settings_dict(test_dict["input_dict"], test_dict["charset_flag"], test_dict["machine"], test_dict["check_positions"]))

        for test_dict in failing:
            with self.assertRaises(RotorSettingsError):
                ScramblerValidators.valid_rotor_settings_dict(test_dict["input_dict"], test_dict["charset_flag"], test_dict["machine"], test_dict["check_positions"])

    def test_valid_ring_settings_dict(self):
        """
        
        """
        passing = [
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"A",
                    "RM":"B",
                    "RF":"C"
                },
                "output_dict":{
                    "RS":"A",
                    "RM":"B",
                    "RF":"C"
                },
                "charset_flag":"L",
                "check_positions":[]
            },
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"01",
                    "RM":"02",
                    "RF":"03"
                },
                "output_dict":{
                    "RS":"01",
                    "RM":"02",
                    "RF":"03"
                },
                "charset_flag":"N",
                "check_positions":[]
            },
            {
                "machine":None,
                "input_dict":{
                    "rs":"a",
                    "rm":"b",
                    "rf":"c"
                },
                "output_dict":{
                    "RS":"A",
                    "RM":"B",
                    "RF":"C"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":None,
                "input_dict":{
                    "r4":"a",
                    "rs":"b",
                    "rm":"c",
                    "rf":"d"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C",
                    "RF":"D"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"a",
                    "rs":"b",
                    "rm":"c",
                    "rf":"d"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C",
                    "RF":"D"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"a",
                    "rm":"c",
                    "rs":"b",
                    "rf":"d"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C",
                    "RF":"D"
                },
                "charset_flag":"l",
                "check_positions":None
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"01",
                    "rs":"02",
                    "rm":"03",
                    "rf":"04"
                },
                "output_dict":{
                    "R4":"01",
                    "RS":"02",
                    "RM":"03",
                    "RF":"04"
                },
                "charset_flag":"n",
                "check_positions":None
            }
        ]

        failing = [
            {
                "machine":"WEHRMACHT",
                "input_dict":{
                    "RS":"A",
                    "RM":"A",
                    "RF":"A"
                },
                "charset_flag":"N",
                "check_positions":[]
            },
            {
                "machine":"ENIGMA M4 u-boat",
                "input_dict":{
                    "r4":"a",
                    "rs":"b",
                    "rm":"c"
                },
                "output_dict":{
                    "R4":"A",
                    "RS":"B",
                    "RM":"C"
                },
                "charset_flag":"l",
                "check_positions":None
            }
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output_dict"], ScramblerValidators.valid_ring_settings_dict(test_dict["input_dict"], test_dict["charset_flag"], test_dict["machine"], test_dict["check_positions"]))

        for test_dict in failing:
            with self.assertRaises(RingSettingsError):
                ScramblerValidators.valid_ring_settings_dict(test_dict["input_dict"], test_dict["charset_flag"], test_dict["machine"], test_dict["check_positions"])
