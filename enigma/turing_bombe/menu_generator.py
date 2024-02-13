from pprint import pprint
from collections import deque


class FindLoops:

    def __init__(self, plain_text, cipher_text):
        self.plain_text = plain_text
        self.cipher_text = cipher_text

    def valid_crib(self):
        letters = [chr(i) for i in range(65,91)]

        self.plain_text = self.plain_text.upper()
        self.cipher_text = self.cipher_text.upper()

        if len(plain_text) != len(cipher_text):
            err_msg = (f"Plain text is length {len(plain_text)} and the cipher text is length {len(cipher_text)}\n. "
                       f"Plain text and cipher text Must be the same length.")
            raise Exception(err_msg)

        for l in plain_text:
            if l not in letters:
                err_msg = f""
                raise Exception(err_msg)

        for i in cipher_text:
            if l not in letters:
                err_msg = f""
                raise Exception(err_msg)

        for i in range(len(plain_text)):
            if plain_text[i] == cipher_text[i]:
                err_msg = (f"Plain text and cipher text has the same letter {plain_text[i]} at index {i}. "
                           f"A letter at an index in the plain text must be different "
                           f"from the letter in the cipher text at the same index.")
                raise Exception(err_msg)
            
    def _find_loops(self):
        pass

    def _filter_unique_loops(self):
        pass

    @staticmethod
    def _can_append_letter(path, c1, c2):
        if c1 != path[-1] and c2 != path[-1]:
            return False
        if path == [c1,c2] or path == [c2,c1]:
            return False
        if (c1 == path[-1] and c2 in path) or (c1 == path[-1] and c1 in path):
            return False
        return True
    
    @staticmethod
    def _can_append_path(path, c1, c2):
        if ((c1 == path[0] and c2 == path[-1]) or (c2 == path[0] and c1 == path[-1])) and len(path) != 2:
            return True
        else:
            return False
        
    @staticmethod
    def no_common_letters(path, c1, c2):
        if c1 not in path and c2 not in path:
            return True
        else:
            return False

if __name__ == "__main__":
    #plain_text = "WEATHERFORECASTBISCAY"
    #cipher_text = "YHXBDYCWCJAQPBLMHMBGP"
    #plain_text = "THERFORECASTBISCAY"
    #cipher_text = "BDYCWCJAQPBLMHMBGP"
    #plain_text = "WEATHERFORECASTBISCAY"
    #cipher_text = "YHXBDYCWCJAQPBLMHMBGP"

    plain_text = "TOTHEPRESIDENTOFTHEUNITEDSTATES"
    cipher_text = "CQNZPYLILPEUIKTEDCGLOVWVGTUFLNZ"

