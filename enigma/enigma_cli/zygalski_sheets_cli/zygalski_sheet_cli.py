from enigma_cli.zygalski_sheets_cli.svg_sheet_cli import SvgSheetCli
from enigma_cli.zygalski_sheets_cli.text_sheet_cli import TextSheetCli


class ZygalskiSheetCli:

    def __init__(self, parser):
        self.parser = parser
        self._add_sub_parsers()

    def process_args(self, args):
        """
        
        """
        if args['sheets'] == 'svg_sheet':
            self.svg_sheet_cli.process_args(args)

        elif args['sheets'] == 'text_sheet':
            self.text_sheet_cli.process_args(args)

    def _add_sub_parsers(self):
        """
        
        """
        subparsers = self.parser.add_subparsers(dest='sheets')
        subparsers.required = True

        svg_sheet = subparsers.add_parser(
            "svg_sheet", 
            help="generates svg sheets")
        self.svg_sheet_cli = SvgSheetCli(svg_sheet)

        text_sheet = subparsers.add_parser(
            "text_sheet", 
            help="generates text sheets")
        self.text_sheet_cli = TextSheetCli(text_sheet)
