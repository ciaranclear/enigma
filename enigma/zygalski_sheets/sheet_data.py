from enigma_tools.setting_tools.setting_tools import RotorSettings
from enigma_core.factory import make_machine
import json
import os


class SheetDataGenerator:

    LETTERS = [chr(i) for i in range(65, 91)]

    def __init__(self):
        """
        
        """
        self._machine_obj = make_machine("WEHRMACHT")

    def data(self, settings):
        """
        
        """
        cond = False
        dirpath = os.path.dirname(__file__)
        dirpath = os.path.join(dirpath, "wehrmacht")
        if os.path.isdir(dirpath) and cond:
            rs = settings["rotor_settings"]["RS"]
            ref = settings["reflector"]
            rot_rs = settings["rotor_types"]["RS"]
            rot_rm = settings["rotor_types"]["RM"]
            rot_rf = settings["rotor_types"]["RF"]
            dirname = f"{ref}_{rot_rs}_{rot_rm}_{rot_rf}"
            filename = f"{rs}_{ref}_{rot_rs}_{rot_rm}_{rot_rf}.json"
            dirpath = os.path.join(dirpath, dirname)
            filepath = os.path.join(dirpath, filename)

            with open(filepath, "r") as f:
                data = f.read()

            return data

        else:
            data = {"data":{}}
            self._machine_obj.settings = settings
            self._settings = self._machine_obj.settings
            self._machine_obj.scrambler.character_set_flag = 'L'
            rotor_settings = self._machine_obj.settings["rotor_settings"]
            rot_set_gen = RotorSettings(positions=2)

            while True:
                rot_set = rot_set_gen.settings
                setting_data = {"G1":[],"G2":[],"G3":[]}
                for letter in self.LETTERS:
                    inpt = letter*6
                    self._machine_obj.settings = {"rotor_settings":rotor_settings}
                    self._machine_obj.settings = {"rotor_settings":rot_set}
                    outp = ""
                    for l in inpt:
                        outp += self._machine_obj.character_input(l)
                    if outp[0] == outp[3]:
                        setting_data["G1"].append([l,outp[0]])
                    if outp[1] == outp[4]:
                        setting_data["G2"].append([l,outp[1]])
                    if outp[2] == outp[5]:
                        setting_data["G3"].append([l,outp[2]])
                data["data"][f"{rot_set['RM']}{rot_set['RF']}"] = setting_data

                try:
                    rot_set_gen.inc()
                except StopIteration:
                    break

            return data