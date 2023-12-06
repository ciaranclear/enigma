from enigma_core.settings.settings import LETTERS, NUMBERS
import re


class SteckerPlugboardSettingsError(Exception):
    """
    Raised when there is an error with stecker plugboard settings.
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class UhrBoxPlugboardSettingsError(Exception):
    """
    Raised when there is an error with uhr box plugboard settings.    
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class SocketIdError(Exception):
    """
    Raised when there is a plugboard socket id error.
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class UhrBoxPlugIdError(Exception):
    """
    Raised if there is a uhr box plug id error.
    """
    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class PlugboardValidators:

    def valid_stecker_pb_settings(pb_settings_str, charset_flag):
        """
        Valid format 'AB CD EF GH IJ KL MN OP QR ST' or
        '01,02 03,04 05,06 07,08 09,10 ......'.
        Parse pb settings for required positions and check that the pb settings
        are valid. Return a pb settings dict or raise an exception.    
        """

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        # parse pb settings string
        pb_settings_str = pb_settings_str.upper()
        pattern = "[A-Z]+" if charset_flag == "L" else "[0-9]+"
        regex = re.compile(pattern)
        pb_settings = re.findall(regex, pb_settings_str)

        # check for correct number of settings
    
        if charset_flag == "L" and len(pb_settings) > 13:
            err_msg = (f"There are to many plugboard pairs provided. "
                       f"Max number of plugboard pairs is 13.")
            raise SteckerPlugboardSettingsError(err_msg)
        elif charset_flag == "N" and len(pb_settings) > 26:
            err_msg = (f"There are to many plugboard pairs provided. "
                       f"Max number of plugboard pairs is 13.")
            raise SteckerPlugboardSettingsError(err_msg)

        # check each pair in pb setting is member of charset
        if charset_flag == "L":
            for pair in pb_settings:
                if len(pair) != 2:
                    err_msg = (f"Invalid plugboard pair {pair}. "
                               f"Each plugboard pair must be two characters.")
                    raise SteckerPlugboardSettingsError(err_msg)
                if pair[0] not in charset or pair[1] not in charset:
                    err_msg = (f"Invalid plugboard pair {pair}. "
                               f"Contains invalid characters. "
                               f"Must contain characters A-Z.")
                    raise SteckerPlugboardSettingsError(err_msg)
        else:
            for socket_id in pb_settings:
                if socket_id not in charset:
                    err_msg = (f"Invalid socket id {socket_id}. "
                               f"Plugboard socket ids must be in range 01-26.")
                    raise SteckerPlugboardSettingsError(err_msg)
            
        # check for unique socket ids
        unique = set(pb_settings)

        if len(unique) != len(pb_settings):
            pb_settings_str = "".join(pb_settings)
            err_msg = (f"Invalid plugboard settings {pb_settings_str}. "
                       f"Contains repeated socket ids. "
                       f"All socket ids must be unique.")
            raise SteckerPlugboardSettingsError(err_msg)

        # return settings dictionary
        settings_dict = {c : c for c in charset}

        if charset_flag == "L":
            for pair in pb_settings:
                settings_dict[pair[0]] = pair[1]
                settings_dict[pair[1]] = pair[0]
        else:
            while True:
                if pb_settings:
                    s1 = pb_settings.pop()
                    s2 = pb_settings.pop()
                    settings_dict[s1] = s2
                    settings_dict[s2] = s1
                else:
                    break

        return settings_dict
    
    def valid_uhr_box_pb_settings(pb_settings_str, charset_flag, group, previous=None):
        """
        Valid format 'A B C D E F G H I J K' or '01 02 03 04 05 06 07 08 09 10'.
        Parse pb settings for all uhr plugs and check that the pb settings are
        valid. If previous groups settings are provided check that there is no
        overlap. return a pb settings dict or raise an exception.
        """

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        if group not in "AaBb":
            raise Exception(f"Invalid group id {group}. Must be in 'AaBb'.")
        else:
            group = group.upper()

        # parse pb settings string
        pb_settings_str = pb_settings_str.upper()
        pattern = "[A-Z]+" if charset_flag == "L" else "[0-9]+"
        regex = re.compile(pattern)
        pb_settings = re.findall(regex, pb_settings_str)

        # check for correct number of settings
        if len(pb_settings) != 10:
            pb_settings_str = ",".join(pb_settings)
            err_msg = (f"Invalid plugboard settings! {pb_settings_str}. "
                       f"10 connections required. "
                       f"Only {len(pb_settings)} connections provided.")
            raise UhrBoxPlugboardSettingsError(err_msg)

        # check for unique settings
        unique = set(pb_settings)
        if len(unique) != len(pb_settings):
            pb_settings_str = ",".join(pb_settings)
            err_msg = (f"Invalid plugboard settings! {pb_settings_str}. "
                       f"Repeated socket id(s) in plugboard settings. "
                       f"All socket ids must be unique.")
            raise UhrBoxPlugboardSettingsError(err_msg)

        # check each setting is member of charset
        for socket_id in pb_settings:
            if socket_id not in charset:
                charset_range = "A-Z" if charset_flag == "L" else "01-26"
                err_msg = (f"Invalid socket id {socket_id}. "
                           f"All socket ids should be in range {charset_range}.")
                raise UhrBoxPlugboardSettingsError(err_msg)

        # if previous group settings provided check there is no overlap
        if previous:
            for socket_id in previous.values():
                if socket_id in pb_settings:
                    err_msg = (f"Repeated socket id {socket_id} in both groups. "
                               f"All socket ids must be unique.")
                    raise UhrBoxPlugboardSettingsError(err_msg)

        # return settings dictionary
        settings = {}
    
        for index, socket_id in enumerate(pb_settings):
            settings[f"{str(index + 1).rjust(2, '0')}{group}"] = pb_settings[index]

        if previous:
            settings.update(previous)

        return settings
    
    def valid_uhr_box_plugboard_settings(plugboard_str, charset_flag):
        """
        Plugboard settings for uhr box mode in format 
        "A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]" 
        letter mode in format 
        "A=[1,2,3,4,5,6,7,8,9,10] B=[11,12,13,14,15,16,17,18,19,20]" 
        number mode
        """
        def parse_uhr_box_connections(connections):
            regex = re.compile(r'(?P<id>[abAB])=\[(?P<plugs>[a-zA-Z0-9,; ]+)\]')
            connections = re.findall(regex, connections)
            return connections

        def valid_uhr_box_groups(connections):
            for group in connections:
                if group[0] not in ('a','A','b','B'):
                    err_msg = f"Invalid uhr box group id {group[0]}. Must be 'A' or 'B'"
                    raise UhrBoxPlugboardSettingsError(err_msg)

            letter_range = 'A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]'
            number_range = 'A=[1,2,3,4,5,6,7,8,9,10] B=[11,12,13,14,15,16,17,18,19,20]'
            charset_range = letter_range if charset_flag == 'L' else number_range
            if len(connections) != 2:
                err_msg = (f"Incorrect uhr box plugboard connections.\n"
		                   f"Must be in the format {charset_range}")
                raise UhrBoxPlugboardSettingsError(err_msg)
            return connections

        def format_uhr_box_letter_connections(connections):
            #filter out non letter chars and convert to upper case
            formatted = []
            for group in connections:
                group_id = group[0].upper()
                conns = group[1]
                conn_str = ''
                for conn in conns:
                    if conn.upper() in LETTERS:
                        conn_str += conn.upper()
                formatted.append((group_id, conn_str))
            return formatted

        def format_uhr_box_number_connections(connections):
            #left pad each number with a 0 to be two digits long
            formatted = []
            for group in connections:
                group_id = group[0].upper()
                conns = group[1]
                fconns = []
                regex = re.compile(r'[0-9]+')
                conns = re.findall(regex, conns)
                for conn in conns:
                    fconns.append(conn.rjust(2, '0'))
                formatted.append((group_id, fconns))
            return formatted

        def validate_uhr_box_connections(connections, charset_flag):
            charset = LETTERS if charset_flag == "L" else NUMBERS
            all_conns = []
            ub_conns = {}
            for group in connections:
                group_id = group[0]
                conns = group[1]
                if len(conns) != 10:
                    err_msg = f""
                    raise UhrBoxPlugboardSettingsError(err_msg)
                for index, conn in enumerate(conns, start=1):
                    if conn not in charset:
                        err_msg = f""
                        raise UhrBoxPlugboardSettingsError(err_msg)
                    elif conn in all_conns:
                        err_msg = f""
                        raise UhrBoxPlugboardSettingsError(err_msg)
                    else:
                        index = f"{index}".rjust(2, '0')
                        ub_conns[f'{index}{group_id}'] = conn
                        all_conns.append(conn)
            return ub_conns

        conns = parse_uhr_box_connections(plugboard_str)
        conns = valid_uhr_box_groups(conns)
        if charset_flag == 'L':
            conns = format_uhr_box_letter_connections(conns)
        elif charset_flag == 'N':
            conns = format_uhr_box_number_connections(conns)
        conns = validate_uhr_box_connections(conns, charset_flag)
        return conns
    
    def valid_socket_id_character(socket_id, charset_flag):
        """
        
        """
        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        if charset_flag == "L":
            socket_id = socket_id.upper()
            if socket_id not in charset:
                err_msg = f"Invalid socket id {socket_id}!. Socket id must be in range 'A-Z'."
                raise SocketIdError(err_msg)
        elif charset_flag == "N": 
            socket_id = socket_id.ljust(2, '0')
            if socket_id not in charset:
                err_msg = f"Invalid socket id {socket_id}. Socket id must be in range '01-26'."
                raise SocketIdError(err_msg)
        
        return socket_id
    
    def valid_uhr_box_plug_id(plug_id, group=None):
        """
    
        """
        group_a_plug_ids = [
            "0A","0A","0A","0A","0A",
            "0A","0A","0A","0A","0A"
        ]
        group_b_plug_ids = [
            "0B","0B","0B","0B","0B",
            "0B","0B","0B","0B","0B"
        ]

        group = group.upper()

        if group != "A" or group != "B":
            err_msg = f"Invalid group id {group}!. Group must be 'A' or 'B'."
            raise UhrBoxPlugIdError(err_msg)

        plug_id = plug_id.upper()

        if group and group == "A":
            plug_ids = group_a_plug_ids
        elif group and group == "B":
            plug_ids = group_b_plug_ids
        else:
            plug_ids = group_a_plug_ids + group_b_plug_ids

        if plug_id not in plug_ids:
            plug_ids_str = ",".join(plug_ids)
            err_msg = f"Invalid plug id {plug_id}. Plug id must in {plug_ids_str}."
            raise UhrBoxPlugIdError(err_msg)
        
        return plug_id
    
    def valid_stecker_pb_dict(pb_dict, charset_flag, connections=None):
        """
        Valid format {}.
        Check each pb setting is valid and unique and that the minimum number of
        connections is satisfied. Return pb settings if valid or raise exception.
        """
        pb_dict = {k.upper() : v.upper() for k, v in pb_dict}

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        # check all keys are in charset
        charset_range = "A-Z" if charset_flag == "L" else "01-26"
        for socket_id in pb_dict.keys():
            if socket_id not in charset:
                err_msg = (f"Invalid socket id {socket_id}!. "
                           f"All socket ids must be in range {charset_range}.")
                raise SteckerPlugboardSettingsError(err_msg)

        # check all values are in charset
        for socket_id in pb_dict.values():
            if socket_id not in charset:
                err_msg = (f"Invalid socket id {socket_id}!. "
                           f"All socket ids must be in range {charset_range}.")
                raise SteckerPlugboardSettingsError(err_msg)

        # check connections are recipricol
        for s1 in pb_dict.keys():
            s2 = pb_dict[s1]
            s3 = pb_dict[s2]
            if s3 != s1:
                err_msg = (f"Connections are not recipricol. "
                           f"Socket id {s1} is connected to {s2} "
                           f"but socket id {s2} is connected to {s3}.")
                raise SteckerPlugboardSettingsError(err_msg)

        # check number of connections if applicable
        if connections:
            if connections not in range(1,14,1):
                err_msg = f"connections should be integer value in range 1-13."
                raise Exception(err_msg)
            conns = 0
            for s1 in pb_dict.keys():
                if pb_dict[s1] != s1:
                    conns += 1
            if conns != connections:
                err_msg = f"{connections} connections required. {conns} provided."
                raise SteckerPlugboardSettingsError(err_msg)

        return pb_dict
    
    def valid_uhr_box_pb_dict(pb_dict, charset_flag):
        """
        Valid format {}.
        Check each pb setting is valid and unique. Return pb settings if valid or
        raise exception.
        """
        pb_dict = {k.upper() : v.upper() for k, v in pb_dict}

        if charset_flag not in "LlNn":
            raise Exception(f"{charset_flag} is not a valid charset flag. Must be L,l,N or n")
        else:
            charset_flag = charset_flag.upper()

        charset = LETTERS if charset_flag == "L" else NUMBERS

        # check for correct number of plugs
        conns = len(pb_dict.keys())
        if conns != 20:
            err_msg = f"20 uhr plugs required. Only {conns} provided."
            raise UhrBoxPlugboardSettingsError(err_msg)

        # check all keys are uhr box plug ids
        plug_ids = pb_dict.keys()
            
        for group in "AB":
            for number in NUMBERS:
                plug_id = f"{group}{number}"
                if plug_id not in plug_ids:
                    err_msg = f"Invalid uhr box plug id {plug_id}!."
                    raise UhrBoxPlugboardSettingsError(err_msg)
        
        # check all socket ids are in charset
        socket_ids = pb_dict.values()

        charset_range = "A-Z" if charset_flag == "L" else "01-26"
        for socket_id in socket_ids:
            if socket_id not in charset:
                err_msg = (f"Invalid socket id {socket_id}!. "
                           f"All socket ids must be in range {charset_range}.")
                raise UhrBoxPlugboardSettingsError(err_msg)    

        # check all socket ids are unique
        if len(set(socket_ids)) != len(socket_ids):
            socket_ids_str = ",".join(socket_ids)
            err_msg = (f"Repeated socket id(s) in {socket_ids_str}. "
                       f"All socket ids must be unique.")
            raise UhrBoxPlugboardSettingsError(err_msg)

        return pb_dict