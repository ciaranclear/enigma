from enigma_app.enigma_app import enigma_app
import argparse
from argparse import RawTextHelpFormatter


class InteractiveEnigmaCli:

    def __init__(self):
        pass

    def process_args(self, args):
        enigma_app()
