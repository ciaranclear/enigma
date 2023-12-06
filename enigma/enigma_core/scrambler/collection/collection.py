from enigma_tools.formatter.formatter import EnigmaFormatter as ef
from enigma_core.settings.settings import EQUIPMENT_DICT, NUMBERS, LETTERS
from enigma_core.scrambler.devices.reflector.reflector import Reflector
from enigma_core.scrambler.devices.rotor.rotor import Rotor
from enigma_core.scrambler.exceptions.exceptions import (DeviceIDError,
                                                         MachineIDError,
                                                         CompatibilityError,
                                                         CellPositionError,
                                                         CellFlagError,
                                                         DeviceBorrowedError,
                                                         RingCharacterError,
                                                         CharacterSetFlagError)


class Collection:
        
    @classmethod
    def compatible_device_type(cls, machine, device, flags):
        """
        Takes a machine, device id and flags list. Returns the device if 
        """
        cls.valid_machine(machine)

        if not isinstance(flags, list):
            msg = f"flags argument must be list of flags not {type(flags)}."
            raise TypeError(msg)

        flags = [cls.valid_cell_flag(flag) for flag in flags]

        machine_dict = EQUIPMENT_DICT[machine]
        reflectors = machine_dict["REFLECTORS"]
        rotors = machine_dict["ROTORS"]

        if device in reflectors.keys() and "REF" in flags:
            return device, "REF"
        
        for rotor, rotor_dict in rotors.items():
            turn_chars = rotor_dict["turnover_chars"]

            if rotor == device and len(turn_chars) != 0 and "R_ROT" in flags:
                return device, "R_ROT"
            
            if rotor == device and len(turn_chars) == 0 and "F_ROT" in flags:
                return device, "F_ROT"
            
        msg = f"{device} is not a valid device for a {machine} enigma machine."
        raise DeviceIDError(msg)

    @classmethod
    def device_list(cls, machine, flags):
        """
        
        """
        cls.valid_machine(machine)

        if not isinstance(flags, list):
            msg = f"flags argument must be list of flags not {type(flags)}."
            raise TypeError(msg)

        flags = [cls.valid_cell_flag(flag) for flag in flags]

        machine_dict = EQUIPMENT_DICT[machine]

        device_list = []

        if "REF" in flags:
            reflectors = machine_dict["REFLECTORS"]
            for reflector in reflectors.keys():
                device_list.append(reflector)

        if "F_ROT" in flags or "R_ROT" in flags:
            rotors = machine_dict["ROTORS"]
            for rotor, rotor_dict in rotors.items():
                turn_chars = rotor_dict["turnover_chars"]
                if len(turn_chars) == 0 and "F_ROT" in flags:
                    device_list.append(rotor)
                if len(turn_chars) > 0 and "R_ROT" in flags:
                    device_list.append(rotor)

        return device_list
    
    @classmethod
    def valid_machine(cls, machine):
        """
        Takes a machine. Returns the machine if it is valid. If not valid 
        raises a MachineIDError.
        """
        if machine not in EQUIPMENT_DICT.keys():
            msg = f"{machine} is not a valid enigma machine."
            raise MachineIDError(msg)
        
        return machine
    
    @classmethod
    def machine_list(cls):
        """
        Returns a list of enigma machines.
        """
        return list(EQUIPMENT_DICT.keys())

    @classmethod
    def compatible_device_position(cls, machine, device, position):
        """
        Takes a machine, device and position. If device is compatible with the
        position returns the position. If not compatible raises a
        CompatibilityError. 
        """
        cls.valid_machine(machine)

        cls.valid_position(machine, position)
        
        cells_map = EQUIPMENT_DICT[machine]["CELLS_MAP"]

        flags = list(set(cells_map.values()))

        try:
            cls.compatible_device_type(machine, device, flags)
        except DeviceIDError as e:
            raise e

        machine_dict = EQUIPMENT_DICT[machine]

        reflectors = machine_dict["REFLECTORS"]

        rotors = machine_dict["ROTORS"]

        cells_map = EQUIPMENT_DICT[machine]["CELLS_MAP"]

        if device in reflectors.keys() and position == "REF":
            return position
        
        for rotor, rotor_dict in rotors.items():
            turn_chars = rotor_dict["turnover_chars"]
            if rotor == device:
                if len(turn_chars) == 0 and cells_map[position] == "F_ROT":
                    return position
                if len(turn_chars) > 0 and cells_map[position] == "R_ROT":
                    return position
                
        msg = (f"{machine} enigma machine {device} device is not "
               f"compatible with scrambler position {position}")
        raise CompatibilityError(msg)
    
    @classmethod
    def valid_position(cls, machine, position):
        """
        
        """
        cls.valid_machine(machine)

        positions = EQUIPMENT_DICT[machine]["CELLS_MAP"].keys()

        if position not in positions:
            msg = f"{position} is not a valid position for {machine} enigma machine."
            raise CellPositionError(msg)
        
        return position
    
    @classmethod
    def device_signature(cls, machine, flags):
        """
        
        """
        cls.valid_machine(machine)

        flags = [cls.valid_cell_flag(flag) for flag in flags]

        cells_map = EQUIPMENT_DICT[machine]["CELLS_MAP"]

        signature = {}

        for position, flag in cells_map.items():
            if flag in flags:
                signature[position] = flag

        return signature
    
    @classmethod
    def device_positions(cls, machine, device):
        """
        Takes a machine and a device type. Returns a list of positions that are
        compatible for that machine and device type.
        """
        cls.valid_machine(machine)

        cls.compatible_device_type(machine, device, ["REF","F_ROT","R_ROT"])

        reflectors = cls.device_list(machine, ["REF"])

        if device in reflectors:
            return ["REF"]

        static_rotors = cls.device_list(machine, ["F_ROT"])

        if device in static_rotors:
            return ["R4"]

        dynamic_rotors = cls.device_list(machine, ["R_ROT"])

        if device in dynamic_rotors:
            return ["RS","RM","RF"]

    @classmethod
    def valid_cell_flag(cls, flag):
        """
        Takes a cell flag. Returns the cell flag if valid. Raises a
        CellFlagError if flag is not valid.
        """
        if flag not in ["REF","F_ROT","R_ROT"]:
            msg = (f"{flag} is not a valid cell flag. "
                   f"Must be 'REF','F_ROT' or 'R_ROT'")
            raise CellFlagError(msg)
        
        return flag
    
    def __init__(self, machine, char_set_flag='L'):
        """
        Takes a machine type to initialize a Collection object for that machine
        type.
        """
        self.machine = self.valid_machine(machine)
        self._collection = []
        self._make_collection_dict()
        self.character_set_flag = char_set_flag

    def __repr__(self):
        """
        Returns the string repressentation of the collection object.
        """
        pass

    def __str__(self):
        """
        
        """
        _str = ef.line("COLLECTION")
        for obj in self._collection:
            _str += '\n'
            status = "TRUE" if obj["BORROWED"] else "FALSE"
            _str += f"DEIVICE ID ---------: {obj['DEVICE_OBJ'].device_id}\n"
            _str += f"BORROWED -----------: {status}\n"
            _str += obj["DEVICE_OBJ"].__str__()
            _str += f"{ef.line()}"
        return _str

    def borrowed_status(self, device_id):
        """
        Takes a device id. Returns the borrowed status of the device obj.
        """
        for device_dict in self._collection:
            if device_dict["DEVICE_OBJ"].device_id == device_id:
                return device_dict["BORROWED"]
            
        msg = f"{device_id} is not a valid device for a {self.machine} enigma machine."
        raise DeviceIDError(msg)

    def borrow_device(self, device_id):
        """
        Takes a device id. Returns the device obj if it is not currently
        borrowed. If device obj is currently borrowed raises a
        DeviceBorrowedError.
        """
        for device_dict in self._collection:
            if device_dict["DEVICE_OBJ"].device_id == device_id:
                if device_dict["BORROWED"]:
                    msg = f"Device {device_id} is currently borrowed."
                    raise DeviceBorrowedError(msg)
                else:
                    device_dict["BORROWED"] = True
                    return device_dict["DEVICE_OBJ"]
                
        msg = f"{device_id} is not a valid device for a {self.machine} enigma machine."
        raise DeviceIDError(msg)

    def return_device(self, device_obj):
        """
        Takes a device obj. Returns the device obj to the collection.
        """
        for device_dict in self._collection:
            if device_dict["DEVICE_OBJ"] is device_obj:
                device_dict["BORROWED"] = False
                return
            
        raise Exception(f"{type(device_obj)} is not a valid device object. "
                        f"Must be of type Reflector or type Rotor")

    def valid_ring_character(self, ring_char):
        """
        Takes a ring character. Returns the ring character if it is valid. If
        not valid raises a RingCharacterError.
        """
        if ring_char not in self._char_set:
            msg = f"{ring_char} is not a valid ring character."
            raise RingCharacterError(msg)
        else:
            return ring_char

    @property
    def character_set(self):
        """
        Returns the character current set.
        """
        return LETTERS if self._char_flag == 'L' else NUMBERS

    @property
    def character_set_flag(self):
        """
        Returns the current character set flag 'L' or 'N'.
        """
        return self._char_flag

    @character_set_flag.setter
    def character_set_flag(self, flag):
        """
        Takes a character set flag to set the character set that all devices in
        the collection will use.
        """
        if flag not in ['L','N']:
            msg = f"{flag} is not a valid character set flag. Must be 'L' or 'N'"
            raise CharacterSetFlagError(msg)
        else:
            self._char_flag = flag

            if flag == 'L':
                self._char_set = LETTERS
            elif flag == 'N':
                self._char_set = NUMBERS

            for device_dict in self._collection:
                device_dict["DEVICE_OBJ"].character_set_flag = flag

    def collection_dict(self):
        """
        Returns a dictionary object with keys of 'reflectors', 'rotors_static'
        and 'rotors_dynamic' to values of list of compatible device types for
        each key.
        """
        collection = {
            "REFLECTORS":self.device_list(self.machine, ["REF"]),
            "ROTORS_STATIC":self.device_list(self.machine, ["F_ROT"]),
            "ROTORS_DYNAMIC":self.device_list(self.machine, ["R_ROT"])
        }

        return collection

    def _make_collection_dict(self):
        """
        Initializes the rotors and reflector objects.
        """
        self._init_reflectors()
        self._init_rotors()

    def _init_reflectors(self):
        """
        Initializes the reflector objects and adds them to the collection.
        """
        reflectors = EQUIPMENT_DICT[self.machine]["REFLECTORS"]

        for reflector_id in reflectors:
            wire_list = reflectors[reflector_id]
            reflector_obj = Reflector(reflector_id, wire_list, 'L')
            reflector_dict = {
                "DEVICE_OBJ":reflector_obj,
                "BORROWED":False
            }
            self._collection.append(reflector_dict)

    def _init_rotors(self):
        """
        Initializes the rotor objects and adds them to the collection.
        """
        rotors = EQUIPMENT_DICT[self.machine]["ROTORS"]

        for rotor_id in rotors:
            wire_list = rotors[rotor_id]["wiring_chars"]
            turn_list = rotors[rotor_id]["turnover_chars"]
            rotor_obj = Rotor(rotor_id, wire_list, turn_list, 'L')
            rotor_dict = {
                "DEVICE_OBJ":rotor_obj,
                "BORROWED":False
            }
            self._collection.append(rotor_dict)