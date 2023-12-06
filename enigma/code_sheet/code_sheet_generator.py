from typing import Optional, Dict, List
from itertools import permutations
import random
import json


class CodeSheetError(Exception):
    def __init__(self, message: str):
        """
        takes an error message.
        """
        super().__init__(message)


class CodeSheetGenerator:
    """
    DESCRIPTION

    1. Can generate scrambler for alpha and numeric modes.
    2. Can generate plugboard settings for alpha and numeric modes.
    3. Can generate plugboard settings for stecker and uhr box modes.

    """

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [str(i).rjust(2, '0') for i in range(1, 27)]
    UHR_BOX_PLUGS = [
        '01A','02A','03A','04A','05A','06A','07A','08A','09A','10A',
        '01B','02B','03B','04B','05B','06B','07B','08B','09B','10B'
    ]

    def __init__(self, 
                days: int, 
                reflectors: List[str], 
                rotors_dynamic: List[str], 
                rotors_static: Optional[List[str]], 
                scrambler_character_flag: str="L", 
                plugboard_character_flag: str="L", 
                plugboard_mode: str="S"
                ) -> None:
        """
        Takes an integer value of days for the number of machine settings to 
        be generated, a list of reflector ids, list of dynamic or turning 
        rotor ids, a list of static non turning rotor ids if a static rotor 
        4th being used. Optional arguments include the static rotors list, 
        scrambler character flag of 'L' or 'N' defaults to 'L'. Plugboard 
        character flag of 'L' or 'N' defaults to 'L'. Plugboard mode flag of
        'S' or 'U' defaults to 'S'. Flag values are 'L' for letters, 'N' for 
        numbers, 'S' for stecker plugboard and 'U' for uhr box plugboard.  
        """
        self.days = days
        self.reflectors = reflectors
        self.rotors_dynamic = rotors_dynamic
        self.rotors_static = rotors_static or []
        self.scrambler_flag = scrambler_character_flag
        self.plugboard_flag = plugboard_character_flag
        self.plugboard_mode = plugboard_mode
        self.settings: Dict[int, Dict] = {day : {} for day in range(1, days+1)}
        self.sh: Dict = {}
        self.code_sheet_str: Optional[str] = None
        self._valid_flags()
        self._make_code_sheet()

    def get_settings(self, day: int) -> Dict:
        """
        Takes an integer value days and generates that number of machine 
        settings.
        """
        try:
            return self.settings[day]
        except KeyError:
            msg = f""
            raise CodeSheetError(msg)

    def valid_day(self, day: int) -> bool:
        """
        Takes an integer value of days and returns True if that value is in the
        range of days provided when the code sheet was initialized else returns
        False.
        """
        try:
            self.settings[day]
        except KeyError:
            return False
        else:
            return True

    def code_sheet_string(self) -> Optional[str]:
        """
        Returns the string repressentation of the code sheet.
        """
        return self.code_sheet_str

    def write_text_file(self, fpath=None) -> None:
        """
        Writes the string repressentaion of the code sheet to a text file.
        Takes an optional file path. If no file path given writes file to
        the current directory.
        """
        fpath = fpath or "code_sheet.txt"
        with open(fpath, 'w') as f:
            if self.code_sheet_str:
                f.write(self.code_sheet_str)
            else:
                raise Exception(f"No code sheet string to write")

    def code_sheet_json(self) -> Optional[str]:
        """

	    """
        return json.dumps(self.settings, sort_keys=True, indent=4)

    def write_json_file(self, fpath=None):
        """
        Writes the JSON repressentation of the code sheet to a text file.
        Takes an optional file path. If no file path given writes file to
        the current directory.
        """
        fpath = fpath or "code_sheet.json"
        with open(fpath, 'w') as f:
            f.write(json.dumps(self.settings, sort_keys=True, indent=4))

    def _make_code_sheet(self):
        """
        Calls methods to make code sheet.
        """
        self._make_code_sheet_settings()
        self._make_code_sheet_string()

    def _make_code_sheet_settings(self):
        """
        Calls methods to make settings for scrambler and plugboard.
        """
        self._make_reflector_perms()
        self._make_rotor_perms()
        self._make_rotor_settings()
        self._make_ring_settings()
        self._make_plugboard_settings()
        self._make_uhr_box_settings()

    def _valid_flags(self):
        """
        Checks flags provided for scrambler characters, plugboard characters
        and plugboard mode are valid else raises exception.
        """
        if self.scrambler_flag not in ["L","N"]:
            raise Exception(
                f"Invalid Scrambler flag! "
                f"{self.scrambler_flag} is not a valid scrambler flag. "
                f"Must be 'L' or 'N'")
        if self.plugboard_flag not in ["L","N"]:
            raise Exception(
                f"Invalid Plugboard flag "
                f"{self.plugboard_flag} is not a valid plugboard flag. "
                f"Must be 'L' or 'N'")
        if self.plugboard_mode not in ["S","U"]:
            raise Exception(
                f"Invalid Plugboard mode "
                f"{self.plugboard_mode} is not a valid plugboard mode. "
                f"Must be 'S' or 'U'")

    def _make_reflector_perms(self):
        """
        Makes a reflector permutation for each day in the code sheet. 
        """
        for day in self.settings.keys():
            self.settings[day]["reflector"] = random.choice(self.reflectors)

    def _make_rotor_perms(self):
        """
        Makes a rotor permutation for each day in the code sheet.
        """
        rd_perms = list(permutations(self.rotors_dynamic, 3))

        for day in self.settings.keys():
            perms = list(random.choice(rd_perms))
            perms = {"RS":perms[0],"RM":perms[1],"RF":perms[2]}
            if self.rotors_static:
                perms["R4"] = random.choice(self.rotors_static)
            self.settings[day]["rotor_types"] = perms

    def _make_plugboard_settings(self):
        """
        Makes plugboard settings for the required plugboard mode.
        """
        if self.plugboard_mode == 'S':
            return self._make_stecker_pb_settings()
        elif self.plugboard_mode == 'U':
            return self._make_uhr_box_pb_connections()
        else:
            msg = (f"CodeSheetGenerator plugboard mode error!."
                   f"{self.plugboard_mode} is an invalid flag. Must be 'S' or 'U'")
            raise Exception(msg)

    def _make_uhr_box_pb_connections(self):
        """
        Makes a dictionary of uhr box connections for each day in the code
        sheet using the required character set.
        """
        charset = self.LETTERS if self.plugboard_flag == 'L' else self.NUMBERS

        for day in self.settings.keys():
            pb_connections = {}
            used = []

            for plug in self.UHR_BOX_PLUGS:
                while True:
                    char = random.choice(charset)
                    if char not in used:
                        pb_connections[plug] = char
                        used.append(char)
                        break

            self.settings[day]["plugboard_connections"] = pb_connections

    def _make_stecker_pb_settings(self):
        """
        Makes a list of stecker connections for each day in the code sheet
        and using the required character set.
        """
        charset = self.LETTERS if self.plugboard_flag == 'L' else self.NUMBERS

        for day in self.settings.keys():
            pb_connections = []
            randomized = []
            used = []
            while len(randomized) < 20:
                char = random.choice(charset)
                if char not in used:
                    randomized.append(char)
                    used.append(char)
            for i in range(10):
                pb_connections.append([randomized.pop(), randomized.pop()])
            self.settings[day]["plugboard_connections"] = pb_connections

    def _make_uhr_box_settings(self):
        """
        Makes an uhr box rotor setting for each day in the code sheet.
        """
        if self.plugboard_mode == "U":
            for day in self.settings.keys():
                self.settings[day]["uhr_box_setting"] = (random.randrange(0, 40))

    def _make_ring_settings(self):
        """
        Makes a set of ring settings for each day in the code sheet using the
        required character set.
        """
        charset = self.LETTERS if self.scrambler_flag == 'L' else self.NUMBERS

        if self.rotors_static:
            position_ids = ["RF","RM","RS","R4"]
        else:
            position_ids = ["RF","RM","RS"]

        for day in self.settings.keys():
            ring_settings = {}
            for position in range(len(position_ids)):
                ring_settings[position_ids[position]] = random.choice(charset)
            self.settings[day]["ring_settings"] = ring_settings

    def _make_rotor_settings(self):
        """
        Makes a set of rotor settings for each day in the code sheet using the 
        required character set.
        """
        charset = self.LETTERS if self.scrambler_flag == 'L' else self.NUMBERS
        positions = 4 if self.rotors_static else 3

        position_ids = ["RF","RM","RS","R4"]

        for day in self.settings.keys():
            rotor_settings = {}
            for position in range(positions):
                rotor_settings[position_ids[position]] = random.choice(charset)
            self.settings[day]["rotor_settings"] = rotor_settings

    def _make_code_sheet_string(self):
        """
        Concatenates the various settings to generate a machine setting 
        string for each day of the code sheet.
        """
        self._add_days()
        self._add_reflectors()
        self._add_rotors()
        self._add_rotor_settings()
        self._add_ring_settings()
        if self.plugboard_mode == 'U':
            self._add_uhr_settings()
            self._add_uhr_box_pb_settings()
        else:
            self._add_stecker_pb_settings()
        self.code_sheet_str = self._concat_sheet_strings()

    def _concat_sheet_strings(self):
        """
        Concats all the machine setting strings to create the string
        repressentation of the code sheet.
        """
        sheet = ""
        for day in self.sh:
            for line in self.sh[day]:
                if sheet != "":
                    sheet += '\n'
                sheet += line
        if self.plugboard_mode == 'S':
            sheet = self._make_stecker_header() + sheet
        else:
            sheet = self._make_uhr_box_header() + sheet
        return sheet

    def _make_stecker_header(self):
        """
        Makes a string header for a stecker plugboard.
        """
        x = self._rotor_types_heading_field()
        y = self._rotor_types_labels_field()
        z = self._rotor_settings_labels_field()
        q = self._rotors_types_field_size() * ' '
        w = self._ring_setting_labels_field()
        hdr = ""
        hdr += (f"| DAY | REFLECTOR |{x}| ROTOR SETTINGS | RING SETTINGS  |"
                f"           PLUGBOARD SETTINGS           |\n")
        hdr += (f"|     |           |{y}|{z}|{w}|"
                f" C0  C1  C2  C3  C4  C5  C6  C7  C8  C9 |\n")
        hdr += (f"|     |           |{q}|                |                |"
                f"                                        |\n")
        return hdr

    def _make_uhr_box_header(self):
        """
        Makes a string header for an uhr box plugboard.
        """
        x = self._rotor_types_heading_field()
        y = self._rotor_types_labels_field()
        z = self._rotors_types_field_size() * ' '
        q = self._rotor_settings_labels_field()
        w = self._ring_setting_labels_field()
        hdr = ""
        hdr += (f"| DAY | REFLECTOR |{x}| ROTOR SETTINGS | RING SETTINGS  |"
                f" UHR |           PLUGBOARD SETTINGS            |\n")
        hdr += (f"|     |           |{z}|                |                |"
                f"     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |\n")
        hdr += (f"|     |           |{y}|{q}|{w}|"
                f"     | 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B |\n")
        hdr += (f"|     |           |{z}|                |                |"
                f"     |                                         |\n")
        return hdr

    def _rotor_types_heading_field(self):
        """
        Creates a heading string to the length required to accomodate all the
        rotor settings.
        """
        return "ROTORS".center(self._rotors_types_field_size(), ' ')

    def _rotor_types_labels_field(self) -> str:
        """
        Creates the rotor types label string for a 3 or 4 rotor machine.
        """
        y = ""
        s1 = self._rotor_non_turning_field_size()
        s2 = self._rotor_turning_field_size()
        if s1 == 0:
            y = (f" {'RS'.ljust(s2)} "
                  f"{'RM'.ljust(s2)} "
                  f"{'RF'.ljust(s2)} ")
        else:
            y = (f" {'R4'.ljust(s1)} "
                  f"{'RS'.ljust(s2)} "
                  f"{'RM'.ljust(s2)} "
                  f"{'RF'.ljust(s2)} ")
        return y

    def _rotor_non_turning_field_size(self):
        """
        Returns the minimum field size required for the non turning rotor.
        """
        if self.rotors_static:
            return len(max(self.rotors_static, key=len))
        else:
            return 0

    def _rotor_turning_field_size(self) -> int:
        """
        Returns the minimum field size required for a turning rotor.
        """
        return len(max(self.rotors_dynamic, key=len))

    def _rotors_types_field_size(self) -> int:
        """
        Returns the required field size for the rotor types.
        """
        rntfs = self._rotor_non_turning_field_size()
        rtfs = self._rotor_turning_field_size()
        if rntfs != 0:
            return (rntfs + (rtfs * 3)) + 5
        else:
            return 4 + (rtfs * 3)

    def _rotor_settings_labels_field(self):
        """
        Returns the rotors field label required for a 3 or 4 rotor machine.
        """
        if self.rotors_static:
            return "  R4 RS RM RF   "
        else:
            return "   RS  RM  RF   "
        
    def _ring_setting_labels_field(self):
        """
        
        """
        if self.rotors_static:
            return "  R4 RS RM RF   "
        else:
            return "   RS  RM  RF   "

    def _add_stecker_pb_settings(self):
        """
        Creates the stecker plugboard settings strings.
        """
        for day in self.settings.keys():
            if self.plugboard_flag == 'N':
                self.sh[day][0] += f"|"
                self.sh[day][1] += f"|"
            else:
                self.sh[day][0] += f"|"
            pbs = self.settings[day]["plugboard_connections"]
            for j in range(len(pbs)):
                if self.plugboard_flag == 'N':
                    self.sh[day][0] += f" {str(pbs[j][0]).rjust(2, '0')} "
                    self.sh[day][1] += f" {str(pbs[j][1]).rjust(2, '0')} "
                else:
                    self.sh[day][0] += f" {pbs[j][0]}{pbs[j][1]} "
            if self.plugboard_flag == 'N':
                self.sh[day][0] += f"|"
                self.sh[day][1] += f"|"
            else:
                self.sh[day][0] += f"|"

    def _add_uhr_box_pb_settings(self):
        """
        
        """
        for day in self.settings.keys():
            self.sh[day][0] += f"|"
            self.sh[day][1] += f"|"
            pbs = self.settings[day]["plugboard_connections"]
            for j in range(10):
                pa = self.UHR_BOX_PLUGS[j]
                pb = self.UHR_BOX_PLUGS[j+10]
                sa = pbs[pa]
                sb = pbs[pb]
                if self.plugboard_flag == 'N':
                    self.sh[day][0] += f" {str(sa).rjust(2, '0')} "
                    self.sh[day][1] += f" {str(sb).rjust(2, '0')} "
                if self.plugboard_flag == 'L':
                    self.sh[day][0] += f" {str(sa).rjust(2, ' ')} "
                    self.sh[day][1] += f" {str(sb).rjust(2, ' ')} "
            self.sh[day][0] += f" |"
            self.sh[day][1] += f" |"

    def _add_uhr_settings(self):
        """
        Creates the uhr box rotor settings strings.
        """
        for i in range(self.days):
            day = i+1
            ubs = self.settings[day]["uhr_box_setting"]
            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day][0] += f"| {str(ubs).rjust(2, '0')}  "
                self.sh[day][1] += "|     "
            else:
                self.sh[day][0] += f"| {str(ubs).rjust(2, '0')} "

    def _add_days(self):
        """
        Creates the string repressentation for each day number.
        """
        for i in range(self.days):
            day = i+1
            day_str = f'{day}'
            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day] = [f"| {day_str.rjust(3, '0')} ","|     "]
            else:
                self.sh[day] = [f"| {day_str.rjust(3, '0')} "]

    def _add_reflectors(self):
        """
        Creates the reflector type strings.
        """
        for i in range(self.days):
            day = i+1
            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day][0] += f"|{self.settings[day]['reflector'].center(11, ' ')}"
                self.sh[day][1] += "|           "
            else:
                self.sh[day][0] += f"|{self.settings[day]['reflector'].center(11, ' ')}"

    def _add_rotors(self):
        """
        Creates the rotor type strings.
        """
        for day in self.settings.keys():
            rs = self.settings[day]["rotor_types"]
            n1 = self._rotor_turning_field_size()
            n2 = self._rotor_non_turning_field_size()
            if self.rotors_static:
                rt_str = (f"| {rs['R4'].ljust(n2, ' ')} "
                            f"{rs['RS'].ljust(n1, ' ')} "
                            f"{rs['RM'].ljust(n1, ' ')} "
                            f"{rs['RF'].ljust(n1, ' ')} ")
            else:
                rt_str = (f"| {rs['RS'].ljust(n1, ' ')} "
                            f"{rs['RM'].ljust(n1, ' ')} "
                            f"{rs['RF'].ljust(n1, ' ')} ")

            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day][0] += rt_str
                self.sh[day][1] += f"{'|' + ' ' * self._rotors_types_field_size()}"
            else:
                self.sh[day][0] += rt_str

    def _add_rotor_settings(self):
        """
        Create the rotor setting strings.
        """
        for day in self.settings.keys():
            rs = self.settings[day]["rotor_settings"]
            if self.rotors_static:
                rs_str = (f"|  {rs['R4'].rjust(2, ' ')} "
                          f"{rs['RS'].rjust(2, ' ')} "
                          f"{rs['RM'].rjust(2, ' ')} "
                          f"{rs['RF'].rjust(2, ' ')}   ")
            else:
                rs_str = (f"|   {rs['RS'].rjust(2, ' ')}  "
                          f"{rs['RM'].rjust(2, ' ')}  "
                          f"{rs['RF'].rjust(2, ' ')}   ")

            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day][0] += rs_str
                self.sh[day][1] += f"|                "
            else:
                self.sh[day][0] += rs_str

    def _add_ring_settings1(self):
        """
        Create the ring setting strings.
        """
        for i in range(self.days):
            day = i+1
            rs = self.settings[day]["ring_settings"]
            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day][0] += (f"|  {rs['RS'].rjust(2, ' ')}  "
                                    f"{rs['RM'].rjust(2, ' ')}  "
                                    f"{rs['RF'].rjust(2, ' ')}   ")
                self.sh[day][1] += "|               "
            else:
                self.sh[day][0] += (f"|  {rs['RS'].rjust(2, ' ')}  "
                                    f"{rs['RM'].rjust(2, ' ')}  "
                                    f"{rs['RF'].rjust(2, ' ')}   ")
                
    def _add_ring_settings(self):
        """
        Create the ring setting strings.
        """
        for day in self.settings.keys():
            rs = self.settings[day]["ring_settings"]
            if self.rotors_static:
                rs_str = (f"|  {rs['R4'].rjust(2, ' ')} "
                          f"{rs['RS'].rjust(2, ' ')} "
                          f"{rs['RM'].rjust(2, ' ')} "
                          f"{rs['RF'].rjust(2, ' ')}   ")
            else:
                rs_str = (f"|   {rs['RS'].rjust(2, ' ')}  "
                          f"{rs['RM'].rjust(2, ' ')}  "
                          f"{rs['RF'].rjust(2, ' ')}   ")

            if self.plugboard_flag == 'N' or self.plugboard_mode == 'U':
                self.sh[day][0] += rs_str
                self.sh[day][1] += f"|                "
            else:
                self.sh[day][0] += rs_str

if __name__ == "__main__":
    days = 32
    reflectors = ["UKW-A","UKW-B","UKW-C"]
    rotors_dynamic = ["I","II","III","IV","V","VI","VII","VIII"]
    rotors_static = ["Beta","Gamma"]
    rotors_static1 = []
    csg = CodeSheetGenerator(days, reflectors, rotors_dynamic, rotors_static1, "N","N","U")
    print(csg.code_sheet_string())
    help(CodeSheetGenerator)
