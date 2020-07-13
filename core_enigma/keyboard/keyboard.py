

class Keyboard(object):

    def __init__(self, keyboard_dict):

        self._keyboard_dict = keyboard_dict
        super(Keyboard, self).__init__()

    def keyboardInput(self, character):

        try:
            valid_character = self._keyboard_dict[character]
        except KeyError:
            return None
        else:
            return valid_character


if __name__ == "__main__":

    keyboard_dict = {
        'a':'A', 'b':'B', 'c':'C', 'd':'D', 'e':'E', 'f':'F', 'g':'G', 'h':'H',
        'i':'I', 'j':'J', 'k':'K', 'l':'L', 'm':'M', 'n':'N', 'o':'O', 'p':'P',
        'q':'Q', 'r':'R', 's':'S', 't':'T', 'u':'U', 'v':'V', 'w':'W', 'x':'X',
        'y':'Y', 'z':'Z', 'A':'A', 'B':'B', 'C':'C', 'D':'D', 'E':'E', 'F':'F',
        'G':'G', 'H':'H', 'I':'I', 'J':'J', 'K':'K', 'L':'L', 'M':'M', 'N':'N',
        'O':'O', 'P':'P', 'Q':'Q', 'R':'R', 'S':'S', 'T':'T', 'U':'U', 'V':'V',
        'W':'W', 'X':'X', 'Y':'Y', 'Z':'Z', '1':'Q', '2':'W', '3':'E', '4':'R',
        '5':'T', '6':'Z', '7':'U', '8':'I', '9':'O', '0':'P'
    }

    sentence = "my name is ciaran clear"
    valid_sentence = ""
    keyboard = Keyboard(keyboard_dict)

    for character in sentence:
        valid_character = keyboard.keyboard_input(character)
        if valid_character:
            valid_sentence += valid_character

    print(valid_sentence)