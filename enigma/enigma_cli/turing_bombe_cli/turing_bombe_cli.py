"""
ARGUMENTS TO PROVIDE.

1. Plain Text.
2. Cipher Text.
3. Permutation.
"""
from turing_bombe.turing_bombe import TuringBombe
import argparse
import json
import re
import os


class TuringBombeCli:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2, '0') for i in range(26)]

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        print(args)
        plain_text = args["plain_text"]
        cipher_text = args["cipher_text"]
        perm_file_path = args["permutations"]
        test_register = args['test_register']

        with open(perm_file_path, "r") as f:
            perms = f.readlines()

        perms = [line.strip() for line in perms]

        for p in perms:
            turing_bombe = TuringBombe(plain_text, cipher_text, p, test_register)
            turing_bombe.solve()

    def _add_parser_arguments(self):
        """
        
        """
        self._parser.add_argument('plain_text', type=str, help='The assumed plain text')
        self._parser.add_argument('cipher_text', type=str, help='The cipher text')
        self._parser.add_argument('permutations', type=str, help='The scrambler permutation file')
        self._parser.add_argument('test_register', type=str, help='The test register should be a loop character A-Z')