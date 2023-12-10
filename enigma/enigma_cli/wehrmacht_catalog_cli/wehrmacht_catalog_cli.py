from scrambler_permutations.make_catalog import make_sheets
import shutil
import os


class WehrmachtCatalogCli:

    def __init__(self, parser):
        self.parser = parser
        self.dir = os.path.join("scrambler_permutations","wehrmacht")
        self._add_arguments()

    def process_args(self, args):
        if args['c'] == True:
            if os.path.isdir(self.dir):
                print("catlog exists.")
            else:
                print("catalog does not exist.")
        elif args['m'] == True:
            if os.path.isdir(self.dir):
                print("catlog already exists.")
            else:
                print("catalog does not exist. creating catalog now.")
                make_sheets()
                print("catalog has been successfully created.")
        elif args['f'] == True:
            if os.path.exists(self.dir):
                msg = (f"wehrmacht catalog already exists. "
                      f"are you sure you want to force remake. y/n. ")
                inpt = input(msg)
                if inpt.upper() == "Y":
                    shutil.rmtree(self.dir)
                    make_sheets()
                    print("catalog has been successfully created.")
                else:
                    print("aborted wehrmacht catalog remake.")
            else:
                make_sheets()

    def _add_arguments(self):
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument('-c', action='store_true', help='check if the catalog exists')
        group.add_argument('-m', action='store_true', help='make wehrmacht catalog')
        group.add_argument('-f', action='store_true', help='force remake of the wehrmacht catalog')
        group.required = True
