from enigma_app.formating.formating import EnigmaFormatter as ef
from enigma_app.scrambler_interface.scrambler_interface import ScramblerInterface
from enigma_app.plugboard_interface.stecker_interface import SteckerPlugboardInterface
from enigma_app.plugboard_interface.uhr_box_interface import UhrBoxPlugboardInterface
from enigma_core.plugboard.stecker_plugboard import SteckerPlugboard
from enigma_core.plugboard.uhr_box_plugboard import UhrBoxPlugboard
from enigma_core.scrambler.collection.collection import Collection
from enigma_tools.histogram.histogram import Histogram
from code_sheet.code_sheet_generator import CodeSheetGenerator
from enigma_app.telex.telex import Telex


class EnigmaInterface:

    def __init__(self, enigma_obj):
        """

        """
        self._enigma_obj = enigma_obj
        self._char_set_flag = 'L'
        # init scrambler interface.
        self._scrambler = ScramblerInterface(enigma_obj.scrambler)
        # init plugboard interface.
        if isinstance(enigma_obj.plugboard, SteckerPlugboard):
            self._plugboard = SteckerPlugboardInterface(enigma_obj.plugboard)
        elif isinstance(enigma_obj.plugboard, UhrBoxPlugboard):
            self._plugboard = UhrBoxPlugboardInterface(enigma_obj.plugboard)

    def menu(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Character set menu.\n"
            f"2. Scrambler menu.\n"
            f"3. Plugboard menu.\n"
            f"4. Code sheet setup.\n"
            f"5. Display machine.\n"
            f"6. User input.\n"
            f"7. Recieve message.\n"
            f"8. Transmit message.\n"
            f"9. Quit.\n"
        )

        while True:
            inpt = input(menu_str)
            if inpt == "1": self._character_set_menu()
            elif inpt == "2": self._scrambler.menu()
            elif inpt == "3": self._plugboard_menu()
            elif inpt == "4": self._code_sheet_setup()
            elif inpt == "5": self._display_machine()
            elif inpt == "6": self._enigma_input()
            elif inpt == "7": self._recieve_message()
            elif inpt == "8": self._transmit_message()
            elif inpt == "9": break
            else:
                print("Invalid input!. Try again.")

    def _plugboard_menu(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Select plugboard mode.\n"
            f"2. Plugboard setup.\n"
            f"3. Quit.\n"
        )

        while True:
            inpt = input(menu_str)
            if inpt == "1": self._select_plugboard_mode()
            elif inpt == "2": self._plugboard.menu()
            elif inpt == "3": break
            else:
                print("Invalid input!. Try again.")

    def _select_plugboard_mode(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Stecker plugboard.\n"
            f"2. Uhr box plugboard.\n"
            f"3. Quit.\n"
        )

        while True:
            inpt = input(menu_str)
            if inpt == "1":
                self._enigma_obj.set_plugboard_mode('S', self._char_set_flag)
                self._plugboard = SteckerPlugboardInterface(self._enigma_obj.plugboard)
                break
            elif inpt == "2":
                self._enigma_obj.set_plugboard_mode('U', self._char_set_flag)
                self._plugboard = UhrBoxPlugboardInterface(self._enigma_obj.plugboard)
                break
            elif inpt == "3":
                break
            else:
                print("Invalid input!. Try again.")

    def _code_sheet_setup(self):
        """

        """
        # get machine reflectors list, rotors list, plugboard mode and char set flag.
        # prompt user to select from code sheet.
        # get settings from code sheet.
        # set settings in machine.
        days = 32
        machine_type = self._enigma_obj.machine_type

        args = [
            days,
            Collection.device_list(machine_type, ["REF"]),
            Collection.device_list(machine_type, ["R_ROT"]),
            Collection.device_list(machine_type, ["F_ROT"]),
            self._char_set_flag,
            self._char_set_flag,
            self._enigma_obj.plugboard.plugboard_mode
        ]

        code_sheet = CodeSheetGenerator(*args)

        print(code_sheet.code_sheet_string())

        while True:
            menu_str= f"Enter a number in the range 1-{days} to select settings."

            try:
                inpt = int(input(menu_str))
            except ValueError:
                print("Invalid input!. Try again.")
            else:
                if 1 <= inpt <= days:
                    settings = code_sheet.get_settings(inpt)
                    self._enigma_obj.settings = settings
                    break
                else:
                    print("Invalid input!. Try again.")

    def _character_set_menu(self):
        """

        """
        # prompt user to enter a character set flag.
        # if char flag is valid set the scrambler and plugboard char set flag.
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Character set A-Z.\n"
            f"2. Character set 01-26.\n"
            f"3. Quit.\n"
        )

        while True:
            inpt = input(menu_str)
            if inpt == "1":
                self._char_set_flag = 'L'
                self._scrambler.character_set_flag('L')
                self._plugboard.character_set_flag('L')
                print("Enigma machine character set is set to alpha.")
                break
            elif inpt == "2":
                self._char_set_flag = 'N'
                self._scrambler.character_set_flag('N')
                self._plugboard.character_set_flag('N')
                print("Enigma machine character set is set to numerical.")
                break
            elif inpt == "3":
                break
            else:
                print("Invalid input!. Try again.")

    def _display_machine(self) -> None:
        """

        """
        print(self._enigma_obj.scrambler.collection)
        print(ef.line("SCRAMBLER"))
        print(f"\n{self._scrambler}\n")
        print(ef.line("PLUGBOARD"))
        print(f"\n{self._plugboard}\n")
        print(ef.line())

    def _enigma_input(self):
        """

        """
        if not self._enigma_obj.valid_enigma():
            print("Enigma setup is not complete. "
                  "Cannot accept input until setup is complete.")
        else:
            inpt = self._get_user_input()
            outp = self._convert_input(inpt)
            print(outp)

    def _get_user_input(self) -> str:
        """

        """
        inpt = input("Enter text to be converted.\n")

        return inpt.upper()

    def _recieve_message(self):
        """

        """
        # check enigma object is valid.
        # prompt for ip address.
        # prompt for a port number.
        # listen for message.
        # decrypt message.
        if not self._enigma_obj.valid_enigma():
            print("Enigma setup is not complete. "
                  "Cannot accept input until setup is complete.")
        else:
            ip_address = Telex.get_ip_address()
            port_number = Telex.get_port_number()
            print(f"Recieving on IP address {ip_address} port number {port_number}.")
            message = Telex.recieve(ip_address, port_number)
            message = self._convert_input(message)
            print(message)

    def _transmit_message(self):
        """

        """
        # check enigma is valid.
        # prompt for ip address.
        # prompt for port number.
        # prompt for input.
        # encrypt input.
        # transmit input.
        if not self._enigma_obj.valid_enigma():
            print("Enigma setup is not complete. "
                  "Cannot accept input until setup is complete.")
        else:
            ip_address = Telex.get_ip_address()
            port_number = Telex.get_port_number()
            print(f"Transmit on IP address {ip_address} port number {port_number}.")
            message = self._get_user_input()
            message = self._encrypt_input(message)
            Telex.transmit(message, ip_address, port_number)

    def _encrypt_input(self, inpt):
        """

        """
        clean_inpt = self._enigma_obj.keyboard.clean_input_string(inpt)
        outp = ""
        for char in clean_inpt:
            outp += self._enigma_obj.character_input(char)
        return outp

    def _convert_input(self, inpt: str) -> None:
        """

        """
        clean_inpt = self._enigma_obj.keyboard.clean_input_string(inpt)
        outp = ""
        for char in clean_inpt:
            outp += self._enigma_obj.character_input(char)
        hist = Histogram(clean_inpt, outp).__str__()
        _str = ef.line("HISTOGRAM")
        _str += '\n'
        _str += ef.center(hist)
        _str += '\n'
        _str += ef.line()
        _str += '\n'
        _str += ef.line("INPUT TEXT")
        _str += '\n\n'
        _str += ef.wrap_string(inpt, 6)
        _str += '\n\n'
        _str += ef.line()
        _str += '\n'
        _str += ef.line("CLEANED INPUT TEXT")
        _str += '\n\n'
        _str += ef.group_string(clean_inpt, 4)
        _str += '\n\n'
        _str += ef.line()
        _str += '\n'
        _str += ef.line("OUTPUT TEXT")
        _str += '\n\n'
        _str += ef.group_string(outp, 4)
        _str += '\n\n'
        _str += ef.line()
        return _str
