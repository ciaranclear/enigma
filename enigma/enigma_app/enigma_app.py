from enigma_core.factory import machine_list, make_machine
from enigma_app.enigma_interface.enigma_interface import EnigmaInterface


def make_enigma(machine):
    """

    """
    machines = machine_list()

    if machine not in machine_list():
        msg = (f"{machine} is not a valid enigma machine. "
               f"Must be one of the following {machines}.")
        raise ValueError(msg)
    else:
        enigma_obj = make_machine(machine)
        enigma_app = EnigmaInterface(enigma_obj)
        enigma_app.menu()

def enigma_app():
    """

    """
    machines = machine_list()

    menu_str = (
        f"Enter a number to select a machine."
    )

    while True:

        print(menu_str)

        for index, machine in enumerate(machines, start=1):
            print(f"{index}. {machine}.")

        print(f"{len(machines)+1}. Quit.")

        try:
            inpt = int(input())
        except ValueError:
            pass
        else:
            if 1 <= inpt <= len(machines):
                machine = machines[inpt-1]
                make_enigma(machine)
            elif inpt == len(machines)+1:
                break
            else:
                print("Invalid input!. Try again.")
