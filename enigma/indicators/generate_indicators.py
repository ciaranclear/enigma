from enigma_core.factory import make_machine
import random


def generate_indicators(settings, number):
    """

    """
    LETTERS = [chr(i) for i in range(65, 91)]

    machine = make_machine("WEHRMACHT", settings)

    settings["character_set_flag"] = 'L'
    settings["plugboard_mode"] = 'S'

    indicators = []

    for n in range(number):

        machine.settings = settings

        indicator = ""
        
        letters = LETTERS.copy()
        random.shuffle(letters)

        for i in range(3):
            indicator += random.choice(letters)

        indicator = indicator*2

        output = ""

        for c in indicator:
            output += machine.character_input(c)

        indicators.append(output)

    return indicators
