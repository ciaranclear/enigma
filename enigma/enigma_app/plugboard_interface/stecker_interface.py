from enigma_app.formating.formating import EnigmaFormatter as ef
from enigma_core.settings.settings import LETTERS, NUMBERS
import re


class SteckerPlugboardInterface:

    def __init__(self, plugboard_obj):
        """
        
        """
        self._plugboard_obj = plugboard_obj

    def __str__(self):
        """
        
        """
        return ef.center(self._plugboard_obj.__str__())

    def menu(self):
        """
        
        """
        
        while True:
            menu_str = (
                f"{ef.line('STECKER PLUGBOARD')}\n"
                f"\n{self.__str__()}\n\n"
                f"Enter a number to select an option\n"
                f"1. Clear plugboard\n"
                f"2. Connect stecker cables\n"
                f"3. Quit\n"
                f"{ef.line()}\n"
            )

            inpt = input(menu_str)
            if inpt == "1": self._clear_plugboard()
            elif inpt == "2": self._connect_stecker_cables()
            elif inpt == "3": return
            else: print("Invalid input! Try agin")

    def character_set_flag(self, flag):
        """
        
        """
        self._plugboard_obj.character_set_flag = flag

    def _clear_plugboard(self):
        """
        
        """
        menu_str = f"Are you sure you want to clear the plugboard Y/N. "

        inpt = input(menu_str)

        if inpt.upper() == 'Y':
            self._plugboard_obj.clear()
            print("The plugboard has been cleared.")

    def _connect_stecker_cables(self) -> None:
        """

        """
        if self._plugboard_obj.character_set_flag == 'L':
            self._letter_plugboard()
        elif self._plugboard_obj.character_set_flag == 'N':
            self._number_plugboard()

    def _letter_plugboard(self):
        """
        
        """
        def get_connections_str():
            """

            """
            menu_str = (
                f"Enter up to 13 space seperated plugboard pairs.\n"
                f"01 02 03 04 05 06 07 08 09 10 11 12 13\n"
            )

            inpt = input(menu_str)

            return inpt
        
        def parse_socket_id_pairs(socket_id_str):
            """
            Parse the socket id strings to get the socket id pairs.
            """
            regex = re.compile("[a-zA-Z]{2}")

            matches = re.findall(regex, socket_id_str)

            return list(matches)
        
        def valid_socket_ids(conns):
            """
            Check each socket id is valid.
            """
            conns = [conn.upper() for conn in conns]
            
            for conn in conns:
                invalid = [c for c in conn if c not in LETTERS]
                if invalid:
                    msg = f"Invalid socket id(s) {','.join(invalid)}."
                    raise ValueError(msg)
                
            return conns
        
        def no_repeats(conns):
            """
            Checks that there are no repeated socket ids.
            """
            all = ''.join(conns)

            repeats = [c for c in all if all.count(c) > 1]
            repeats = list(set(repeats))

            if repeats:
                msg = (f"Repeated socket id(s) {','.join(repeats)}.\n"
                       f"All socket ids must be unique.")
                raise ValueError(msg)

            return conns
        
        while True:        
            conns_str = get_connections_str()
            conns = parse_socket_id_pairs(conns_str)

            try:
                conns = valid_socket_ids(conns)
            except ValueError as e:
                print(e.__str__())
                continue

            try:
                conns = no_repeats(conns)
            except ValueError as e:
                print(e.__str__())
                continue

            self._plugboard_obj.make_connections(conns)
            break

    def _number_plugboard(self):
        """
        
        """
        def get_connections_str():
            """
            Prompt user to input socket id pairs to connect. Returns the socket
            id string.            
            """
            menu_str = (
                f"Enter up to 13 space seperated plug pairs. \n"
                f"The socket ids in each plug pair being seperated by '-'.\n"
                f"-001- -002- -003- -004- -005- -006- -007- -008- -009- -010- -011- -012- -013-\n")
            inpt = input(menu_str)

            return inpt

        def parse_socket_id_pairs(socket_id_str):
            """
            Parse the socket id strings to get the socket id pairs.
            """
            regex = re.compile("(\d\d)-(\d\d)")

            matches = re.findall(regex, socket_id_str)

            return list(matches)
            
        def valid_socket_ids(conns):
            """
            Check each socket id is valid.
            """
            for conn in conns:
                invalid = [c for c in conn if c not in NUMBERS]
                if invalid:
                    msg = f"Invalid socket id(s) {','.join(invalid)}."
                    raise ValueError(msg)
                
            return conns
        
        def no_repeats(conns):
            """
            Checks that there are no repeated socket ids.
            """
            socket_ids = []

            for conn in conns:
                socket_ids.append(conn[0])
                socket_ids.append(conn[1])

            repeats = [c for c in socket_ids if socket_ids.count(c) > 1]
            repeats = list(set(repeats))

            if repeats:
                msg = (f"Repeated socket id(s) {','.join(repeats)}.\n"
                       f"All socket ids must be unique.")
                raise ValueError(msg)
            
            return conns

        while True:        
            conns_str = get_connections_str()
            conns = parse_socket_id_pairs(conns_str)

            try:
                conns = valid_socket_ids(conns)
            except ValueError as e:
                print(e.__str__())
                continue

            try:
                conns = no_repeats(conns)
            except ValueError as e:
                print(e.__str__())
                continue

            self._plugboard_obj.make_connections(conns)
            break