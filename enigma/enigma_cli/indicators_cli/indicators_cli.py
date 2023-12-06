from enigma_core.factory import make_machine, machine_list
from indicators.generate_indicators import generate_indicators
from indicators.filter_females import filter_females
from argparse import RawTextHelpFormatter
import re


class IndicatorsCli:

    def __init__(self, parser):
        self.parser = parser
        self._machine_data = {}
        self._load_machine_data()
        self._add_parser_arguments()


    def process_args(self, args):
        if args['indicators'] == 'generate_indicators':
            reflector = args['ref']
            rotors = self._valid_rotors(args)
            rotor_settings = self._valid_rotor_settings(args)
            ring_settings = self._valid_ring_settings(args)
            number = args['number']
            plugboard_connections = self._valid_plugboard_settings(args)
            settings = {
                "machine":"WEHRMACHT",
                "reflector":reflector,
                "rotor_types":rotors,
                "rotor_settings":rotor_settings,
                "ring_setttings":ring_settings,
                "plugboard_connections":plugboard_connections,
                "plugboard_mode":"S"
            }
            indicators = generate_indicators(settings, number)
            for indicator in indicators:
                print(indicator)

        else:
            self._filter_indicators(args)

    def _load_machine_data(self):
        machine_obj = make_machine("WEHRMACHT")
        self._machine_data = machine_obj.scrambler.collection.collection_dict()

    def _valid_reflector(self, args):
        pass

    def _valid_rotors(self, args):
        rotors = args['rotors']
        rotors = rotors.upper()
        regex = re.compile('[A-Z]+')
        rotors = re.findall(regex, rotors)
        rotors = {
            "RS":rotors[0],
            "RM":rotors[1],
            "RF":rotors[2]
	    }
        return rotors

    def _valid_rotor_settings(self, args):
        rotor_settings = args['rotor_settings']
        rotor_positions = 3
        charset = [chr(i) for i in range(65, 91)]
        valid_settings = []
        if rotor_settings:
            rotor_settings = rotor_settings.upper()
            regex = re.compile('[a-zA-Z]')
            rotor_settings = re.findall(regex, rotor_settings)
            if len(rotor_settings) != rotor_positions:
                raise Exception(f"{len(rotor_settings)} rotor settings provided. {rotor_positions} expected")

            for setting in rotor_settings:
                if setting.upper() not in charset:
                    raise ValueError(f"{setting} is not a valid rotor setting.")
                else:
                    valid_settings.append(setting.upper())
        valid_settings = {
            "RS":valid_settings[0],
            "RM":valid_settings[1],
            "RF":valid_settings[2]
	    }
        return valid_settings

    def _valid_ring_settings(self, args):
        ring_settings = args['ring_settings']
        rotor_positions = 3
        charset = [chr(i) for i in range(65, 91)]
        valid_settings = []
        if ring_settings:
            ring_settings = ring_settings.upper()
            regex = re.compile('[a-zA-Z]')
            ring_settings = re.findall(regex, ring_settings)
            if len(ring_settings) != rotor_positions:
                raise Exception(f"{len(ring_settings)} rotor settings provided. {rotor_positions} expected")

            for setting in ring_settings:
                if setting.upper() not in charset:
                    raise ValueError(f"{setting} is not a valid ring setting.")
                else:
                    valid_settings.append(setting.upper())
        valid_settings = {
            "RS":valid_settings[0],
            "RM":valid_settings[1],
            "RF":valid_settings[2]
	}
        return valid_settings

    def _valid_plugboard_settings(self, args):
        def parse_stecker_connections(connections):
            regex = re.compile(r'([a-zA-Z]+)[,;]?')
            settings = re.findall(regex, connections)
            return connections

        def format_stecker_letter_connections(connections):
            formatted = []
            regex = re.compile(r'[a-zA-Z]+\s?[a-zA-Z]*')
            connections = re.findall(regex, connections)
            for connection in connections:
                conn = ''
                for c in connection:
                    if c.upper() in [chr(i) for i in range(65, 91)]:
                        conn += c.upper()
                if len(conn) != 2:
                    raise Exception(f"Connection error. {c} was not provided as a letter pair")
                else:
                    formatted.append(conn)
            return formatted

        def validate_stecker_connections(connections):
            all_conns = []
            for conns in connections:
                for conn in conns:
                    if conn in all_conns:
                        raise Exception(f"")
                    all_conns.append(conn)
            return connections

        conns = args['plugboard_settings']
        conns = parse_stecker_connections(conns)
        conns = format_stecker_letter_connections(conns)
        conns = validate_stecker_connections(conns)
        return conns

    def _filter_indicators(self, args):
        file_path = args['indicators_file']
        with open(file_path, 'r') as f:
            indicators = f.read()
        
        indicators = indicators.split('\n')
        
        indicators = [indicator for indicator in indicators if len(indicator) == 6]

        filtered = filter_females(indicators)
        for indicator in filtered:
            print(indicator)

    def _add_parser_arguments(self):
        subparsers = self.parser.add_subparsers(dest='indicators')
        generate_traffic = subparsers.add_parser('generate_indicators', help='generates indicators', formatter_class=RawTextHelpFormatter)
        ref_str = ' | '.join(self._machine_data["REFLECTORS"])
        generate_traffic.add_argument('ref', type=str, help=f'type of reflector ( {ref_str} ){" "*11}WORD')
        rot_str = ' | '.join(self._machine_data['ROTORS_DYNAMIC'])
        generate_traffic.add_argument('rotors', type=str, help=f'types of rotors ( {rot_str} ) in format{" "*3}"RS,RM,RF"')
        generate_traffic.add_argument('rotor_settings', type=str, help=f'Rotor settings A-Z in format{" "*26}"RS,RM,RF"')
        generate_traffic.add_argument('ring_settings', type=str, help=f'Ring settings A-Z in format{" "*27}"RS,RM,RF"')
        generate_traffic.add_argument('plugboard_settings', type=str, help=f'plugboard settings in format{" "*26}"AB,CD,EF,GH,IJ,KL,M,N,O,P,QR,ST"')
        generate_traffic.add_argument('number', type=int, help=f'number of indicators{" "*34}INTEGER')

        filter_traffic = subparsers.add_parser('filter_indicators', help='filters females from indicators', formatter_class=RawTextHelpFormatter)
        filter_traffic.add_argument('indicators_file', type=str, help='indicators file path')
