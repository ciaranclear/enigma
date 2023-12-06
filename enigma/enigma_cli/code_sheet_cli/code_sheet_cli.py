from enigma_core.factory import make_machine, machine_list
from code_sheet.code_sheet_generator import CodeSheetGenerator
import argparse
import json
import os


class CodeSheetCli:

    def __init__(self, parser):
        self._parser = parser
        self._machine = None
        self._plugboard_mode = None
        self._days = None
        self._charset_flag = None
        self._output = None
        self._machine_data ={}
        self._load_machine_data()
        self._add_parser_arguments()

    def process_args(self, args):
        reflectors = self._machine_data[self._machine]['REFLECTORS']
        rotors_dynamic = self._machine_data[self._machine]['ROTORS_DYNAMIC']
        rotors_static = self._machine_data[self._machine]['ROTORS_STATIC']
        
        generator = CodeSheetGenerator(
            self._days,
            reflectors,
            rotors_dynamic,
            rotors_static,
            scrambler_character_flag = self._charset_flag,
            plugboard_character_flag = self._charset_flag,
            plugboard_mode = self._plugboard_mode
	)

        output = None
        if self._format == 'S':
            output = generator.code_sheet_string()
        elif self._format == 'J':
            output = generator.code_sheet_json()
        
        if self._output:
            with open(self._output, 'w') as f:
                f.write(output)
        else:
            print(output)

    def _load_machine_data(self):
        machines = machine_list()

        for machine in machines:
            machine_obj = make_machine(machine)
            self._machine_data[machine] = machine_obj.scrambler.collection.collection_dict()

    def _add_parser_arguments(self):
        self._add_machine_arg()
        self._add_output_format_arg()
        self._add_plugboard_mode_arg()
        self._add_days_arg()
        self._add_charset_arg()
        self._add_output_arg()

    def _add_machine_arg(self):
        def valid_machine_type(machine):
            machine = machine.upper()
            for mach in self._machine_data:
                if mach.upper() == machine:
                    self._machine = mach
                    return mach
            raise ValueError(f"machine type {machine} is not a valid enigma machine")

        machines = self._machine_data.keys()
        machines_str = " | ".join(machines)
        machines_str = f"( {machines_str} )"
        self._parser.add_argument('machine', type=valid_machine_type, help=f'Enigma machine type {machines_str}')

    def _add_output_format_arg(self):
        def valid_output_format(_format):
            if _format.upper() not in ('S','J'):
                raise ValueError(f'')
            self._format = _format.upper()
            return _format.upper()
        self._parser.add_argument('format', type=valid_output_format, help='output format ( string format "S" | json format "J" )')

    def _add_plugboard_mode_arg(self):
        def valid_plugboard_mode(mode):
            if mode == None:
                mode = 'S'
            if mode.upper() not in ('S','U'):
                raise ValueError(f'Invalid plugboard mode {mode} must be "S" or "U"')
            self._plugboard_mode = mode.upper()
            return mode.upper()
        self._parser.add_argument('plugboard-mode', type=valid_plugboard_mode, help='Plugboard mode ( stecker "S" | uhr box "U" )')

    def _add_days_arg(self):
        def valid_days(days):
            if days == None:
                days = 1
            else:
                try:
                    days = int(days)
                except ValueError:
                    raise ValueError(f'')
            if 1 <= days <= 999:
                self._days = days
                return days
            else:
                raise ValueError(f'')
        self._parser.add_argument('days', type=valid_days, help='Number of days integer value 1-999')

    def _add_charset_arg(self):
        def valid_charset(charset):
            if charset.upper() not in ('L','N'):
               raise ValueError(f'')
            self._charset_flag = charset.upper()
            return charset
        self._parser.add_argument('charset', type=valid_charset, help='Machine character set ( letters "L" | numbers "N" )')

    def _add_output_arg(self):
        def valid_output_file(file_path):
            dirpath = os.path.split(file_path)[0]
            if dirpath != '' and not os.path.isdir(dirpath):
                raise ValueError(f'Invalid file path {file_path}')
            else:
                self._output = file_path
        self._parser.add_argument('-o', '--output-file', type=valid_output_file, help='The output-file path')
