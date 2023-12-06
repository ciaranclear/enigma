from enigma_app.formating.formating import EnigmaFormatter as ef
from enigma_core.settings.settings import LETTERS, NUMBERS
from enigma_core.plugboard.uhr_box import UhrBox

class UhrBoxPlugboardInterface:

    def __init__(self, plugboard_obj):
        """
        Takes an uhr box plugboard object to provide an interface for.        
        """
        self._plugboard_obj = plugboard_obj

    def __str__(self):
        """
        Returns the string repressentation of the uhr box plugboard.
        """
        return ef.center(self._plugboard_obj.__str__())


    def menu(self):
        """
        Provides the uhr box plugboard menu.
        """
        
        while True:
            menu_str = (
                f"{ef.line('UHR BOX PLUGBOARD')}\n"
                f"\n{self.__str__()}\n"
                f"Enter a number to select an option\n"
                f"1. Clear plugboard\n"
                f"2. Connect uhr box plugs\n"
                f"3. Set uhr box setting\n"
                f"4. Quit\n"
                f"{ef.line()}\n"
            )

            inpt = input(menu_str)
            if inpt == "1": self._clear_plugboard()
            elif inpt == "2": self._connect_uhr_box_plugs()
            elif inpt == "3": self._set_uhr_box_setting()
            elif inpt == "4": return
            else: print("Invalid input! Try agin")

    def character_set_flag(self, flag):
        """
        Sets the plugboard character set to the character set flag provided.
        """
        self._plugboard_obj.character_set_flag = flag

    def _clear_plugboard(self):
        """
        Prompts the user to enter Y/N to confirm if the user wants to clear the
        plugboard. 
        """
        menu_str = f"Are you sure you want to clear the plugboard Y/N. "

        inpt = input(menu_str)

        if inpt.upper() == 'Y':
            self._plugboard_obj.clear()
            print("The plugboard has been cleared.")

    def _connect_uhr_box_plugs(self):
        """
        Prompts the user to input socket ids to connect the uhr box plugs to.
        """

        def get_socket_str(group):
            """
            Takes a uhr box group id. Prompts the user to input socket ids for
            the uhr box plugs in that group.
            """
            if group not in ['A','B']:
                raise ValueError(f"{group} is not a valid group. Must be 'A' or 'B'")
            
            if group == 'A':
                plugs_list = UhrBox.PLUG_A_IDS
            elif group == 'B':
                plugs_list = UhrBox.PLUG_B_IDS

            plug_str = ' '.join(plugs_list)

            msg = (
                f"Enter 10 space seperated socket ids to connect uhr plugs 01{group}-10{group}.\n"
                f"Use rule provided to assign a socket id to an uhr box plug.\n"
                f"{plug_str}\n"
            )

            inpt = input(msg)

            return inpt
        
        def parse_socket_ids(socket_str, group):
            """
            Takes the string containing socket ids. Parses the string for
            10 socket ids. If 10 socket ids not pressent raises a ValueError.
            """
            socket_ids = socket_str.split(' ')
            
            socket_ids = [c for c in socket_ids if c != '']

            if len(socket_ids) != 10:
                msg = (f"Invalid socket ids for group {group} plugs.\n"
                       f"10 socket ids must be provides.\n"
                       f"{len(socket_ids)} socket ids provided.")
                raise ValueError(msg)
            
            return socket_ids
        
        def valid_socket_ids(socket_ids, char_set, group):
            """
            Takes a list of socket ids, plugboard character set and the uhr box
            group id. Checks that all socket ids are in the plugboard character
            set. Checks that no socket id is repeated. If the socket id list is
            not valid a ValueError is raised.
            """
            socket_ids = [c.upper() for c in socket_ids]

            invalid = [c for c in socket_ids if c not in char_set]

            if invalid:
                msg = (f"Invalid socket id(s) for group {group} plugs. "
                       f"{','.join(invalid)}. Must be A-Z.")
                raise ValueError(msg)
            
            repeats = [c for c in socket_ids if socket_ids.count(c) > 1]
            repeats = list(set(repeats))

            if repeats:
                msg = (f"Repeated socket id(s) for group {group} plugs.\n"
                       f"'{','.join(repeats)}' socket id(s) are repeated.\n"
                       f"All socket ids must be unique.")
                raise ValueError(msg)
            
            return socket_ids

        def get_socket_ids(group, char_set):
            """
            Takes an uhr box plug group id and plugboard character set. Returns
            a valid socket id list.
            """
            while True:
                socket_str = get_socket_str(group)

                try:
                    socket_ids = parse_socket_ids(socket_str, group)
                except ValueError as e:
                    print(e.__str__())
                    continue

                try:
                    socket_ids = valid_socket_ids(socket_ids, char_set, group)
                except ValueError as e:
                    print(e.__str__())
                else:
                    return socket_ids
        
        def unique_socket_ids(sockets_a, sockets_b):
            """
            Takes two socket id lists and checks that there are no repeated
            characters between the two lists.
            """
            all_sockets = sockets_a + sockets_b
            repeats = [c for c in all_sockets if all_sockets.count(c) > 1]
            repeats = list(set(repeats))

            if repeats:
                msg = f"Invalid socket ids!. Repeated socket id(s) {','.join(repeats)}."
                raise ValueError(msg)
            
        def make_connection_dict(socket_a_ids, socket_b_ids):
            """
            Takes two socket id lists and returns a dictionary with key value
            pairs of uhr box plug id to socket id.
            """
            all_socket_ids = socket_a_ids + socket_b_ids
            all_plug_ids = UhrBox.PLUG_A_IDS + UhrBox.PLUG_B_IDS
            conns = zip(all_plug_ids, all_socket_ids)

            conns_dict = {conn[0]:conn[1] for conn in conns}

            return conns_dict
            
        char_flag = self._plugboard_obj.character_set_flag
        char_set = LETTERS if char_flag == 'L' else NUMBERS

        while True:
            socket_a_ids = get_socket_ids('A', char_set)
            socket_b_ids = get_socket_ids('B', char_set)

            try:
                unique_socket_ids(socket_a_ids, socket_b_ids)
            except ValueError as e:
                print(e.__str__())
                continue

            conns = make_connection_dict(socket_a_ids, socket_b_ids)

            self._plugboard_obj.make_connections(conns)
            break

    def _set_uhr_box_setting(self):
        """
        Prompts the user to input a rotor setting for the uhr box.        
        """
        menu_str = f"Enter an uhr box rotor setting in the range 0-39. "

        while True:
            try:
                inpt = int(input(menu_str))
            except ValueError:
                print("Invalid input!. Try again.")
            else:
                if 0 <= inpt <= 39:
                    self._plugboard_obj.rotor_setting = inpt
                    break
                else:
                    print("Invalid input!. Try again.")

