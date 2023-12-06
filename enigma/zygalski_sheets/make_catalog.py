"""
FOLDER STRUCTURE FOR SHEETS
/WEHRMACHT
    /UKW-B_III_II_I
       wehrmacht_iii_ii_i_A.json
       wehrmacht_iii_ii_i_B.json

1. Create the file structure.
2. Generate the scrambler permutations.
3. For each permutation generate sheets for A-Z.
"""
import os
from enigma_core.factory import make_machine
from enigma_tools.setting_tools.setting_tools import scrambler_perms
from zygalski_sheets1.sheet_data import SheetDataGenerator
import multiprocessing
import json


LETTERS = [chr(i) for i in range(65, 91)]


def make_permutation_catalog(perm, dir):

    dname = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
    dpath = os.path.join(dir, dname)

    if not os.path.isdir(dpath):
        os.mkdir(dpath)

    for l in LETTERS:
        settings = {
            "reflector":perm.REF,
            "rotor_types":{"RS":perm.RS,"RM":perm.RM,"RF":perm.RF},
		    "rotor_settings":{"RS":l,"RM":"A","RF":"A"}
        }

        fname = f"{l}_{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}.json"
        fpath = os.path.join(dpath, fname)
        print(fname)
        if os.path.isfile(fpath):
            continue

        generator = SheetDataGenerator()
        data = generator.data(settings)
        data = json.dumps(data)

        with open(fpath, "w") as f:
            f.write(data)

def make_sheets():
    """
    
    """
    dir = os.path.dirname(__file__)
    dir = os.path.dirname(dir)

    dir = os.path.join(dir, "wehrmacht")

    if not os.path.isdir(dir):
        os.mkdir(dir)

    machine = make_machine("WEHRMACHT")

    collection = machine.scrambler.collection.collection_dict()
    rotors_static = collection["ROTORS_STATIC"]
    rotors_dynamic = collection["ROTORS_DYNAMIC"]
    reflectors = collection["REFLECTORS"]

    perms = scrambler_perms(reflectors, rotors_dynamic, rotors_static)

    processes = []

    for perm in perms:
        p = multiprocessing.Process(target=make_permutation_catalog, args=[perm, dir])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()