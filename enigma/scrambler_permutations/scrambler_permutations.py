from indicators.filter_females import filter_females
from enigma_core.scrambler.collection.collection import Collection
from enigma_tools.setting_tools.setting_tools import scrambler_perms, RotorSettings
import json
import os


class ScramblerPermutations:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self, indicators):
        """

        """
        self.indicators = indicators
        self.catalog_dir = None
        self.permutations = None
        self.females = None
        self.groups = None
        self.filtered_perms = []
        self._get_catalog()
        self._filter_females()
        self._make_groups()
        self._make_permutations()

    def filter_permutations(self, v=False):
        """

        """
        for perm in self.permutations:
            if v:
                print(
                    f"REF {perm.REF.ljust(4, ' ')} "
                    f"RS {perm.RS.ljust(3, ' ')} "
                    f"RM {perm.RM.ljust(3, ' ')} "
                    f"RF {perm.RF.ljust(3, ' ')}")
            self._filter_permutation(perm)

        return self.filtered_perms

    def _filter_females(self):
        """

        """
        self.females = filter_females(self.indicators)

    def _make_groups(self):
        """

        """
        groups = {
            "G1":[],
            "G2":[],
            "G3":[]
        }

        for female in self.females:
            if female[0] == female[3]:
                if female[0] not in groups["G1"]:
                    groups["G1"].append(female[0])
            if female[1] == female[4]:
                if female[1] not in groups["G2"]:
                    groups["G2"].append(female[1])
            if female[2] == female[5]:
                if female[2] not in groups["G3"]:
                    groups["G3"].append(female[2])

        self.groups = groups

    def _get_catalog(self):
        """

        """
        dir = os.path.dirname(__file__)
        dir = os.path.dirname(dir)

        self.catalog_dir = os.path.join(dir, "wehrmacht")

    def _make_permutations(self):
        """

        """
        reflectors = Collection.device_list("WEHRMACHT", ["REF"])
        rotors_dynamic = Collection.device_list("WEHRMACHT", ["R_ROT"])

        self.permutations = scrambler_perms(reflectors, rotors_dynamic)

    def _filter_permutation(self, perm):
        """

        """
        catalog_dirname = "wehrmacht"
        dirpath = os.path.dirname(__file__)
        catalog_dirpath = os.path.join(dirpath, catalog_dirname)
        perm_dirname = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
        perm_dirpath = os.path.join(catalog_dirpath, perm_dirname)
        for l in self.LETTERS:
            perm_filename = f"{l}_{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}.json"
            perm_filepath = os.path.join(perm_dirpath, perm_filename)

            with open(perm_filepath, "r") as f:
                sheet = json.loads(f.read())
                self._filter_sheet(sheet, perm, l)

    def _filter_sheet(self, sheet, perm, l):
        """

        """
        data = sheet["data"]
        rotor_settings = RotorSettings('L', 2)
        while True:
            settings = rotor_settings.settings

            setting_data = data[f"{settings['RM']}{settings['RF']}"]

            setting_groups = {
                "G1":[],
                "G2":[],
                "G3":[]
            }

            for groupname in ["G1","G2","G3"]:
                for list in setting_data[groupname]:
                    for c in list:
                        if c not in setting_groups[groupname]:
                            setting_groups[groupname].append(c)

            valid = True

            for groupname in ["G1","G2","G3"]:
                for c in self.groups[groupname]:
                    if c not in setting_groups[groupname]:
                        valid = False

            if valid:
                settings["RS"] = l
                p = {
                    "reflector":perm.REF,
                    "rotor_types":{
                        "RS":perm.RS,
                        "RM":perm.RM,
                        "RF":perm.RF
                    },
                    "rotor_settings":settings
                }
                self.filtered_perms.append(p)

            try:
                rotor_settings.inc()
            except StopIteration:
                break
