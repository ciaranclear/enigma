import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.machine_validators import *


class TestMachineValidators(unittest.TestCase):

    machines_list = EQUIPMENT_DICT.keys()

    def test_valid_enigma_machine(self):
        """
        
        """

        for machine in self.machines_list:
            self.assertEqual(machine, MachineValidators.valid_enigma_machine(machine))

        for machine in self.machines_list:
            self.assertEqual(machine, MachineValidators.valid_enigma_machine(machine.lower()))

        self.assertRaises(EnigmaMachineError, MachineValidators.valid_enigma_machine, "invalid_machine")

    def test_valid_permutation(self):
        """
        
        """
        passing = [
            {"input":"A_UKW-B_III_II_I_G3","output":"A_UKW-B_III_II_I_G3"}
        ]

        failing = [
            "A_UKW-Z_III_II_I_G3",
            "A_UKW-B_III_II_I_G4",
            "A_UKW-B_III_III_I_G3"
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output"], MachineValidators.valid_permutation(test_dict["input"]))

        for test_str in failing:
            with self.assertRaises(PermutationError):
                MachineValidators.valid_permutation(test_str)
