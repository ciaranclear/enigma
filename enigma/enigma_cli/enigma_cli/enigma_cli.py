from enigma_core.factory import make_machine, machine_list
import argparse
import json
import re
import os


class CommandLineEnigmaCli:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2, '0') for i in range(26)]

    def __init__(self, parser):
        self._parser = parser
        self._machine_data = {}
        self._load_machine_data()
        self._add_parser_arguments()
        self._machine = None
        self._reflector = None
        self._rotors = None
        self._rotor_settings = None
        self._ring_settings = None
        self._scrambler_mode = None
        self._charset_flag = None
        self._charset = None
        self._plugboard_mode = None
        self._plugboard_connections = None
        self._uhr_box_setting = None
        self._input_file_path = None
        self._output_file_path = None
        self._msg = None

    def process_args(self, args):

        self._valid_machine_type(args)
        self._valid_reflector(args)
        self._valid_rotors(args)
        self._valid_rotor_settings(args)
        self._valid_ring_settings(args)
        self._valid_plugboard_settings(args)
        self._valid_output_file(args)
        self._get_machine_output()

    def _valid_machine_type(self, args):
        machine = args['machine']
        machine = machine.upper()
        for mach in self._machine_data:
            if mach.upper() == machine.upper():
                self._machine = mach
                return mach
        raise ValueError(f"machine type {machine} is not a valid enigma")

    def _valid_reflector(self, args):
        reflector = args['reflector']
        reflector = reflector.upper()
        reflectors = self._machine_data[self._machine]['REFLECTORS']
        for ref in reflectors:
            if reflector.upper() == ref.upper():
                self._reflector = ref
                return ref
        raise ValueError(f"reflector type {reflector} is not a valid reflector type for enigma machine {self._machine}") 

    def _valid_rotors(self, args):
        rotors = args['rotors']
        rotors = rotors.upper()
        regex = re.compile('[A-Z]+')
        rotors = re.findall(regex, rotors)
        rotor_positions = 4 if self._machine_data[self._machine]['ROTORS_STATIC'] else 3

        valid_rotors = []

        if len(rotors) != len(set(rotors)):
            raise Exception(f"{rotors} contains a repeated value. All rotors must be unique.")

        if len(rotors) != rotor_positions:
            raise Exception(f"{rotor_positions} rotor types required {len(rotors)} provided.")

        rotors_static = self._machine_data[self._machine]['ROTORS_STATIC']
        rotors_dynamic = self._machine_data[self._machine]['ROTORS_DYNAMIC']

        if rotor_positions == 4:
            rotor_static = rotors.pop(0)
            valid_rotor = False
            for rotor in rotors_static:
                if rotor_static.upper() == rotor.upper():
                    valid_rotors.append(rotor)
                    valid_rotor = True
            if not valid_rotor:
                raise ValueError(f"{rotor_static} is not a valid static rotor for {self._machine} enigma.")
            	
        for r1 in rotors:
            valid_rotor = False
            for r2 in rotors_dynamic:
                if r1.upper() == r2.upper():
                    valid_rotors.append(r2)
                    valid_rotor = True
            if not valid_rotor:
                raise ValueError(f"{r1} is not a valid dynamic rotor type for a {self._machine} enigma.")
        valid_rotors.reverse()
        rotor_positions = ["RF","RM","RS","R4"]
        rotors_dict = {rotor_positions[i]:valid_rotors[i] for i in range(len(valid_rotors))}
        self._rotors = rotors_dict
        return rotors_dict

    def _valid_rotor_settings(self, args):
        rotor_settings = args['rot_settings']
        rotors_static = self._machine_data[self._machine]['ROTORS_STATIC']
        rotor_positions = 4 if self._machine_data[self._machine]['ROTORS_STATIC'] else 3
        valid_settings = []
        if rotor_settings:
            rotor_settings = rotor_settings.upper()
            regex = re.compile('[a-zA-Z0-9]+')
            rotor_settings = re.findall(regex, rotor_settings)
            if len(rotor_settings) != rotor_positions:
                raise Exception(f"{len(rotor_settings)} rotor settings provided. {rotor_positions} expected")

            for setting in rotor_settings:
                if self._charset_flag == 'N': setting = setting.rjust(2, '0')
                if setting.upper() not in self._charset:
                    raise ValueError(f"{setting} is not a valid rotor setting.")
                else:
                    valid_settings.append(setting.upper())
        valid_settings.reverse()
        rotor_positions = ["RF","RM","RS","R4"]
        rotor_settings_dict = {rotor_positions[i]:valid_settings[i] for i in range(len(valid_settings))}
        self._rotor_settings = rotor_settings_dict
        return rotor_settings_dict

    def _valid_ring_settings(self, args):
        ring_settings = args['rng_settings']
        valid_settings = []
        if ring_settings:
            ring_settings = ring_settings.upper()
            regex = re.compile('[a-zA-Z0-9]+')
            ring_settings = re.findall(regex, ring_settings)
            for setting in ring_settings:
                if self._charset_flag == 'N': setting = setting.rjust(2, '0')
                if setting.upper() not in self._charset:
                    raise ValueError(f"{setting} is not a valid ring settting.")
                else:
                    valid_settings.append(setting.upper())
        valid_settings.reverse()
        rotor_positions = ["RF","RM","RS","R4"]
        ring_settings_dict = {rotor_positions[i]:valid_settings[i] for i in range(len(valid_settings))}
        self._ring_settings = ring_settings_dict
        return ring_settings_dict

    def _valid_plugboard_settings(self, args):

        def parse_uhr_box_connections(connections):
            regex = re.compile(r'(?P<id>[abAB])=\[(?P<plugs>[a-zA-Z0-9,; ]+)\]')
            connections = re.findall(regex, connections)
            return connections

        def parse_stecker_connections(connections):
            regex = re.compile(r'([a-zA-Z0-9 ]+)[,;]?')
            settings = re.findall(regex, connections)
            return connections

        def valid_uhr_box_groups(connections):
            for group in connections:
                if group[0] not in ('a','A','b','B'):
                    raise Exception(f"Invalid uhr box group id {group[0]}. Must be 'A' or 'B'")

            letter_range = 'A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]'
            number_range = 'A=[1,2,3,4,5,6,7,8,9,10] B=[11,12,13,14,15,16,17,18,19,20]'
            charset_range = letter_range if self._charset_flag == 'L' else number_range
            if len(connections) != 2:
                raise Exception(
                    f"Incorrect uhr box plugboard connections.\n"
		    f"Must be in the format {charset_range}")
            return connections

        def format_uhr_box_letter_connections(connections):
            #filter out non letter chars and convert to upper case
            formatted = []
            for group in connections:
                group_id = group[0].upper()
                conns = group[1]
                conn_str = ''
                for conn in conns:
                    if conn.upper() in self.LETTERS:
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

        def format_stecker_letter_connections(connections):
            formatted = []
            regex = re.compile(r'[a-zA-Z]+\s?[a-zA-Z]*')
            connections = re.findall(regex, connections)
            for connection in connections:
                conn = ''
                for c in connection:
                    if c.upper() in self.LETTERS:
                        conn += c.upper()
                if len(conn) != 2:
                    raise Exception(f"Connection error. {c} was not provided as a letter pair")
                else:
                    formatted.append(conn)
            return formatted

        def format_stecker_number_connections(connections):
            formatted = []
            regex = re.compile(r'\d+ \d+')
            connections = re.findall(regex, connections)
            regex = re.compile(r'\d+')
            for conns in connections:
                conns = re.findall(regex, conns)
                fconns = []
                for conn in conns:
                    fconns.append(conn.rjust(2, '0'))
                formatted.append(fconns)
            return formatted

        def validate_uhr_box_connections(connections):
            all_conns = []
            ub_conns = {}
            for group in connections:
                group_id = group[0]
                conns = group[1]
                if len(conns) != 10:
                    raise Exception(f"")
                for index, conn in enumerate(conns, start=1):
                    if conn not in self._charset:
                        raise Exception(f"")
                    elif conn in all_conns:
                        raise Exception()
                    else:
                        index = f"{index}".rjust(2, '0')
                        ub_conns[f'{index}{group_id}'] = conn
                        all_conns.append(conn)
            return ub_conns

        def validate_stecker_connections(connections):
            all_conns = []
            #check for unique connections
            for conns in connections:
                for conn in conns:
                    if conn in all_conns:
                        raise Exception(f"")
                    all_conns.append(conn)
            return connections

        conns = args['plugboard_connections']
        if self._plugboard_mode == 'S' and conns:
            conns = parse_stecker_connections(conns)
            if self._charset_flag == 'L':
                conns = format_stecker_letter_connections(conns)
            elif self._charset_flag == 'N':
                conns = format_stecker_number_connections(conns)
            conns = validate_stecker_connections(conns)
        elif self._plugboard_mode == 'U' and conns:
            conns = parse_uhr_box_connections(conns)
            conns = valid_uhr_box_groups(conns)
            if self._charset_flag == 'L':
                conns = format_uhr_box_letter_connections(conns)
            elif self._charset_flag == 'N':
                conns = format_uhr_box_number_connections(conns)
            conns = validate_uhr_box_connections(conns)
        self._plugboard_connections = conns

    def _valid_output_file(self, args):
        output_file = args['output_file']
        if output_file:
            dirpath = os.path.split(output_file)[0]
            if dirpath != '' and  not os.path.isdir(dirpath):
                raise Exception(f"{dirpath} is not a valid directory path.")
            self._output_file_path = output_file

    def _get_machine_output(self):
        settings = self._make_settings_dict()
        machine_obj = make_machine(self._machine)
        machine_obj.settings = settings

        settings = machine_obj.settings

        outp = ""
        for c in self._msg:
            o = machine_obj.character_input(c)
            if o:
                outp += o
        outp += '\n'
        if self._output_file_path:
            with open(self._output_file_path, 'w') as f:
                f.write(outp)
        else:
            print(outp)
        
    def _make_settings_dict(self):
        settings = {
            'machine':self._machine,
            'reflector':self._reflector,
            'rotor_types':self._rotors
        }
        if self._rotor_settings: settings['rotor_settings'] = self._rotor_settings
        if self._ring_settings: settings['ring_settings'] = self._ring_settings
        if self._scrambler_mode != None:
            settings['turnover_flag'] = self._scrambler_mode
        if self._plugboard_mode: settings['plugboard_mode'] = self._plugboard_mode
        if self._plugboard_connections: settings['plugboard_connections'] = self._plugboard_connections
        if self._uhr_box_setting: settings['uhr_box_setting'] = self._uhr_box_setting
        if self._charset_flag:
            settings['scrambler_char_set_flag'] = self._charset_flag
            settings['plugboard_char_set_flag'] = self._charset_flag
        
        return settings 
        
    def _load_machine_data(self):
        machines = machine_list()
        
        for machine in machines:
            machine_obj = make_machine(machine)
            self._machine_data[machine] = machine_obj.scrambler.collection.collection_dict()

    def _add_parser_arguments(self):
        self._add_machine_arg()
        self._add_reflector_arg()
        self._add_rotors_arg()
        self._add_inputs_arg()
        self._add_rotor_settings_arg()
        self._add_ring_settings_arg()
        self._add_scrambler_mode_arg()
        self._add_character_set_arg()
        self._add_plugboard_mode_arg()
        self._add_uhr_box_setting_arg()
        self._add_plugboard_settings_arg()
        self._add_output_arg()

    def _add_machine_arg(self):
        machines = self._machine_data.keys()
        machines_str = " | ".join(machines)
        machines_str = f"( {machines_str} )"
        self._parser.add_argument('machine', type=str, help=f'Enigma machine type {machines_str}')

    def _add_reflector_arg(self):
        reflector_strs = {}

        for machine in self._machine_data:
            reflectors = self._machine_data[machine]["REFLECTORS"]
            reflector_str = " | ".join(reflectors)
            reflector_strs[machine] = f"( {reflector_str} )"
 
        ref_strs = "\n"
        for machine, ref_str in reflector_strs.items():
            ref_strs += f"{machine}".ljust(25, ' ')
            ref_strs += f"{ref_str}"
            ref_strs += '\n'

        self._parser.add_argument(
            'reflector',
            type=str,
            help=f'Reflector type in format "REF" {ref_strs}')

    def _add_rotors_arg(self):
        rotor_strs = {}

        for machine in self._machine_data:
            rotors_static = self._machine_data[machine]["ROTORS_STATIC"]
            rotors_dynamic = self._machine_data[machine]["ROTORS_DYNAMIC"]
            rotors_static_str = " | ".join(rotors_static)
            rotors_dynamic_str = ", ".join(rotors_dynamic)
            rotor_strs[machine] = (f"( {rotors_static_str} )".ljust(17, ' ') 
	                         + f" [{rotors_dynamic_str}]")
 
        rot_strs = "\n"
        for machine, rot_str in rotor_strs.items():
            rot_strs += f"{machine}".ljust(25, ' ')
            rot_strs += f"{rot_str}"
            rot_strs += '\n'

        self._parser.add_argument('rotors',
            type=str,
            help=f'Rotor types in format "R4,RS,RM,RF" or "RS,RM,RF" where\n'
                 f'R4 = Static Rotor if applicable\n'
                 f'RS = Slow Rotor\n'
                 f'RM = Middle Rotor\n'
                 f'RF = Fast Rotor\n'
                 f' {rot_strs}')

    def _add_inputs_arg(self):
        def input_file(v):
            with open(v, 'r') as f:
                msg = f.read()
                self._msg = msg
                return msg

        def input_msg(v):
            msg = v
            self._msg = msg
            return msg
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument('-i', '--input-file', type=input_file, help='The input file path')
        group.add_argument('--message', type=input_msg, help='The message string')
        group.required = True

    def _add_rotor_settings_arg(self):
        self._parser.add_argument(
            '--rot-settings', 
            type=str,
            help='Rotor settings in format [R4,RS,RM,RF] or [RS,RM,RF]')

    def _add_ring_settings_arg(self):
        self._parser.add_argument(
            '--rng-settings',
            type=str,
            help='Ring settings in format [RS,RM,RF]')

    def _add_scrambler_mode_arg(self):
        def isBool(v):
            mode = None
            if isinstance(v, bool):
                mode = v
            if v.lower() == 'true':
                mode = True
            elif v.lower() == 'false':
                mode = False
            if mode == None:
                raise argparse.ArgumentTypeError('Boolean value expected')
            self._scrambler_mode = mode
            return mode

        self._parser.add_argument(
            '--scrambler-mode',
            type=isBool,
            help='Scrambler turnover mode ( True | False )')

    def _add_character_set_arg(self):
        def validCharSet(v):
            if v.upper() in ('L','N'):
                v = v.upper()
                self._charset_flag = v
                self._charset = self.LETTERS if v == 'L' else self.NUMBERS
                return v
            else:
                raise argparse.ArgumentTypeError('"L" or "N" expected')
        self._parser.add_argument(
            '-c',
            '--charset',
            type=validCharSet, 
            help=f'Machine character set ( L | N ) where\n'
                 f'L = Letters\n'
                 f'N = Numbers')

    def _add_plugboard_mode_arg(self):
        def validPBMode(v):
            v = v.upper()
            if v in ('S','U'):
                self._plugboard_mode = v
                return v
            else:
                raise argparse.ArgumentTypeError('"S" or "U" expected')
        self._parser.add_argument(
            '--plugboard-mode',
            type=validPBMode, 
            help=f'Plugboard mode ( S | U ) where\n'
                 f'S = Stecker\n'
                 f'U = Uhr Box')

    def _add_uhr_box_setting_arg(self):
        def validUBSet(v):
            v = int(v)
            if v in range(40):
                self._uhr_box_setting = v
                return v
            else:
                raise argparse.ArgumentTypeError(f'{v} is not a valid uhr box setting. Must be in range "00"-> "39"')
        self._parser.add_argument(
            '--uhr-box-setting',
            type=validUBSet,
            help='Uhr box setting in range 0 - 39')

    def _add_plugboard_settings_arg(self):
        self._parser.add_argument(
            '--plugboard-connections',
            type=str,
            help=f'Plugboard settings for stecker mode\n'
                 f'in format [AB,CD,EF,GH,IJ,KL,M,N,O,P,QR,ST] letters mode\n'
                 f'in format [1 2,3 4,5 6,7 8,9 10,11 12,13,14,15 16,17,18,19 20] numbers mode\n'
                 f'Plugboard settings for uhr box mode\n'
                 f'in format "A=[A,B,C,D,E,F,G,H,I,J] '
                 f'B=[K,L,M,N,O,P,Q,R,S,T]" letter mode\n'
                 f'in format "A=[1,2,3,4,5,6,7,8,9,10] '
                 f'B=[11,12,13,14,15,16,17,18,19,20]" number mode')

    def _add_output_arg(self):
        self._parser.add_argument(
            '-o',
            '--output-file',
            type=str,
            help='The output file path')
