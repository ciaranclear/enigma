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


EXAMINING A STOP

1. Trace entire path on wire 'A'. If 1 or 25 wires live in every applicable register
   Isolate the 1 wire in each applicable register and check for contradictions. If
   no contradictions record stop.
"""

from enigma_core.factory import make_machine
from enigma_core.validators.scrambler_validators import ScramblerValidators, PermutationError
from enigma_tools.setting_tools.setting_tools import RotorSettings
from pprint import pprint


class TuringBombe:

    LETTERS = [chr(i) for i in range(65, 91)]

    def __init__(self, plain_text, cipher_text, permutation, test_register):
        self._plain_text = plain_text
        self._cipher_text = cipher_text
        self._permutation = permutation
        self._test_register = test_register
        self._diagonal_board = False
        self._cables = {}
        self._registers = {l:[False for i in range(26)] for l in self.LETTERS}
        self._stops = []
        self._menu_chars = None
        self._bombe_str = None
        self._machine = make_machine("WEHRMACHT")
        self._rotor_settings_gen = RotorSettings('L', 3)
        self._perm = self._valid_permutation()
        self._menu_characters()
        self._initialize_machine()
        self._valid_crib()

    def __str__(self):
        """
        
        """
        return self._bombe_str

    def solve(self):
        """
        
        """
        while True:
            self._set_machine()
            self._wire_bombe()
            self._check_stop()
            print(self._bombe_settings_str())

            try:
                self._rotor_settings_gen.inc()
            except StopIteration:
                break
        
        print(self._stops)
        print(len(self._stops))
        return self._stops

    def _valid_crib(self):
        """
        
        """
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

    def _menu_characters(self):
        """
        
        """
        text = self._plain_text + self._cipher_text
        self._menu_chars = list(set(text))
        self._menu_chars.sort()

    def _valid_permutation(self):
        """
        
        """
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
            err_msg = f"Permutation {self._permutation} is not a valid permutation."
            raise PermutationError(err_msg)

    def _initialize_bombe(self):
        """
        
        """
        self._initialize_machine()
        self._wire_bombe()

    def _initialize_machine(self):
        """
        
        """
        perm_dict = self._perm[1]
        settings = {
            "reflector":perm_dict["REF"],
            "rotor_types":{
                "RS":perm_dict["ROT_RS"],
                "RM":perm_dict["ROT_RM"],
                "RF":perm_dict["ROT_RF"]
            },
            "ring_settings":{"RS":"A","RM":"A","RS":"A"},
            "turnover_flag":False
        }
        self._machine.settings = settings
        self._set_machine()

    def _set_machine(self):
        """
        
        """
        rot_settings = self._rotor_settings_gen.settings
        settings = {
            "rotor_settings":{
                "RS":rot_settings["RS"],
                "RM":rot_settings["RM"],
                "RF":rot_settings["RF"]
            }
        }
        self._machine.settings = settings

    def _wire_bombe(self):
        """
        
        """
        self._bombe_str = f"{self._permutation}\n"
        self._cables = {l:[] for l in self.LETTERS}
        for i in range(len(self._plain_text)):
            c1 = self._plain_text[i]
            c2 = self._cipher_text[i]
            self._machine.character_input('A')

            c1_dict = {}
            c2_dict = {}

            for cin in self.LETTERS:
                cout = self._machine.non_keyed_input(cin)
                c1_dict[cin] = f"{c2}{cout}"
                c2_dict[cout] = f"{c1}{cin}"

            self._cables[c1].append(c1_dict)
            self._cables[c2].append(c2_dict)

            self._bombe_str += f"{c1}{c2} {self._machine_settings_str()}\n"

    def _trace_paths(self, cable, wire):
        """
        
        """
        wires = []
        self._trace_path(cable, wire, wires)

    def _trace_path(self, cable, wire, wires):
        """
        
        """
        # record ire_id in wires list
        wires.append(f"{cable}{wire}")
        # set wire in cable register to True
        self._registers[cable][self.LETTERS.index(wire)] = True
        # if applicable trace path on diagonal board wire
        if (cable != wire) and wire in self._menu_chars and f"{wire}{cable}" not in wires and self._diagonal_board:
            self._trace_path(wire, cable, wires)
        # trace path on any connected scramblers
        for scrambler in self._cables[cable]:
            wire_id = scrambler[wire]
            connected_cable = wire_id[0]
            connected_wire = wire_id[1]
            if wire_id not in wires:
                self._trace_path(connected_cable, connected_wire, wires)

    def _check_stop(self):
        """
        
        """
        # check one letter in test_register. if 26 wires live return False.
        # check for 1 or 25 live wires do. if 1 or 25 wires do more extensive check.
        # check for contradictions. if no contradictions return True else False.
        self._reset_registers()
        self._trace_paths(self._test_register, 'A')
        if (self._registers[self._test_register].count(True) == 26):
            return False
        else:
            # check for 1 or 25 wires
            for l in self.LETTERS:
                self._reset_registers()
                self._trace_paths(self._test_register, l)
                self._log_stop(l)
                if (self._registers[self._test_register].count(True) == 25):
                    # make 1 wire in each registry live and look for contradictions.
                    self._invert_registers()
                    if self._valid_registers() and self._no_contradictions():
                        self._document_stop(l)
                        self._record_stop()
                        break
                elif (self._registers[self._test_register].count(True) == 1):
                    if self._valid_registers() and self._no_contradictions():
                        self._document_stop(l)
                        self._record_stop()
                        break                    
                
    def _valid_registers(self):
        """
        
        """
        for c in self._menu_chars:
            if self._registers[c].count(True) not in [0,1]:
                return False
        return True

    def _invert_registers(self):
        """
        
        """
        for c in self._menu_chars:
            register = self._registers[c]
            for i in range(len(register)):
                if register[i] == True:
                    register[i] = False
                elif register[i] == False:
                    register[i] = True
    
    def _reset_registers(self):
        """
        
        """
        self._registers = {l:[False for i in range(26)] for l in self.LETTERS}

    def _no_contradictions(self):
        """
        
        """
        pairs = {}

        for c1 in self._menu_chars:
            try:
                ind = self._registers[c1].index(True)
            except ValueError:
                continue
            else:
                c2 = self.LETTERS[ind]
                """
                if (c1 in pairs.keys() and c2 not in pairs.keys()) or \
                   (c2 in pairs.keys() and c1 not in pairs.keys()):
                    return False
                """
                if (c1 in pairs.keys() and c2 != pairs[c1]) or (c2 in pairs.keys() and c1 != pairs[c2]):
                    return False
                else:
                    pairs[c1] = c2
                    pairs[c2] = c1
        return True

    def _stecker_pairs(self):
        """
        
        """
        stecker_pairs = []

        for c1 in self._menu_chars:
            try:
                ind = self._registers[c1].index(True)
            except ValueError:
                continue
            else:
                c2 = self.LETTERS[ind]
                pair = [c1,c2]
                pair.sort()
                stecker_pairs.append(pair)

        stecker_pairs = [tuple(pair) for pair in set(tuple(pair) for pair in stecker_pairs)]
        stecker_pairs = sorted(stecker_pairs, key=lambda x: x[0])

        return stecker_pairs
    
    def _record_stop(self):
        """
        
        """
        stop = {
            "settings":self._rotor_settings_gen.settings,
            "stecker_pairs":self._stecker_pairs()
        }
        self._stops.append(stop)
    
    def _wiring_str(self):
        """
        
        """
        wiring_str = ""

        for c1 in self._menu_chars:
            scramblers = self._cables[c1]
            for scrambler in scramblers:
                c2 = list(scrambler.values())[0][1]
                wiring_str += f"{c1}{c2}\n"
                c1_str = ""
                c2_str = ""
                for l in self.LETTERS:
                    c1_str += l
                    c2_str += scrambler[l][1]
                wiring_str += f"{c1_str}\n"
                wiring_str += f"{c2_str}\n"
        return wiring_str

    def _registers_str(self, c):
        """
        
        """
        reg_str = (f"Test Register {self._test_register}: Test Wire {c}\n"
                   f"  {self._menu_str()}\n"
                   f"  {''.join(self.LETTERS)}\n")

        for l in self.LETTERS:
            reg_str += f"{self._register_str(l)}\n"
        return reg_str

    def _register_str(self, l):
        """
        
        """
        reg_str = f"{l} "

        register = self._registers[l]
        for b in register:
            if b:
                reg_str += '|'
            elif not b:
                reg_str += '-'
        if l in self._menu_chars:
            reg_str += '='
        return reg_str

    def _machine_settings_str(self):
        """
        
        """
        settings = self._machine.settings
        rot_set = settings["rotor_settings"]
        rs = rot_set["RS"]
        rm = rot_set["RM"]
        rf = rot_set["RF"]
        return f"{rs}{rm}{rf}"
    
    def _bombe_settings_str(self):
        """
        
        """
        settings = self._rotor_settings_gen.settings
        rs = settings["RS"]
        rm = settings["RM"]
        rf = settings["RF"]
        return f"{rs}{rm}{rf}"
    
    def _menu_str(self):
        """
        
        """
        menu_str = ""

        for l in self.LETTERS:
            if l not in self._menu_chars:
                menu_str += '_'
            else:
                menu_str += l
        return menu_str

    def _document_stop(self, l):
        """
        
        """
        stop_setting = self._bombe_settings_str()

        stop_str = (f"PERM: {self._permutation}\n"
                    f"STOP: {stop_setting}\n"
                    f"{self._registers_str(l)}\n")
        with open("stops.log","a") as f:
            f.write(stop_str)

    def _log_stop(self, l):
        """
        
        """
        stops = [
            "AAA",
            "AAB",
            "AAC",
            "AAV"
        ]

        stop_setting = self._bombe_settings_str()

        for stop in stops:
            if stop == stop_setting:
                self._document_stop(l)
