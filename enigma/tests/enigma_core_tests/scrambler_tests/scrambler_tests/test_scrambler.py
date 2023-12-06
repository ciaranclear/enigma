import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.scrambler.scrambler.scrambler import Scrambler


class TestScrambler(unittest.TestCase):
    """

    """
    def make_default_scrambler(self, machine, char_flag='L'):
        return Scrambler(machine, char_flag)

    def setting_machine_list(self):
        """
        
        """
        return list(EQUIPMENT_DICT.keys())
    
    def settings_reflectors_list(self, machine):
        """
        
        """
        return list(EQUIPMENT_DICT[machine]["REFLECTORS"].keys())
    
    def settings_rotor_list(self, machine, flag=None):
        """
        Returns a list of rotors for the provided machine type. if an optional
        F_ROT or R_ROT rotor flag is provided then a list of only rotors that
        match the provided flag will be returned.
        """
        rotors_list = []

        rotors = EQUIPMENT_DICT[machine]["ROTORS"]

        for rotor_id, rotor_data in rotors.items():
            turn_chars = rotor_data["turnover_chars"]
            if (flag == None or flag == "R_ROT") and len(turn_chars) != 0:
                rotors_list.append(rotor_id)
            elif (flag == None or flag == "F_ROT") and len(turn_chars) == 0:
                rotors_list.append(rotor_id)

        return rotors_list

    def test_set_get_remove_device(self):
        """
        
        """
        machines = self.setting_machine_list()

        for machine in machines:
            reflectors = self.settings_reflectors_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            s = self.make_default_scrambler(machine)

            for reflector in reflectors:
                s.set_device("REF", reflector)
                device_obj = s.get_device("REF")
                s.remove_device("REF")

            for rotor in static_rotors:
                s.set_device("R4", rotor)
                device_obj = s.get_device("R4")
                s.remove_device("R4")

            for rotor in dynamic_rotors:
                s.set_device("RF", rotor)
                device_obj = s.get_device("RF")
                s.remove_device("RF")

    def test_get_device_id(self):
        """
        
        """
        machines = self.setting_machine_list()

        for machine in machines:
            reflectors = self.settings_reflectors_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            s = self.make_default_scrambler(machine)

            for reflector in reflectors:
                self.assertEqual(s.get_device_id("REF"), None)
                s.set_device("REF", reflector)
                device_obj = s.get_device("REF")
                self.assertEqual(s.get_device_id("REF"), reflector)
                s.remove_device("REF")

            for rotor in static_rotors:
                self.assertEqual(s.get_device_id("R4"), None)
                s.set_device("R4", rotor)
                device_obj = s.get_device("R4")
                self.assertEqual(s.get_device_id("R4"), rotor)
                s.remove_device("R4")

            for rotor in dynamic_rotors:
                self.assertEqual(s.get_device_id("RF"), None)
                s.set_device("RF", rotor)
                device_obj = s.get_device("RF")
                self.assertEqual(s.get_device_id("RF"), rotor)
                s.remove_device("RF")

    def test_clear_scrambler(self):
        """
        
        """
        machines = self.setting_machine_list()

        for machine in machines:
            reflectors = self.settings_reflectors_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            s = self.make_default_scrambler(machine)

            s.set_device("REF", reflectors[0])

            if static_rotors: s.set_device("R4", static_rotors[0])

            s.set_device("RF", dynamic_rotors[0])
            s.set_device("RM", dynamic_rotors[1])
            s.set_device("RS", dynamic_rotors[2])

            self.assertEqual(s.valid_scrambler(), True)

            s.clear_scrambler()

            self.assertEqual(s.valid_scrambler(), False)

    def test_default_settings(self):
        """
        
        """
        machines = self.setting_machine_list()

        for machine in machines:
            reflectors = self.settings_reflectors_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            s = self.make_default_scrambler(machine)

            s.set_device("REF", reflectors[0])

            if static_rotors: s.set_device("R4", static_rotors[0])

            s.set_device("RF", dynamic_rotors[0])
            s.set_device("RM", dynamic_rotors[1])
            s.set_device("RS", dynamic_rotors[2])

            rot_settings = {
                "RS":"X",
                "RM":"Y",
                "RF":"Z"
            }

            rng_settings = {
                "RS":"B",
                "RM":"C",
                "RF":"D"
            }

            if static_rotors:
                rot_settings["R4"] = "Q"
                rng_settings["R4"] = "E"

            s.rotor_settings = rot_settings
            s.ring_settings = rng_settings

            s.default_settings()

            rot_settings = s.rotor_settings

            rng_settings = s.ring_settings

            for setting in rot_settings.values():
                self.assertEqual(setting, "A")

            for setting in rng_settings.values():
                self.assertEqual(setting, "A")

    def test_input_output(self):
        """
        
        """
        s = self.make_default_scrambler("WEHRMACHT")

        s.set_device("REF", "UKW-B")
        s.set_device("RS", "III")
        s.set_device("RM", "II")
        s.set_device("RF", "I")

        input = "MYNAMEISCIARANCLEAR"

        output = ""

        for c in input:
            i = LETTERS.index(c)
            i = s.keyed_input(i)
            output += LETTERS[i]

        #print(output)


        s = self.make_default_scrambler("WEHRMACHT")

        s.turnover_flag = False

        s.set_device("REF", "UKW-B")
        s.set_device("RS", "III")
        s.set_device("RM", "II")
        s.set_device("RF", "I")

        input = "MYNAMEISCIARANCLEAR"

        output = ""

        for c in input:
            i = LETTERS.index(c)
            i = s.keyed_input(i)
            output += LETTERS[i]

        #print(output)

    def test_character_set(self):
        """
        
        """
        s = self.make_default_scrambler("WEHRMACHT", 'L')

        self.assertEqual(s.character_set_flag, 'L')

        self.assertEqual(s.character_set, LETTERS)

        s.character_set_flag = 'N'

        self.assertEqual(s.character_set_flag, 'N')

        self.assertEqual(s.character_set, NUMBERS)

    def test_rotor_types(self):
        """
        
        """
        machines = self.setting_machine_list()

        for machine in machines:
            s = self.make_default_scrambler(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            rotors_dict = {
                "RF":dynamic_rotors[0],
                "RM":dynamic_rotors[1],
                "RS":dynamic_rotors[2]
            }

            if static_rotors: rotors_dict["R4"] = static_rotors[0]

            s.rotor_types = rotors_dict

            rotors_dict = s.rotor_types