import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.scrambler.collection.collection import Collection
from enigma_core.scrambler.exceptions.exceptions import (DeviceIDError, 
                                                         MachineIDError, 
                                                         CompatibilityError,
                                                         CellPositionError,
                                                         DeviceBorrowedError,
                                                         RingCharacterError,
                                                         CharacterSetFlagError)


class TestCollection(unittest.TestCase):
    
    def make_default_collection(self, machine=None, char_flag=None):
        """
        Returns a Collection object which defaults to WEHRMACHT and LETTERS
        character set or to the optional provided machine type and character 
        set flag parameters.        
        """
        machine = machine or "WEHRMACHT"
        char_flag = char_flag or 'L'

        return Collection(machine, char_flag)
    
    def settings_machine_list(self):
        """
        Returns a machine type list.
        """
        return list(EQUIPMENT_DICT.keys())
    
    def settings_reflector_list(self, machine):
        """
        Returns a list of reflectors for the provided machine type.
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

    def test_compatible_device_type(self):
        """
        
        """
        # for each machine
        # check compatibility for each device and device flag.
        # check for failing flag.
        # check for failing device type.

        machines = self.settings_machine_list()

        for machine in machines:
            reflectors = self.settings_reflector_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")
            
            for reflector in reflectors:
                args = [machine, reflector, ["REF"]]
                self.assertEqual(
                    Collection.compatible_device_type(*args),
                    (reflector, "REF")
                )

                self.assertRaises(
                    DeviceIDError, 
                    Collection.compatible_device_type, 
                    machine, "dud_reflector", ["REF"]
                )
                
            for rotor in static_rotors:
                args = [machine, rotor, ["F_ROT"]]
                self.assertEqual(
                    Collection.compatible_device_type(*args),
                    (rotor, "F_ROT")
                )

                self.assertRaises(
                    DeviceIDError, 
                    Collection.compatible_device_type, 
                    machine, "dud_rotor", ["F_ROT"]
                )

            for rotor in dynamic_rotors:
                args = [machine, rotor, ["R_ROT"]]
                self.assertEqual(
                    Collection.compatible_device_type(*args),
                    (rotor, "R_ROT")
                )

                self.assertRaises(
                    DeviceIDError, 
                    Collection.compatible_device_type, 
                    machine, "dud_rotor", ["R_ROT"]
                )

    def test_device_list(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            reflectors = self.settings_reflector_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            refs = Collection.device_list(machine, ["REF"])

            for reflector in reflectors:
                self.assertIn(reflector, refs)

            dynamic_rots = Collection.device_list(machine, ["R_ROT"])

            for rotor in dynamic_rotors:
                self.assertIn(rotor, dynamic_rots)

            if static_rotors:
                static_rots = Collection.device_list(machine, ["F_ROT"])

                for rotor in static_rotors:
                    self.assertIn(rotor, static_rots)

    def test_valid_machine(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            self.assertEqual(Collection.valid_machine(machine), machine)
            
        self.assertRaises(
            MachineIDError, 
            Collection.valid_machine, 
            "dud_machine"
        )

    def test_machine_list(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            self.assertIn(machine, Collection.machine_list())

        self.assertNotIn("dud_machine", Collection.machine_list())

    def test_compatible_device_position(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            reflectors = self.settings_reflector_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            for reflector in reflectors:
                args = [machine, reflector, "REF"]
                self.assertEqual(
                    Collection.compatible_device_position(*args),
                    "REF"
                )

                args = [machine, reflector, "RF"]
                self.assertRaises(
                    CompatibilityError, 
                    Collection.compatible_device_position, 
                    *args
                )

            for rotor in static_rotors:
                args = [machine, rotor, "R4"]
                self.assertEqual(
                    Collection.compatible_device_position(*args),
                    "R4"
                )

                args = [machine, rotor, "REF"]
                self.assertRaises(
                    CompatibilityError, 
                    Collection.compatible_device_position, 
                    *args
                )

            for rotor in dynamic_rotors:
                positions = ["RS","RM","RF"]
                for position in positions:
                    args = [machine, rotor, position]
                    self.assertEqual(
                        Collection.compatible_device_position(*args),
                        position
                    )

                    args = [machine, rotor, "REF"]
                    self.assertRaises(
                        CompatibilityError, 
                        Collection.compatible_device_position, 
                        *args
                    )

    def test_valid_position(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            positions = EQUIPMENT_DICT[machine]["CELLS_MAP"].keys()

            for position in positions:
                self.assertEqual(
                    Collection.valid_position(machine, position),
                    position
                )

            self.assertRaises(
                CellPositionError,
                Collection.valid_position,
                machine, "dud"
            )


    def test_device_signature(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            cells_map = EQUIPMENT_DICT[machine]["CELLS_MAP"]
            flags = list(set(cells_map.values()))

            signature = Collection.device_signature(machine, flags)

            for position in cells_map.keys():
                self.assertIn(position, signature.keys())

            if "R4" not in cells_map.keys():
                self.assertNotIn("R4", signature.keys())

    def test_device_positions(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            reflectors = self.settings_reflector_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            for reflector in reflectors:
                self.assertEqual(
                    Collection.device_positions(machine, reflector),
                    ["REF"]
                )

            for rotor in static_rotors:
                self.assertEqual(
                    Collection.device_positions(machine, rotor),
                    ["R4"]
                )

            for rotor in dynamic_rotors:
                self.assertEqual(
                    Collection.device_positions(machine, rotor),
                    ["RS","RM","RF"]
                )

    def test_valid_cell_flag(self):
        """
        
        """
        for flag in ["REF","F_ROT","R_ROT"]:
            self.assertEqual(
                Collection.valid_cell_flag(flag),
                flag
            )

    def test_borrowed_functionality(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            c = self.make_default_collection(machine)

            reflectors = self.settings_reflector_list(machine)

            static_rotors = self.settings_rotor_list(machine, "F_ROT")

            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            device_lists = [
                reflectors,
                static_rotors,
                dynamic_rotors
            ]

            for device_list in device_lists:
                for device_id in device_list:
                    # check borrow status
                    self.assertEqual(c.borrowed_status(device_id), False)

                    # borrow device
                    device_obj = c.borrow_device(device_id)

                    # raise borrowed error
                    self.assertRaises(
                        DeviceBorrowedError,
                        c.borrow_device,
                        device_id
                    )

                    # check borrow status
                    self.assertEqual(c.borrowed_status(device_id), True)

                    # return device
                    c.return_device(device_obj)

                    # check borrow status
                    self.assertEqual(c.borrowed_status(device_id), False)

    def test_character_functionality(self):
        """
        
        """
        c = self.make_default_collection(char_flag='L')

        # get character set flag
        self.assertEqual(c.character_set_flag, 'L')

        # get character set
        self.assertEqual(c.character_set, LETTERS)

        # check valid ring character
        self.assertEqual(c.valid_ring_character('A'), 'A')

        # check invalid ring character
        self.assertRaises(
            RingCharacterError,
            c.valid_ring_character,
            '01'
        )

        # false character set flag

        try:
            c.character_set_flag = '#'
        except CharacterSetFlagError:
            pass
        else:
            raise Exception("Failed to raise expected exception CharacterSetFlagError")

        # change character set flag
        c.character_set_flag = 'N'

        # get character set flag
        self.assertEqual(c.character_set_flag, 'N')

        # get character set
        self.assertEqual(c.character_set, NUMBERS)

        # check valid ring character
        self.assertEqual(c.valid_ring_character('01'), '01')

        # check invalid ring character
        self.assertRaises(
            RingCharacterError,
            c.valid_ring_character,
            'A'
        )

    def test_collection_dict(self):
        """
        
        """
        machines = self.settings_machine_list()

        for machine in machines:
            reflectors = self.settings_reflector_list(machine)
            static_rotors = self.settings_rotor_list(machine, "F_ROT")
            dynamic_rotors = self.settings_rotor_list(machine, "R_ROT")

            c = self.make_default_collection(machine)

            collection_dict = c.collection_dict()

            self.assertEqual(
                collection_dict["REFLECTORS"],
                reflectors
            )

            self.assertEqual(
                collection_dict["ROTORS_DYNAMIC"],
                dynamic_rotors
            )

            if static_rotors:
                self.assertEqual(
                    collection_dict["ROTORS_STATIC"],
                    static_rotors
                )
