

class TextZygalskiSheet:
    """
    
    """
    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{str(i+1).rjust(2, '0')}" for i in range(26)]

    def __init__(self, settings, data):
        """
        
        """
        self.settings = settings
        self.data = data

    def __str__(self):
        """
        
        """
        return self.text_sheet()

    def text_sheet(self,
        groups,
        marker='N',
        charset="L",
        settings=True,
        meta=True):
        """
        
        """
        groups = groups or [1,2,3]
        sheet_str = ""

        if settings:
            sheet_str += self._make_machine_string()
            sheet_str += "\n"

        sheet_str += self._letter_bar() if charset == 'L' else self._number_bar()
        sheet_str += '\n'
        sheet_str += self._seperator(2) if charset == 'L' else self._seperator(3)
        sheet_str += '\n'

        for letter in self.LETTERS:
            sheet_str += self._make_line(letter, groups, marker, charset)
            sheet_str += '\n'

        sheet_str += self._seperator(2) if charset == 'L' else self._seperator(3)
        sheet_str += '\n'
        sheet_str += self._letter_bar() if charset == 'L' else self._number_bar()

        if meta:
            sheet_str += "\n\n"
            sheet_str += self._meta_string(groups)

        return sheet_str

    def _number_bar(self):
        """
        
        """
        _str = "   0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2\n"
        _str += "   1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6"
        return _str

    def _letter_bar(self):
        """
        
        """
        _str = "  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        return _str

    def _seperator(self, n):
        """
        
        """
        _str = " "*n 
        _str += "| "*26
        return _str

    def _rotor_types_string(self):
        """
        
        """
        st = self.settings["reflector"]
        rs = self.settings["rotor_types"]
        if "R4" in rs:
            st += f"_{rs['R4']}"
        st += f"_{rs['RS']}_{rs['RM']}_{rs['RF']}"
        return st

    def _make_machine_string(self):
        """
        
        """
        _str = f"{' '*16}{self.settings['machine_type']}\n\n"
        _str += self._make_scrambler_string()
        _str += "\n\n"
        _str += self._make_plugboard_string()
        _str += "\n"
        return _str

    def _make_scrambler_string(self):
        """
	    Returns the string repressentation of the scrambler.
        """
        sd = self.settings
        rotors_length = len(sd["rotor_settings"].keys())*6

        def header_string():
            """
            
            """
            header_str = f"{' '*17}REFLECTOR{' '*4}"
            header_str += "ROTORS".center(rotors_length, ' ')
            header_str += '\n'
            return header_str

        def positions_string():
            """
            
            """
            position_str = "POSITIONS".ljust(31, ' ')
            positions = list(sd["rotor_types"].keys())
            for position in positions:
                position_str += f" {position.center(4, '-')} "
            position_str += '\n'
            return position_str

        def types_string():
            """
            
            """
            types_str = "TYPES".ljust(17, ' ')
            ref_id = sd["reflector"] or "--"
            types_str += ref_id.center(9, ' ')
            types_str += ' '*5
            rotor_types = sd["rotor_types"]
            positions = list(rotor_types.keys())
            for position in positions:
                rotor_id = rotor_types[position] or "--"
                types_str += rotor_id.center(6, ' ')
            types_str += '\n'
            return types_str

        def rotor_settings_string():
            """
            
            """
            settings_str = "ROTOR SETTINGS".ljust(31, ' ')
            rotor_settings = sd["rotor_settings"]
            positions = list(rotor_settings.keys())
            for position in positions:
                if position in ["RM","RF"]:
                    rotor_setting = "--"
                else:
                    rotor_setting = rotor_settings[position]
                settings_str += rotor_setting.center(6, ' ')
            settings_str += '\n'
            return settings_str

        def ring_settings_string():
            """
            
            """
            settings_str = "RING SETTINGS".ljust(31, ' ')
            ring_settings_str = ""
            ring_settings = sd["ring_settings"]
            positions = list(ring_settings.keys())
            for position in positions:
                ring_setting = ring_settings[position] or "--"
                ring_settings_str += ring_setting.center(6, ' ')
            settings_str += ring_settings_str.rjust(rotors_length, ' ')
            return settings_str

        scrambler_str = header_string()
        scrambler_str += positions_string()
        scrambler_str += types_string()
        scrambler_str += rotor_settings_string()
        scrambler_str += ring_settings_string()
        return scrambler_str
	    
    def _make_plugboard_string(self):
        """

        """
        def make_line(line, left_pad):
            pb_line = f"{left_pad}"
            pb_line += '  '.join([f"{str(charset[i]).ljust(2, pad)}" for i in line])
            pb_line += f"\n{left_pad}"
            pb_line += '  '.join([f"{str(connections[charset[i]]).ljust(2, pad)}" for i in line])
            return pb_line

        layout = [
            [16,22,4,17,19,25,20,8,14],
            [0,18,3,5,6,7,9,10],
            [15,24,23,2,21,1,12,13,11]
        ]

        charset_flag = self.settings["plugboard_char_set_flag"]
        charset = self.LETTERS if charset_flag == "L" else self.NUMBERS
        conns = {c:c for c in charset}
        conns1 = {c[0]:c[1] for c in self.settings["plugboard_connections"]}
        conns2 = {c[1]:c[0] for c in self.settings["plugboard_connections"]}
        connections = {**conns, **conns1, **conns2}

        pad = ' ' if charset_flag == 'L' else '0'
        pb_str = ""
        pb_str += make_line(layout[0], '  ')
        pb_str += '\n'
        pb_str += make_line(layout[1], '    ')
        pb_str += '\n'
        pb_str += make_line(layout[2], '  ')
        return pb_str    

    def _make_line(self, row, groups, marker, charset):
        """
        
        """
        line = ""
        if charset == 'L':
            line += f"{row}-"
        else:
            line += f"{self.NUMBERS[self.LETTERS.index(row)]}-"
        for index, letter in enumerate(self.LETTERS, start=1):
            setting_data = self.data["data"][f"{row}{letter}"]
            num = 0
            if setting_data["G1"] and 1 in groups:
                num += 1
            if setting_data["G2"] and 2 in groups:
                num += 2
            if setting_data["G3"] and 3 in groups:
                num += 4
            if marker == 'N':
                line += f"{str(num)}"
            if marker == '1':
                line += '0' if num == 0 else '1'
            if index < len(self.LETTERS):
                line += ' '
        if charset == 'L':
            line += f"-{row}"
        else:
            line += f"-{self.NUMBERS[self.LETTERS.index(row)]}"
        return line
    
    def _meta_string(self, groups):
        """
        
        """
        _str = f"RM RF G1{' '*18}G2{' '*18}G3\n\n"
        for setting in self.data["data"]:
            setting_data = self.data["data"][setting]
            if setting_data["G1"] or setting_data["G2"] or setting_data["G3"]:
                _str += f"{setting[0]}  {setting[1]}  "
                for n in [1,2,3]:
                    group_str = ""
                    if n in groups:
                        group_data = setting_data[f"G{n}"]
                        used = []
                        for pair in group_data:
                            if pair[0] not in used:
                                used.append(pair[0])
                                used.append(pair[1])
                                group_str += f"{pair[0]},{pair[1]} "
                    group_str = group_str.ljust(20, ' ')
                    _str += group_str
                _str += '\n'
            else:
                _str += f"{setting[0]}  {setting[1]}\n"
        return _str
