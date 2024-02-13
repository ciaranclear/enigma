"""
STEPS

1. Take a cipher text and plain text string as input.
2. Check that each letter in the plain text is not the same as the letter in the cipher text at the same position.
3. Make a menu using the crib and find all the loops.
4. Use the menu to plug up the scramblers on the bombe.
5. Inputs will be made into the cable of the most common letter in the menu.
6. For each wheel setting the letters A-Z will be input to the bombe.
7. If a letter is input and returns as itself and there are no contradictions present then the input letter is
   steckered with the cable letter. The wire letter in the other applicable cables are steckered to there cable
   letter.
8. Record the stop position and the stecker settings.
9. Run the machine until all rotor settings have been exhausted.

TEST EXAMPLE

REFLECTOR TYPE:         UKW-B
ROTOR TYPES:            III     II      I
ROTOR SETTINGS:         A       A       V
RING SETTINGS:          A       A       A
PLUGBOARD SETTINGS:     AC,BD,EG,FH,IK,JL,MO,NP,QS,RT
PERMUTATION:            UKW-B_III_II_I

PLAIN TEXT:             WEATHERFORECASTBISCAY
CIPHER TEXT:            YHXBDYCWCJAQPBLMHMBGP
"""

from enigma_core.factory import make_machine
from enigma_core.validators.scrambler_validators import ScramblerValidators, PermutationError
from enigma_tools.setting_tools.setting_tools import RotorSettings
from collections import deque
from pprint import pprint


