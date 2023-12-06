from enigma_core.validators.scrambler_validators import *
from zygalski_sheets.svg_sheet import SVGZygalskiSheet
from zygalski_sheets.sheet_data import SheetDataGenerator


class SvgSheetCli:

    def __init__(self, parser):
        self.parser = parser
        self._add_arguments()

    def process_args(self, args):
        """
        
        """
        perm_str = args["permutation"]

        try:
            perm_str, perm_dict = ScramblerValidators.valid_permutation(perm_str, group_flag=False)
        except PermutationError as e:
            raise e
        else:
            settings = {
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
                "ring_settings":{"RS":"A","RM":"A","RF":"A"}
            }
            sheet_data_generator = SheetDataGenerator()
            sheet_data = sheet_data_generator.data(settings)
            svg_sheet_generator = SVGZygalskiSheet()
            for group in ["G1","G2","G3"]:
                sheet_id = f"{perm_str}_{group}"
                svg_sheet = svg_sheet_generator.render_sheet(sheet_data, sheet_id, group)
                with open(f"{perm_str}_{group}.svg", "w") as f:
                    f.write(svg_sheet)

    def _add_arguments(self):
        """
        
        """
        self.parser.add_argument(
            "permutation", 
            help=f"provide a permutation in form 'A_UKW-B_III_II_I'. "
            f"returns svg zygalski sheets.")