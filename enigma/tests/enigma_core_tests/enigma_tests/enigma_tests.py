"""
settings = {
    scrambler_char_flag:
    scrambler_turnover_flag:
    plugboard_char_flag:
    plugboard_mode:
    "connections":{
        "01A":"A","02A":"B","03A":"C","04A":"D","05A":"E",
        "06A":"F","07A":"G","08A":"H","09A":"I","10A":"J",
        "01B":"K","02B":"L","03B":"M","04B":"N","05B":"O",
        "06B":"P","07B":"Q","08B":"R","09B":"S","10B":"T"
    },
    connections:[
        ["A","B"],["C","D"],["E","F"],["G","H"],["I","J"],
        ["K","L"],["M","N"],["O","P"],["Q","R"],["S","T"]
    ]
    reflector:
    rotor_types:
    rotor_settings:
    ring_settings:
}
"""

import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.factory import machine_list, make_machine


class TestEnigmaCore(unittest.TestCase):

    def make_enigma_machine(self, machine, plugboard_mode='S', char_set='L'):
        """
        
        """
        return make_machine(machine, )

    def test_stecker_machine(self):
        """
        
        """
        # WEHRMACHT
        settings = {
            "scrambler_char_flag":'L',
            "scrambler_turnover_flag":True,
            "plugboard_char_flag":'L',
            "plugboard_mode":'S',
            "plugboard_connections":[
                ["A","B"],["C","D"],["E","F"],["G","H"],["I","J"],
                ["K","L"],["M","N"],["O","P"],["Q","R"],["S","T"]
            ],
            "reflector":"UKW-B",
            "rotor_types":{"RS":"III","RM":"II","RF":"I"},
            "rotor_settings":{"RS":"X","RM":"Y","RF":"Z"},
            "ring_settings":{"RS":"X","RM":"Y","RF":"Z"}
        }

        machine = make_machine("WEHRMACHT", settings)

        input = "mynameisciaranclear"

        output = ""

        for c in input:
            output += machine.character_input(c)

        self.assertEqual(output, "LDHHAUKORQRKSVXGZUI")

        # LUFTWAFFE
        settings = {
            "scrambler_char_flag":'L',
            "scrambler_turnover_flag":True,
            "plugboard_char_flag":'L',
            "plugboard_mode":'S',
            "reflector":"UKW-B",
            "rotor_types":{"RS":"III","RM":"II","RF":"I"},
            "rotor_settins":{"RS":"A","RM":"A","RF":"A"},
            "ring_settings":{"RS":"A","RM":"A","RF":"A"}
        }

        machine = make_machine("LUFTWAFFE", settings)

        input = "mynameisciaranclear"

        output = ""

        for c in input:
            output += machine.character_input(c)

        self.assertEqual(output, "HCLMFDVUKZJZGEEOOCY")

        # ENIGMA M3 Kriegsmarine
        settings = {
            "scrambler_char_flag":'L',
            "scrambler_turnover_flag":True,
            "plugboard_char_flag":'L',
            "plugboard_mode":'S',
            "reflector":"UKW-B",
            "rotor_types":{"RS":"III","RM":"II","RF":"I"},
            "rotor_settins":{"RS":"X","RM":"A","RF":"A"},
            "ring_settings":{"RS":"A","RM":"A","RF":"A"}
        }

        machine = make_machine("ENIGMA M3 Kriegsmarine", settings)

        input = "mynameisciaranclear"

        output = ""

        for c in input:
            output += machine.character_input(c)

        self.assertEqual(output, "HCLMFDVUKZJZGEEOOCY")

        # ENIGMA M4 u-boat
        settings = {
            "scrambler_char_flag":'L',
            "scrambler_turnover_flag":True,
            "plugboard_char_flag":'L',
            "plugboard_mode":'S',
            "reflector":"UKW-B",
            "rotor_types":{"R4":"Beta","RS":"III","RM":"II","RF":"I"},
            "rotor_settins":{"R4":"A","RS":"A","RM":"A","RF":"A"},
            "ring_settings":{"R4":"A","RS":"A","RM":"A","RF":"A"}
        }

        machine = make_machine("ENIGMA M4 u-boat", settings)

        input = "mynameisciaranclear"

        output = ""

        for c in input:
            output += machine.character_input(c)

        self.assertEqual(output, "HCLMFDVUKZJZGEEOOCY")

    def test_uhr_box_machine(self):
        """
        
        """
        # WEHRMACHT
        settings = {
            "scrambler_char_flag":'L',
            "scrambler_turnover_flag":True,
            "plugboard_char_flag":'L',
            "plugboard_mode":'U',
            "uhr_box_setting":2,
            "plugboard_connections":{
                "01A":"A","02A":"B","03A":"C","04A":"D","05A":"E",
                "06A":"F","07A":"G","08A":"H","09A":"I","10A":"J",
                "01B":"K","02B":"L","03B":"M","04B":"N","05B":"O",
                "06B":"P","07B":"Q","08B":"R","09B":"S","10B":"T"
            },
            "reflector":"UKW-B",
            "rotor_types":{"RS":"III","RM":"II","RF":"I"},
            "rotor_settings":{"RS":"A","RM":"A","RF":"A"},
            "ring_settings":{"RS":"A","RM":"A","RF":"A"}
        }

        machine = make_machine("WEHRMACHT", settings)

        input = "mynameisciaranclear"

        output = ""

        for c in input:
            output += machine.character_input(c)

        self.assertEqual(output, "FMIPNGKZJLVICKACOJZ")

        # LUFTWAFFE
        settings = {
            "scrambler_char_flag":'L',
            "scrambler_turnover_flag":True,
            "plugboard_char_flag":'N',
            "plugboard_mode":'U',
            "uhr_box_setting":2,
            "plugboard_connections":{
                "01A":"01","02A":"02","03A":"03","04A":"04","05A":"05",
                "06A":"06","07A":"07","08A":"08","09A":"09","10A":"10",
                "01B":"11","02B":"12","03B":"13","04B":"14","05B":"15",
                "06B":"16","07B":"17","08B":"18","09B":"19","10B":"20"
            },
            "reflector":"UKW-B",
            "rotor_types":{"RS":"III","RM":"II","RF":"I"},
            "rotor_settings":{"RS":"A","RM":"A","RF":"A"},
            "ring_settings":{"RS":"A","RM":"A","RF":"A"}
        }

        machine = make_machine("WEHRMACHT", settings)

        input = "mynameisciaranclear"

        output = ""

        for c in input:
            output += machine.character_input(c)

        self.assertEqual(output, "FMIPNGKZJLVICKACOJZ")

        # ENIGMA M3 Kriegsmarine

        # ENIGMA M4 u-boat