class TuringBombe:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self, plain_text, cipher_text, permutation, test_register):
        self._plain_text = plain_text
        self._cipher_text = cipher_text
        self._permutation = permutation
        self._test_register = test_register
        self._cables = {}
        self._registers = {l:[False for i in range(26)] for l in self.LETTERS}
        self._stops = []
        self.machine = make_machine("WEHRMACHT")
        self.rotor_settings_gen = RotorSettings('L', 3)
        self._perm = self._valid_permutation()
        self._initialize_machine()
        self._valid_crib()

    def solve(self):
        # validate permutation
        # validate crib
        # find loops
        # wire bombe
        # if no loops raise exception

        # for each rotor position input each letter into the test registry
        while True:
            settings = self.rotor_settings_gen.settings
            rs = settings["RS"]
            rm = settings["RM"]
            rf = settings["RF"]
            print(f"RS {rs} RM {rm} RF {rf}")
            self._set_machine()
            self._wire_bombe()
            self._check_stop()

            try:
                self.rotor_settings_gen.inc()
            except StopIteration:
                break
        # when rotor settings exhausted return the stops
        pprint(self._stops)
        return self._stops
    
    def solve1(self):
        self._test()

    def _valid_permutation(self):
        try:
            perm = ScramblerValidators.valid_permutation(self._permutation, True, True)
            return perm
        except PermutationError:
            pass
        try:
            perm = ScramblerValidators.valid_permutation(self._permutation, False, True)
            return perm
        except PermutationError:
            pass
        try:
            perm = ScramblerValidators.valid_permutation(self._permutation, False, False)
            return perm
        except PermutationError:
            err_msg = f"Permutation {self.permutation} is not a valid permutation."
            raise PermutationError(err_msg)

    def _valid_crib(self):

        self._plain_text = self._plain_text.upper()
        self._cipher_text = self._cipher_text.upper()

        if len(self._plain_text) != len(self._cipher_text):
            err_msg = (f"Plain text is length {len(self._plain_text)} and the cipher text is length {len(self._cipher_text)}\n. "
                       f"Plain text and cipher text Must be the same length.")
            raise Exception(err_msg)

        for l in self._plain_text:
            if l not in self.LETTERS:
                err_msg = f"Character {l} in plain text is not valid. Must be A-Z."
                raise Exception(err_msg)

        for i in self._cipher_text:
            if l not in self.LETTERS:
                err_msg = f"Character {l} in cipher text is not valid. Must be A-Z."
                raise Exception(err_msg)

        for i in range(len(self._plain_text)):
            if self._plain_text[i] == self._cipher_text[i]:
                err_msg = (f"Plain text and cipher text has the same letter {self._plain_text[i]} at index {i}. "
                           f"A letter at an index in the plain text must be different "
                           f"from the letter in the cipher text at the same index.")
                raise Exception(err_msg)

    def _wire_bombe(self):
        self.cables = {l:[] for l in self.LETTERS}
        for i in range(len(self._plain_text)):
            c1 = self._plain_text[i]
            c2 = self._cipher_text[i]
            self.machine.character_input('A')

            c1_dict = {}
            c2_dict = {}

            for cin in self.LETTERS:
                cout = self.machine.non_keyed_input(cin)
                c1_dict[cin] = f"{c2}{cout}"
                c2_dict[cout] = f"{c1}{cin}"

            self.cables[c1].append(c1_dict)
            self.cables[c2].append(c2_dict)

    def _trace_paths(self, cable, wire):
        """
        1. Set wire in cable to True.
        2. Set wire in diagonal connection to True.
        3. For each connected scrambler in that cable set its connected wire to True.
        4. Record each visited wire so as not to visit the same wire twice.
        """
        wires = []
        self._trace_path(cable, wire, wires)

    def _trace_path(self, cable, wire, wires):
        menu_letters = list(set(self._plain_text + self._cipher_text))

        # set the wire in the given cable to True
        self._registers[cable][self.LETTERS.index(wire)] = True
        # record this wire as visited
        wires.append(f"{cable}{wire}")

        # if cable in menu_letters set wire in diagonal board to True
        if (cable != wire) and wire in menu_letters and f"{wire}{cable}" not in wires:
            self._trace_path(wire, cable, wires)
        
        for scrambler in self.cables[cable]:
            wire_id = scrambler[wire]
            connected_cable = wire_id[0]
            connected_wire = wire_id[1]
            if wire_id not in wires:
                self._trace_path(connected_cable, connected_wire, wires)

    def _reset_registers(self):
        self._registers = {l:[False for i in range(26)] for l in self.LETTERS}

    def _initialize_machine(self):
        rot_settings = self.rotor_settings_gen.settings
        perm_dict = self._perm[1]
        settings = {
            "reflector":perm_dict["REF"],
            "rotor_types":{
                "RS":perm_dict["ROT_RS"],
                "RM":perm_dict["ROT_RM"],
                "RF":perm_dict["ROT_RF"]
            },
            "rotor_settings":{
                "RS":rot_settings["RS"],
                "RM":rot_settings["RM"],
                "RF":rot_settings["RF"]
            },
            "ring_settings":{"RS":"A","RM":"A","RS":"A"},
            "turnover_flag":False
        }
        self.machine.settings = settings

    def _set_machine(self):
        rot_settings = self.rotor_settings_gen.settings
        settings = {
            "rotor_settings":{
                "RS":rot_settings["RS"],
                "RM":rot_settings["RM"],
                "RF":rot_settings["RF"]
            }
        }
        self.machine.settings = settings

    def _check_stop(self):
        # stop if a letter comes back as itself in the test registry
        # if stopped check for contradictions
        # if no contradictions record rotor settings and plugboard settings
        # select test registry from longest loop in loops

        for l in self.LETTERS:
            self._trace_paths(self._test_register, l)

            if self._is_stop(self._test_register, l):
                if not self._contradictions():
                    print("STOP")
                    self._print_rotor_settings()
                    self._print_registry(self._test_register, 'A')
                    self._stops.append(
                        {
                            "rotor_settings":self.rotor_settings_gen.settings,
                            "stecker_pairs":self._get_stecker_pairs()
                        }
                    )

            self._reset_registers()

    def _is_stop(self, test_registry, l):
        ind = self.LETTERS.index(l)

        if self._registers[test_registry].count(True) == 1:
            return True

        if self._registers[test_registry][ind] == False:
            return False
        lets = list(set(self._plain_text + self._cipher_text))
        stop = True
        for l in lets:
            if self._registers[l].count(True) != 1:
                stop = False
        return stop
    
    def _contradictions(self):
        menu_letters = list(set(self._plain_text + self._cipher_text))
        stecker_pairs = {}

        for s1 in menu_letters:
            registry = self._registers[s1]
            ind = registry.index(True)
            s2 = self.LETTERS[ind]
            if s1 in stecker_pairs.keys() and stecker_pairs[s1] != s2:
                return True
        return False

    def _get_stecker_pairs(self):
        menu_letters = list(set(self._plain_text + self._cipher_text))
        stecker_pairs = []

        for s1 in menu_letters:
            registry = self._registers[s1]
            ind = registry.index(True)
            s2 = self.LETTERS[ind]
            if [s1,s2] not in stecker_pairs or [s2,s1] not in stecker_pairs:
                stecker_pairs.append([s1,s2])
        return stecker_pairs

    def _is_alpha(self, text):
        for c in text:
            if c not in self.LETTERS:
                return False
        return True
    
    def _print_rotor_settings(self):
        rot_settings = self.rotor_settings_gen.settings
        rs = rot_settings["RS"]
        rm = rot_settings["RM"]
        rf = rot_settings["RF"]
        settings_str = f"RS {rs} RM {rm} RF {rf}"
        print(settings_str)

    def _print_registry(self, registry, test_letter):
        menu_letters = list(set(self._plain_text + self._cipher_text))
        reg_str = f"Test Registry {registry} Test Letter {test_letter}\n"
        for l in self.LETTERS:
            reg_str += l
            reg_str += " "
            reg = self._registers[l]
            for v in reg:
                if v:
                    reg_str += "1"
                else:
                    reg_str += "0"
            if l in menu_letters:
                reg_str += "-"
            reg_str += "\n"
        print(reg_str)

    def _test(self):
        """
        Perform test so only when all letters in one cable are live only one wire in every
        other cable is live.
        """
        self.cables = {l:[] for l in self.LETTERS}
        for l in self.LETTERS:
            self._trace_paths('A',l)
            self._print_registry(l,'A')
            self._reset_registers()