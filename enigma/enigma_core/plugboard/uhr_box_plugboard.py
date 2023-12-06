from typing import Optional, Sequence, Dict, List
from enigma_core.plugboard.plugboard import Plugboard
from enigma_core.plugboard.exceptions import SocketIDError, PlugIDError
from enigma_core.plugboard.uhr_box import UhrBox
from enigma_core.settings.settings import LETTERS, NUMBERS


class UhrBoxPlugboard(Plugboard):

    def __init__(self, character_set_flag: Optional[str]='L') -> None:
        """
        Takes an optional character set flag of 'L' or 'N'. Defaults to 'L' if
        no flag is provided. 
        """
        print("INIT UHR BOX PLUGBOARD")
        super(UhrBoxPlugboard, self).__init__()
        self.plugboard_mode = "U"
        self.ub = UhrBox()
        self._charset_flag = None
        self._charset = None
        self.uhr_plugs_map = {}
        self._make_uhr_plugs_map()
        self.character_set_flag = character_set_flag

    def __str__(self) -> str:
        """
        Returns the string repressentation of the plugboard and uhr box rotor
        setting.
        """
        ub_str = f"Uhr Box Setting: {self.rotor_setting}\n\n"
        ub_str += self._plugboard_str()
        return ub_str

    def _plugboard_str(self) -> str:
        """
        Returns the string repressentation of the plugboard.
        """
        pb_str = ""
        for i in range(10):
            pa = f"{str(i+1).rjust(2, '0')}A"
            pb = f"{str(i+1).rjust(2, '0')}B"
            sa = self.uhr_plugs_map[pa] or "--"
            sb = self.uhr_plugs_map[pb] or "--"
            pb_str += f"{pa} ---> {sa.ljust(2, ' ')}" if sa else f"{pa} --->   "
            pb_str += "        "
            pb_str += f"{pb} ---> {sb.ljust(2, ' ')}" if sb else f"{pb} --->   "
            if i != 9: pb_str += '\n'
        return pb_str

    @property
    def rotor_setting(self) -> int:
        """
        Returns the uhr box rotor setting.
        """
        return self.ub.rotor_setting

    @rotor_setting.setter
    def rotor_setting(self, setting: int) -> None:
        """
        Takes an uhr box rotor setting and sets uhr box rotor to that 
        settting.
        """
        self.ub.rotor_setting = setting
        self._make_translation_arrays()

    def connect(self, plug_id: str, socket_id: str) -> None:
        """
        Takes an uhr box plug id and plugboard socket id. Makes a connection
        betwen that uhr box plug and plugboard socket.
        """
        self.valid_plug_id(plug_id)
        self.valid_socket_id(socket_id)
        self.disconnect(socket_id)
        self.uhr_plugs_map[plug_id] = socket_id
        self._make_translation_arrays()

    def disconnect(self, socket_id: str) -> None:
        """
        Takes a plugboard socket id. If an uhr box plug is connected to that
        plugboard socket the plug will be disconnected.
        """
        self.valid_socket_id(socket_id)
        for _, _socket_id in self.uhr_plugs_map.items():
            if socket_id == _socket_id:
                self.uhr_plugs_map[socket_id] = None
                self._make_translation_arrays()
                break

    def is_connected(self, socket_id: str) -> bool:
        """
        Takes a plugboard socket id. If uhr box plug is connected to that
        plugboard socket True is returned else False.
        """
        self.valid_socket_id(socket_id)
        if socket_id in self.uhr_plugs_map.values():
            return True
        return False

    def connected_plug(self, socket_id: str) -> Optional[str]:
        """
        Takes a plugboard socket id. If there is an uhr box plug connected to
        that plugboard socket then that uhr box plug id is returned. If no
        connection is found returns None.
        """
        self.valid_socket_id(socket_id)
        for plug_id, _socket_id in self.uhr_plugs_map.items():
            if socket_id == _socket_id:
                return plug_id
            
        return None

    def connected_to(self, socket_id: str, contact_type: str) -> str:
        """
        Takes a plugboard socket id and contact type and returns the plugboard
        socket id that contact is connected to.
        """
        self.valid_socket_id(socket_id)
        for plug_id, _socket_id in self.uhr_plugs_map.items():
            if socket_id == _socket_id:
                _contact_id = self.ub.connected_contact_id(plug_id, contact_type)
                _plug_id = _contact_id[0]
                return self.uhr_plugs_map[_plug_id]
        return socket_id

    def number_of_connected(self) -> int:
        """
        Returns the number of connected uhr box plugs.
        """
        count = 0
        for socket_id in self.uhr_plugs_map.values():
            if socket_id:
                count += 1
        return count

    def clear(self) -> None:
        """
        Clears all plugboard connections.
        """
        self._make_uhr_plugs_map()
        self._make_translation_arrays()

    def make_connections(self, connections: Dict[str, str]) -> None:
        """
        Takes a dictionary object that maps uhr box plug ids to plugboard
        socket ids and makes those connections.
        """
        self.clear()
        for plug_id, socket_id in connections.items():
            self.connect(plug_id, socket_id)
        self._make_translation_arrays()

    def valid_socket_id(self, socket_id: str) -> str:
        """
        Takes a plugboard socket id and returns True if valid else raises a
        SocketIDError.
        """
        if socket_id not in self._charset:
            msg = ("Plugboard Socket ID error! "
                   f"{socket_id} is not a valid socket id. "
                   f"Must be in {self._charset}")
            raise SocketIDError(msg)
        return socket_id

    def valid_plug_id(self, plug_id: str) -> bool:
        """
        Takes an uhr box plug id and returns True if valid else raises a
        ValueError.
        """
        plug_ids = self.ub.PLUG_A_IDS + self.ub.PLUG_B_IDS
        if plug_id not in plug_ids:
            msg = ("Uhr Box Plug ID error! "
                   f"{plug_id} is not a valid Uhr Plug ID. "
                   f"Must be in {plug_ids}")
            raise PlugIDError(msg)
        return plug_id

    @property
    def character_set(self) -> List[str]:
        """
        Returns the plugboard character set.
        """
        return self._charset

    @property
    def character_set_flag(self) -> str:
        """
        Returns the plugboard character set flag.
        """
        return self._charset_flag

    @character_set_flag.setter
    def character_set_flag(self, flag: str) -> None:
        """
        Takes a character set flag of 'L' or 'N' and converts the plugboard
        to that character set.
        """
        if flag == None: return
        flags = ['L','N']
        if flag in flags and flag != self._charset_flag:
            self._charset_flag = flag
            self._charset = LETTERS if flag == 'L' else NUMBERS
            translation = {}
            for i in range(len(LETTERS)):
                if flag == 'L': translation[NUMBERS[i]] = LETTERS[i]
                if flag == 'N': translation[LETTERS[i]] = NUMBERS[i]
            for plug_id, socket_id in self.uhr_plugs_map.items():
                if socket_id:
                    self.uhr_plugs_map[plug_id] = translation[socket_id]
        elif flag not in flags:
            msg = (
                f"Charset flag error!. {flag} is not a valid charset flag. "
                f"Must be 'L' or 'N'")
            raise ValueError(msg)

    def valid_plugboard(self) -> bool:
        """
        Returns a boolean value indicating if the plugboard is valid and
        ready for use.
        """
        n = self.number_of_connected()
        return n == 0 or n == 20
    
    @property
    def settings(self):
        """
        Returns a dictionary object with the plugboard mode, plugboard
        connections, uhr box setting and character set flag for the 
        plugboard.
        """
        settings = {}
        settings["plugboard_mode"] = self.plugboard_mode
        connections = {p : s for p, s in self.uhr_plugs_map.items() if s != None}
        settings["plugboard_connections"] = connections
        settings["uhr_box_setting"] = self.ub.rotor_setting
        settings["plugboard_char_flag"] = self.character_set_flag
        return settings

    @settings.setter
    def settings(self, settings):
        """
        Takes optional settings for plugboard connections, plugboard
        character set flag and an uhr box setting.
        """
        try:
            char_flag = settings["plugboard_char_flag"]
        except KeyError:
            pass
        else:
            self.character_set_flag = char_flag

        try:
            uhr_box_setting = settings["uhr_box_setting"]
        except KeyError:
            pass
        else:
            self.ub.rotor_setting = uhr_box_setting

        try:
            connections = settings["plugboard_connections"]
        except KeyError:
            pass
        else:
            self.make_connections(connections)

    def _make_uhr_plugs_map(self) -> None:
        """
        Initializes an uhr plug map that maps uhr plug ids to a None value.
        Will be used to map uhr plug ids to plugboard socket ids.
        """
        self.uhr_plugs_map = {}
        for plug_id in self.ub.PLUG_A_IDS:
            self.uhr_plugs_map[plug_id] = None
        for plug_id in self.ub.PLUG_B_IDS:
            self.uhr_plugs_map[plug_id] = None

    def _make_translation_arrays(self) -> None:
        """
        Makes the translation arrays that maps the wiring between the large
        and small plugboard contacts that may be directly connected to each
        other if there is no plug connected at that socket or through the
        uhr box if there is an uhr box plug connected at that location.
        """
        lg_contact_arr = [i for i in range(26)]
        sm_contact_arr = [i for i in range(26)]

        for _, socket_id in self.uhr_plugs_map.items():
            if socket_id:
                socket_id1 = self.connected_to(socket_id, 'LG')
                if socket_id1:
                    lg_contact_arr[self._charset.index(socket_id)] = self._charset.index(socket_id1)
                socket_id2 = self.connected_to(socket_id, 'SM')
                if socket_id2:
                    sm_contact_arr[self._charset.index(socket_id)] = self._charset.index(socket_id2)
        self.lg_contact_arr = lg_contact_arr
        self.sm_contact_arr = sm_contact_arr
