import argparse
from argparse import RawTextHelpFormatter
from enigma_cli.enigma_app_cli.enigma_app_cli import InteractiveEnigmaCli
from enigma_cli.enigma_cli.enigma_cli1 import CommandLineEnigmaCli
from enigma_cli.code_sheet_cli.code_sheet_cli import CodeSheetCli
from enigma_cli.statistics_cli.statistics_cli import StatisticsCli
from enigma_cli.indicators_cli.indicators_cli import IndicatorsCli
from enigma_cli.permutations_cli.permutations_solver_cli import PermutationsSolverCli
from enigma_cli.zygalski_sheets_cli.zygalski_sheet_cli import ZygalskiSheetCli


def enigma_cli(argv=None):

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    subparsers.add_parser(
        'interactive_enigma',
        help="interactive enigma")
    interactive_enigma_cli = InteractiveEnigmaCli()

    command_line_enigma = subparsers.add_parser(
        'enigma_simulator',
        help='cli enigma',
        formatter_class=RawTextHelpFormatter)
    command_line_enigma_cli = CommandLineEnigmaCli(command_line_enigma)

    code_sheet = subparsers.add_parser(
        'code_sheet',
        help='returns an enigma code sheet')
    code_sheet_cli = CodeSheetCli(code_sheet)

    statistics = subparsers.add_parser(
        'statistics',
        help='provides bigram trigram and index of coincidence values')
    statistics_cli = StatisticsCli(statistics)

    indicators = subparsers.add_parser(
        'indicators',
        help='generates and filters enigma indicators')
    indicators_cli = IndicatorsCli(indicators)

    permutations_solver = subparsers.add_parser(
        'permutations',
        help='solves for rotor permutations')
    permutations_solver_cli = PermutationsSolverCli(permutations_solver)

    zygalski_sheets = subparsers.add_parser(
        'zygalski_sheets',
        help='generates zygalski sheets')
    zygalski_sheets_cli = ZygalskiSheetCli(zygalski_sheets)

    args = parser.parse_args(argv)
    args = vars(args)

    if args['command'] == 'interactive_enigma':
        interactive_enigma_cli.process_args(args)

    elif args['command'] == 'enigma_simulator':
        command_line_enigma_cli.process_args(args)

    elif args['command'] == 'code_sheet':
        code_sheet_cli.process_args(args)

    elif args['command'] == 'statistics':
        statistics_cli.process_args(args)

    elif args['command'] == 'indicators':
        indicators_cli.process_args(args)

    elif args['command'] == 'permutations':
        permutations_solver_cli.process_args(args)

    elif args['command'] == 'zygalski_sheets':
        zygalski_sheets_cli.process_args(args)

    return 0
