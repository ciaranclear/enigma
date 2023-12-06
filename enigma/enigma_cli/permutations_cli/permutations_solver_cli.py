from indicators.filter_females import filter_females
from scrambler_permutations.scrambler_permutations import ScramblerPermutations
from argparse import RawTextHelpFormatter

        
class PermutationsSolverCli:

    def __init__(self, parser):
        self.parser = parser
        self._add_arguments()

    def process_args(self, args):

        indicators_fpath = args['indicators_file']

        with open(indicators_fpath, 'r') as f:
            indicators_str = f.read()

        indicators = indicators_str.split('\n')
        
        indicators = [indicator for indicator in indicators if len(indicator) == 6]
        
        indicators = filter_females(indicators)
        
        sp = ScramblerPermutations(indicators)
        
        permutations = sp.filter_permutations()

        for perm in permutations:
            l = perm["rotor_settings"]["RS"]
            ref = perm["reflector"]
            rs = perm["rotor_types"]["RS"]
            rm = perm["rotor_types"]["RM"]
            rf = perm["rotor_types"]["RF"]

            print(f"{l}_{ref}_{rs}_{rm}_{rf}")

    def _add_arguments(self):
        self.parser.add_argument('indicators_file', type=str, help='indicators file path')