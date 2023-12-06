from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
import re


class EnigmaMachineError(Exception):
    """
    
    """
    def __init__(self, machine):
        """
        
        """
        machines_list = EQUIPMENT_DICT.keys()

        machines_str = ",".join(machines_list)

        err_msg = f"{machine} is not a valid enigma machine. Must be in {machines_str}."
        super().__init__(err_msg)


class MachineValidators:
    """
    
    """

    def valid_enigma_machine(machine):
        """"
        Check if case insensitive machine type is in machine list.
        Return uppercase machine type if valid or raise exception.    
        """
        machines_list = EQUIPMENT_DICT.keys()

        machine = machine.upper()

        for machine_original in machines_list:
            _machine = machine_original.upper()
            if machine == _machine:
                return machine_original
        
        raise EnigmaMachineError(machine)
