from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.machine_validators import MachineValidators, EnigmaMachineError
import re


class ReflectorTypeError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RotorTypesError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RotorSettingsError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RingSettingsError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RingCharacterError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class ScramblerTypesDictError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class PermutationError(Exception):
    """
    
    """
    def __init__(self, err_msg):
        """
        
        """
        super().__init__(err_msg)


class ScramblerValidators:
    """
    
    """

    def valid_reflector_type(machine, reflector):
        """
        Check if case insensitive reflector type is in reflectors
        list for given machine type. return uppercase reflector type
        if valid or raise exception. 
        """
        try:
            machine = MachineValidators.valid_enigma_machine(machine)
        except EnigmaMachineError as e:
            raise e
        else:
            reflectors_list = EQUIPMENT_DICT[machine]["REFLECTORS"].keys()

            reflector = reflector.upper()
        
            for reflector_original in reflectors_list:
                _reflector = reflector_original.upper()
                if reflector == _reflector:
                    return reflector_original
            err_msg = (f"Reflector type {reflector} is not a valid "
                       f"reflector type for {machine} enigma machine.")
            raise ReflectorTypeError(err_msg)
        
    def valid_rotor_types(machine, rotors_str):
        """
        Valid format 'III II I'.
        Parse rotor types for all positions and check that rotor types
        are valid. Return rotor type dict if valid or raise exception.
        """
        position_ids = ["RF","RM","RS","R4"]

        try:
            machine = MachineValidators.valid_enigma_machine(machine)
        except EnigmaMachineError as e:
            raise e
        else:
            rotors_str = rotors_str.upper()
            regex = re.compile('[A-Z]+')
            rotors = re.findall(regex, rotors_str)

            valid_rotors = EQUIPMENT_DICT[machine]["ROTORS"]
            cells_map = EQUIPMENT_DICT[machine]["CELLS_MAP"]

            positions = len(cells_map.keys()) -1

            # check for correct number of rotors
            if len(rotors) != positions:
                err_msg = (f"Incorrect number of rotors. "
                           f"{len(rotors)} rotors provided. "
                           f"{positions} rotors required.")
                raise RotorTypesError(err_msg)

            # check for valid rotor types
            valid_rotors_dict = {rot.upper() : rot for rot in valid_rotors.keys()}

            for rotor in rotors:
                if rotor not in valid_rotors_dict.keys():
                    valid_rotors_str = ",".join(valid_rotors_dict.keys())
                    err_msg = f"{rotor} not a valid rotor type. Must be in {valid_rotors_str}."
                    raise RotorTypesError(err_msg)

            # check for compatible rotor positions
            rotors.reverse()

            for index, rotor in enumerate(rotors):
                turnover_chars = valid_rotors[valid_rotors_dict[rotor]]["turnover_chars"]
                if index < 3 and len(turnover_chars) == 0:
                        err_msg = f"{rotor} incompatible rotor for position {position_ids[index]}."
                        raise RotorTypesError(err_msg)
                if index == 3 and len(turnover_chars) != 0:
                        err_msg = f"{rotor} incompatible rotor for position {position_ids[index]}."
                        raise RotorTypesError(err_msg)

            # check for unique rotor types
            unique = set(rotors)
            rotors_str = ",".join(rotors)
            if len(unique) != len(rotors):
                err_msg = f"repeated rotor type in {rotors_str}"
                raise RotorTypesError(err_msg)

            valid_dict = {}

            for index, rotor in enumerate(rotors, start=0):
                valid_dict[position_ids[index]] = valid_rotors_dict[rotor]

            return valid_dict
        
    def valid_rotor_settings(rot_settings_str, charset_flag, positions):
        """
        Valid format 'A A A' or '01 01 01' in order 'RS RM RF'.
        Parse rotor settings for all positions and check that rotor settings
        are valid. Return rotor settings dict if valid or raise exception.
        """

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()
    
        if positions not in [3,4]:
            err_msg = (f"{positions} is not a valid value for positions. "
                       f"Must be integer with value of 3 or 4.")
            raise Exception(err_msg)

        # parse settings
        rot_settings_str = rot_settings_str.upper()
        pattern = "[A-Z]+" if charset_flag == "L" else "[0-9]+"
        regex = re.compile(pattern)
        rotor_settings = re.findall(regex, rot_settings_str)
        # check for correct number of settings
        num_settings = len(rotor_settings)
        if num_settings != positions:
            err_msg = f"{num_settings} provided. {positions} rotor settings required."
            raise RotorSettingsError(err_msg)

        # check each setting is member correct charset
        charset = LETTERS if charset_flag == "L" else NUMBERS

        err_str = "letter A-Z" if charset_flag == "L" else "number 01-26"

        for rotor_setting in rotor_settings:
            if rotor_setting not in charset:
                err_msg = f"{rotor_setting} is an invalid rotor setting. Must be a {err_str}."
                raise RotorSettingsError(err_msg)
        
        # return rotor settings dictionary
        position_ids = ["RF","RM","RS","R4"]

        rotor_settings.reverse()

        settings_dict = {}

        for index, rotor_setting in enumerate(rotor_settings):
            settings_dict[position_ids[index]] = rotor_settings[index]

        return settings_dict
    
    def valid_ring_settings(rng_settings_str, charset_flag, positions):
        """
        Valid format 'A A A' or '01 01 01' in order 'RS RM RF'.
        Parse ring settings for all positions and check that ring settings
        are valid. Return ring settings dict if valid or raise exception.
        """

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()
    
        if positions not in [3,4]:
            err_msg = (f"{positions} is not a valid value for positions. "
                       f"Must be integer with value of 3 or 4.")
            raise Exception(err_msg)

        # parse settings
        rng_settings_str = rng_settings_str.upper()
        pattern = "[A-Z]+" if charset_flag == "L" else "[0-9]+"
        regex = re.compile(pattern)
        ring_settings = re.findall(regex, rng_settings_str)
        # check for correct number of settings
        num_settings = len(ring_settings)
        if num_settings != positions:
            err_msg = f"{num_settings} provided. {positions} ring settings required."
            raise RotorSettingsError(err_msg)

        # check each setting is member correct charset
        charset = LETTERS if charset_flag == "L" else NUMBERS

        err_str = "letter A-Z" if charset_flag == "L" else "number 01-26"

        for ring_setting in ring_settings:
            if ring_setting not in charset:
                err_msg = f"{ring_setting} is an invalid ring setting. Must be a {err_str}"
                raise RotorSettingsError(err_msg)
        
        # return rotor settings dictionary
        position_ids = ["RF","RM","RS","R4"]

        ring_settings.reverse()

        settings_dict = {}

        for index, ring_setting in enumerate(ring_settings):
            settings_dict[position_ids[index]] = ring_settings[index]

        return settings_dict
    
    def valid_scrambler_types_dict(machine, rotor_types_dict, check_positions):
        """
        Valid format {RS:'III', RM:'II', RF:'I'}.
        Check the rotor types at the required positions are valid and are
        compatible for that position. return valid return rotor types dictionary
        if valid or raise exception.
        """
        valid_position_ids = ["R4","RS","RM","RF"]

        try:
            machine = MachineValidators.valid_enigma_machine(machine)
        except EnigmaMachineError as e:
            raise e
        else:
            machine_positions = [p for p in EQUIPMENT_DICT[machine]["CELLS_MAP"].keys()]

        if check_positions:
            check_positions = [pos.upper() for pos in check_positions]
            for position in check_positions:
                if position not in machine_positions:
                    machine_positions_str = ",".join(machine_positions)
                    err_msg = (f"Invalid scrambler position {position}!. "
                               f"Scrambler position must be in {machine_positions_str}.")
                    raise Exception(err_msg)
        else:
            check_positions = machine_positions
        
        check_positions = [p for p in valid_position_ids if p in check_positions]

        formatted_settings = {k.upper() : v.upper() for k,v in rotor_types_dict.items()}

        # check for valid positions in 
        for position in formatted_settings.keys():
            if position not in machine_positions:
                machine_positions_str = ",".join(machine_positions)
                err_msg = (f"Invalid scrambler position {position}!."
                           f"Scrambler position must be in {machine_positions_str}.")
                raise ScramblerTypesDictError(err_msg)
    
        # check for valid reflector and rotor types at each check position
        valid_rotor_types_dict = {p : None for p in machine_positions}

        rotors_dict = EQUIPMENT_DICT[machine]["ROTORS"]

        reflectors_dict = EQUIPMENT_DICT[machine]["REFLECTORS"]

        for position in check_positions:
            if position in ["R4","RF","RM","RS"]:
                rotor_dict = None

                _rotor_type = formatted_settings[position]
                for rotor_type in rotors_dict.keys():
                    if _rotor_type and _rotor_type.upper() == rotor_type.upper():
                        rotor_dict = rotors_dict[rotor_type]
                        if position in ["RS","RM","RF"]:
                            if not rotor_dict["turnover_chars"]:
                                err_msg = (f"{rotor_type} is not compatible with positions RS,RM,RF. "
                                           f"Only compatible with position R4.")
                                raise ScramblerTypesDictError(err_msg)
                        elif position == "R4":
                            if rotor_dict["turnover_chars"]:
                                err_msg = (f"{rotor_type} is not compatible with position R4."
                                           f"Only compatible with positions RS,RM,RF.")
                                raise ScramblerTypesDictError(err_msg)
                        valid_rotor_types_dict[position] = rotor_type
                if not rotor_dict:
                    err_msg = f"{_rotor_type} is not a valid rotor type for {machine} machine."
                    raise ScramblerTypesDictError(err_msg)
            elif position == "REF":
                reflector_dict = None
                _reflector_type = formatted_settings[position]
                for reflector_type in reflectors_dict.keys():
                    if _reflector_type and _reflector_type.upper() == reflector_type.upper():
                        valid_rotor_types_dict[position] = reflector_type
                if not reflector_dict:
                    err_msg = f"{_reflector_type} is not a valid reflector type for {machine} machine."
                    raise ScramblerTypesDictError(err_msg)
            
        # check for duplicates
        device_types = [device for device in valid_rotor_types_dict.values() if device != None]

        if len(device_types) != len(set(device_types)):
            device_types_str = ",".join(device_types)
            err_msg = (f"Repeated scrambler device in {device_types_str}. "
                       f"All scrambler device types must be unique.")
            raise ScramblerTypesDictError(err_msg)

        return valid_rotor_types_dict
    
    def valid_rotor_settings_dict(settings_dict, charset_flag, machine=None, check_positions=None):
        """
        Valid format {RS:'A', RM:'A', RF:'A'}.
        Check the rotor settings at the required positions are valid rotor settings.
        Return rotor settings dict if valid or raise exception.
        """
        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        valid_position_ids = ["R4","RS","RM","RF"]

        if check_positions:
            check_positions = [pos.upper() for pos in check_positions]
            for position in check_positions:
                if position not in valid_position_ids:
                    err_msg = f"{position} is not a valid rotor position. Must e in R4,RS,RM,RF."
                    raise Exception(err_msg)
        
            check_positions = [p for p in valid_position_ids if p in check_positions]
            
        if machine:
            try:
                machine = MachineValidators.valid_enigma_machine(machine)
            except EnigmaMachineError as e:
                raise e
            else:
                machine_positions = [p for p in EQUIPMENT_DICT[machine]["CELLS_MAP"].keys() if p != "REF"]

        # if machine and check positions check for valid positions
        if check_positions:
            for position in check_positions:
                if position not in machine_positions:
                    machine_positions_str = ",".join(machine_positions)
                    err_msg = (f"{position} is not a valid rotor position. "
                               f"Must be in {machine_positions_str}.")
                    raise Exception(err_msg)
        
        # check for valid positions in settings dict
        formatted_settings = {k.upper() : v.upper() for k,v in settings_dict.items()}

        for position in formatted_settings.keys():
            if machine:
                if position not in machine_positions:
                    machine_positions_str = ",".join(machine_positions)
                    err_msg = (f"{position} is not a valid rotor position. "
                               f"Must be in {machine_positions_str}.")
                    raise RotorSettingsError(err_msg)
            else:
                if position not in valid_position_ids:
                    err_msg = (f"{position} is not a valid rotor position. "
                               f"Must be in R4,RS,RM,RF.")
                    raise RotorSettingsError(err_msg)

        # create valid check positions
        if machine and check_positions:
            check_positions = machine_positions
        elif machine and not check_positions:
            check_positions = machine_positions
        elif not check_positions:
            check_positions = formatted_settings.keys()

        # if machine create empty positions
        valid_settings_dict = {}

        if machine:
            for position in machine_positions:
                valid_settings_dict[position] = None

        # check each position in check positions is in formatted settings
        for position in check_positions:
            if position not in formatted_settings.keys():
                valid_positions_str = ",".join(formatted_settings.keys())
                err_msg = (f"{position} is not a valid position. "
                           f"Must be in {valid_positions_str}.")
                raise RotorSettingsError(err_msg)

        # check and format applicable settings in settings dict
        for position in check_positions:
            setting = formatted_settings[position]
            if setting not in charset:
                charset_range = "A-Z" if charset_flag == "L" else "01-26"
                err_msg = f"{setting} is not a valid rotor setting. Must be in {charset_range}."
                raise RotorSettingsError(err_msg)
            else:
                valid_settings_dict[position] = setting
        
        return valid_settings_dict
    
    def valid_ring_settings_dict(settings_dict, charset_flag, machine=None, check_positions=None):
        """
        Valid format {RS:'A', RM:'A', RF:'A'}.
        If machine type provided check that all positions are pressent.
        If check positions provided only check those positions.
        If no machine or check positions provided evaluate all positions.
        Return ring settings dict if valid or raise exception.
        """

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        valid_position_ids = ["R4","RS","RM","RF"]

        if check_positions:
            check_positions = [pos.upper() for pos in check_positions]
            for position in check_positions:
                if position not in valid_position_ids:
                    err_msg = f""
                    raise Exception(err_msg)
        
            check_positions = [p for p in valid_position_ids if p in check_positions]
            
        if machine:
            try:
                machine = MachineValidators.valid_enigma_machine(machine)
            except EnigmaMachineError as e:
                raise e
            else:
                machine_positions = [p for p in EQUIPMENT_DICT[machine]["CELLS_MAP"].keys() if p != "REF"]

        # if machine and check positions check for valid positions
        if check_positions:
            for position in check_positions:
                if position not in machine_positions:
                    machine_positions_str = ",".join(machine_positions)
                    err_msg = (f"{position} is not a valid rotor position. "
                               f"Must be in {machine_positions_str}.")
                    raise Exception(err_msg)
        
        # check for valid positions in settings dict
        formatted_settings = {k.upper() : v.upper() for k,v in settings_dict.items()}

        for position in formatted_settings.keys():
            if machine:
                if position not in machine_positions:
                    machine_positions_str = ",".join(machine_positions)
                    err_msg = (f"{position} is not a valid rotor position. "
                               f"Must be in {machine_positions_str}.")
                    raise RingSettingsError(err_msg)
            else:
                if position not in valid_position_ids:
                    err_msg = (f"{position} is not a valid rotor position. "
                               f"Must be in R4,RS,RM,RF.")
                    raise RingSettingsError(err_msg)

        # create valid check positions
        if machine and check_positions:
            check_positions = machine_positions
        elif machine and not check_positions:
            check_positions = machine_positions
        elif not check_positions:
            check_positions = formatted_settings.keys()

        # if machine create empty positions
        valid_settings_dict = {}

        if machine:
            for position in machine_positions:
                valid_settings_dict[position] = None

        # check each position in check positions is in formatted settings
        for position in check_positions:
            if position not in formatted_settings.keys():
                valid_positions_str = ",".join(formatted_settings.keys())
                err_msg = (f"{position} is not a valid position. "
                           f"Must be in {valid_positions_str}.")
                raise RingSettingsError(err_msg)

        # check and format applicable settings in settings dict
        for position in check_positions:
            setting = formatted_settings[position]
            if setting not in charset:
                charset_range = "A-Z" if charset_flag == "L" else "01-26"
                err_msg = (f"{setting} is not a valid ring setting. "
                           f"Must be in {charset_range}.")
                raise RingSettingsError(err_msg)
            else:
                valid_settings_dict[position] = setting
        
        return valid_settings_dict
    
    def valid_ring_character(character, charset_flag):
        """
    
        """
        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        charset_range = "A-Z" if charset_flag == "L" else "01-26"

        if charset_flag == "L":
            character = character.upper()
            if character not in charset:
                err_msg = (f"{character} is not a valid ring character. "
                           f"Ring character must be in {charset_range}.")
                raise RingCharacterError(err_msg)
        elif charset_flag == "N": 
            character = character.ljust(2, '0')
            if character not in charset:
                err_msg = (f"{character} is not a valid ring character. "
                           f"Ring character must be in {charset_range}.")
                raise RingCharacterError(err_msg)
        
        return character
    
    def valid_permutation(permutation_str, rs_flag=True, group_flag=True):
        """
        Valid input A_UKW-B_III_II_I_G3. 
        Parse permutation string to check for valid slow rotor, reflector,
        rotor types and group id. Return uppercase permutation if valid or
        raise exception.
        """
        permutation_str = permutation_str.upper()
        if rs_flag and not group_flag:
            pattern = "([A-Z]{1})_(UKW-[ABC])_([IV]+)_([IV]+)_([IV]+)"
        elif rs_flag and group_flag:
            pattern = "([A-Z]{1})_(UKW-[ABC])_([IV]+)_([IV]+)_([IV]+)_([G][123]{1})"
        elif not rs_flag and group_flag:
            pattern = "(UKW-[ABC])_([IV]+)_([IV]+)_([IV]+)_([G][123]{1})"
        elif not rs_flag and not group_flag:
            pattern = "(UKW-[ABC])_([IV]+)_([IV]+)_([IV]+)"
        parts = re.match(pattern, permutation_str)

        if not parts:
            err_msg = f"{permutation_str} is not a valid permutation string."
            raise PermutationError(err_msg)

        elif rs_flag and not group_flag and len(parts.groups()) != 5:
            err_msg = f""
            raise PermutationError(err_msg)
        
        elif rs_flag and group_flag and len(parts.groups()) != 6:
            err_msg = f""
            raise PermutationError(err_msg)
        
        elif not rs_flag and group_flag and len(parts.groups()) != 5:
            err_msg = f""
            raise PermutationError(err_msg)
        
        elif not rs_flag and not group_flag and len(parts.groups()) != 4:
            err_msg = f""
            raise PermutationError(err_msg)
    
        valid_rotors = EQUIPMENT_DICT["WEHRMACHT"]["ROTORS"].keys()

        perm_dict = {}
        
        if rs_flag and not group_flag:
            keys = ["RS","REF","ROT_RS","ROT_RM","ROT_RF"]
        elif rs_flag and group_flag:
            keys = ["RS","REF","ROT_RS","ROT_RM","ROT_RF","GROUP"]
        elif not rs_flag and group_flag:
            keys = ["REF","ROT_RS","ROT_RM","ROT_RF","GROUP"]
        elif not rs_flag and not group_flag:
            keys = ["REF","ROT_RS","ROT_RM","ROT_RF"]

        for index, key in enumerate(keys, start=1):
            perm_dict[key] = parts.group(index)

        if rs_flag and not group_flag:
            rs = parts.group(1)
            ref = parts.group(2)
            rot_rs = parts.group(3)
            rot_rm = parts.group(4)
            rot_rf = parts.group(5)
        elif rs_flag and group_flag:
            rs = parts.group(1)
            ref = parts.group(2)
            rot_rs = parts.group(3)
            rot_rm = parts.group(4)
            rot_rf = parts.group(5)
            group = parts.group(6)
        elif not rs_flag and group_flag:
            ref = parts.group(1)
            rot_rs = parts.group(2)
            rot_rm = parts.group(3)
            rot_rf = parts.group(4)
            group = parts.group(5)
        elif not rs_flag and not group_flag:
            ref = parts.group(1)
            rot_rs = parts.group(2)
            rot_rm = parts.group(3)
            rot_rf = parts.group(4)

        rotors = [rot_rs, rot_rm, rot_rf]

        unique = set(rotors)

        if len(unique) != len(rotors):
            err_msg = f""
            raise PermutationError(err_msg)
    
        for rotor in rotors:
            if rotor not in valid_rotors:
                err_msg = f""
                raise PermutationError(err_msg)

        if rs_flag and not group_flag:
            perm_str = f"{rs}_{ref}_{rot_rs}_{rot_rm}_{rot_rf}"
        elif rs_flag and group_flag:
            perm_str = f"{rs}_{ref}_{rot_rs}_{rot_rm}_{rot_rf}_{group}"
        elif not rs_flag and group_flag:
            perm_str = f"{ref}_{rot_rs}_{rot_rm}_{rot_rf}_{group}"
        elif not rs_flag and not group_flag:
            perm_str = f"{ref}_{rot_rs}_{rot_rm}_{rot_rf}"

        return perm_str, perm_dict
