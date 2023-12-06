from enigma_core.validators.scrambler_validators import *
from zygalski_sheets.text_sheet import TextZygalskiSheet
from zygalski_sheets.sheet_data import SheetDataGenerator
import re


class TextSheetCli:

    def __init__(self, parser):
        self.parser = parser
        self._add_arguments()

    def process_args(self, args):
        """
        
        """
        print(args)
        perm_str = args["permutation"]

        try:
            perm_str, perm_dict = ScramblerValidators.valid_permutation(perm_str, group_flag=False)
        except PermutationError as e:
            raise e
        else:
            settings = {
                "machine_type":"WEHRMACHT",
                "reflector":perm_dict["REF"],
                "rotor_types":{
                    "RS":perm_dict["ROT_RS"],
                    "RM":perm_dict["ROT_RM"],
                    "RF":perm_dict["ROT_RF"]
                },
                "rotor_settings":{
                    "RS":perm_dict["RS"],
                    "RM":"A",
                    "RF":"A"
                },
                "ring_settings":{"RS":"A","RM":"A","RF":"A"},
                "plugboard_char_set_flag":"L",
                "plugboard_connections":[]
            }
            sheet_data_generator = SheetDataGenerator()
            sheet_data = sheet_data_generator.data(settings)

            text_sheet_generator = TextZygalskiSheet(settings, sheet_data)
            groups = args["groups"]

            p = re.compile("[123]")
            groups = re.findall(p, groups)
            groups = [int(i) for i in groups]
            charset = None
            if args["l"] == True:
                charset = "L"
            elif args["n"]:
                charset = "N"
            text_sheet = text_sheet_generator.text_sheet(groups, "N", charset, sheet_data, True)
            print(text_sheet)

    def _add_arguments(self):
        """
        
        """
        self.parser.add_argument(
            "permutation", 
            help=f"provide a permutation in form 'A_UKW-B_III_II_I'. "
            f"returns a text zygalski sheet.")
        self.parser.add_argument(
            "--groups",
            help=f"enter the groups of females you want '1,2,3'. "
            f"defaults to all groups."
        )

        group = self.parser.add_mutually_exclusive_group()
        group.add_argument("-l", action="store_true", help="alpha output")
        group.add_argument("-n", action="store_true", help="numeric output")
        group.required = True
