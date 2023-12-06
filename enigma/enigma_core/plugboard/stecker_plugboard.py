from typing import Optional, Sequence, Dict, List, Tuple
from enigma_core.settings.settings import LETTERS, NUMBERS
from enigma_core.plugboard.plugboard import Plugboard
from enigma_core.plugboard.exceptions import SocketIDError


class SteckerPlugboard(Plugboard):

    def __init__(self, character_set_flag: Optional[str]='L') -> None:
        """

        """
        super(SteckerPlugboard, self).__init__()
        self.plugboard_mode = "S"
        self.sockets = {}
        self._charset_flag = None
        self._charset = None
        self.character_set_flag = character_set_flag
        self._make_sockets()

    def __str__(self) -> str:
        """
        Returns the string repressentation of the stecker plugboard.
        """
        def make_line(line, left_pad: Optional[str]='') -> str:
            pb_line = f"{left_pad}"
            pb_line += '  '.join([f"{str(self._charset[i]).ljust(2, pad)}" for i in line])
            pb_line += f"\n{left_pad}"
            pb_line += '  '.join([f"{str(self.sockets[self._charset[i]]).ljust(2, pad)}" for i in line])
            return pb_line

        alfa_layout = [
            [16,22,4,17,19,25,20,8,14],
            [0,18,3,5,6,7,9,10],
            [15,24,23,2,21,1,12,13,11]
        ]

        num_layout = [
            [0,1,2,3,4,5,6,7,8],
            [9,10,11,12,13,14,15,16],
            [17,18,19,20,21,22,23,24,25]
        ]

        if self._charset_flag == 'L':
            layout = alfa_layout
        elif self._charset_flag == 'N':
            layout = num_layout

        pad = ' ' if self._charset_flag == 'L' else '0'
        pb_str = ""
        pb_str += make_line(layout[0], '  ')
        pb_str += '\n'
        pb_str += make_line(layout[1], '    ')
        pb_str += '\n'
        pb_str += make_line(layout[2], '  ')
        return pb_str
    
    def __repr__(self) -> str:
        """
        Returns the string repressentation of the stecker plugboard.
        """
        return self.__str__()

    def connect(self, s1: str, s2: str) -> None:
        """

        """
        self.valid_socket_id(s1)
        self.valid_socket_id(s2)
        self.disconnect(s1)
        self.disconnect(s2)
        self.sockets[s1] = s2
        self.sockets[s2] = s1
        self._make_translation_arrays()

    def disconnect(self, s: str) -> None:
        """
        Takes a socket id. Disconnectes that socket and its connected socket.
        After disconnect the translation arrays are regenerated.
        """
        self.valid_socket_id(s)
        o = self.sockets[s]
        self.sockets[s] = s
        self.sockets[o] = o
        self._make_translation_arrays()

    def is_connected(self, s: str) -> bool:
        """
        Takes a socket id. Returns a boolean value indicating its connected
        status.
        """
        self.valid_socket_id(s)
        if self.sockets[s] == s:
            return False
        return True

    def connected_to(self, s: str) -> str:
        """
        Takes a socket id. Returns the connected socket id.
        """
        self.valid_socket_id(s)
        return self.sockets[s]

    def clear(self) -> None:
        """
        Clears the stecker plugboard.
        """
        self._make_sockets()

    def number_of_connections(self) -> int:
        """
        Returns the number of connections.
        """
        count = 0
        for socket_id in self._charset:
            if self.sockets[socket_id] != socket_id:
                count += 1
        return count

    def connected(self) -> List[Tuple[str, str]]:
        """
        Returns a list of connected sockets. Each tuple is a socket id and the
        socket id it is connected to.
        """
        conns = []
        for k, v in self.sockets.items():
            if k != v:
                pair = [k, v]
                pair.sort()
                if pair not in conns:
                    conns.append(pair)
        return conns

    def unconnected(self) -> List[str]:
        """
        Returns a list of unconnected socket ids. 
        """
        unconns = []
        for k, v in self.sockets.items():
            if k == v:
                unconns.append(k)
        return unconns

    def make_connections(self, connections: Sequence[Sequence[str]]) -> None:
        """
        Takes a list of socket id pairs to be connected. The plugboard will be
        cleared before the new connections are made.
        """
        self.clear()
        for connection in connections:
            self.connect(*connection)

    def valid_socket_id(self, socket_id: str) -> bool:
        """
        Takes a socket id. Returns a valid socket id. If not valid raises a
        SocketIDError.
        """
        if socket_id not in self._charset:
            msg = ("Plugboard Socket ID error! "
                   f"{socket_id} is not a valid socket id. "
                   f"Must be in {self._charset}")
            raise SocketIDError(msg)
        else:
            return socket_id

    def valid_plugboard(self) -> bool:
        """
        Will always return True as the stecker plugboard is always valid .As
        only valid connections can be made in pairs and diconnections are
        performed in pairs there is never any discontinuity within the
        plugboard.
        """
        return True

    @property
    def settings(self):
        """
        
        """
        settings = {}
        settings["plugboard_mode"] = self.plugboard_mode
        connections = []
        for s1 in self.character_set:
            s2 = self.connected_to(s1)
            if s1 != s2 and (s2, s1) not in connections:
                connections.append((s1, s2))
        settings["plugboard_connections"] = connections
        settings["plugboard_char_set_flag"] = self.character_set_flag
        return settings

    @settings.setter
    def settings(self, settings):
        """
        
        """
        try:
            connections = settings["plugboard_connections"]
        except KeyError:
            pass
        else:
            self.make_connections(connections)

        try:
            character_set_flag = settings["plugboard_char_set_flag"]
        except KeyError:
            pass
        else:
            self.character_set_flag = character_set_flag

    @property
    def character_set(self) -> List[str]:
        """
        Returns the current character set list.
        """
        return self._charset

    @property
    def character_set_flag(self) -> str:
        """
        Returns the current character set flag.
        """
        return self._charset_flag

    @character_set_flag.setter
    def character_set_flag(self, flag: str) -> None:
        """
        Takes a character set flag 'L' or 'N'.
        """
        if flag == None: return
        flags = ['L','N']
        if flag in flags and flag != self._charset_flag:
            self._charset_flag = flag
            self._charset = LETTERS if flag == 'L' else NUMBERS
            translation = {}
            for i in range(26):
                if flag == 'L': translation[NUMBERS[i]] = LETTERS[i]
                if flag == 'N': translation[LETTERS[i]] = NUMBERS[i]
            sockets = {}
            for k, v in self.sockets.items():
                sockets[translation[k]] = translation[v]
            self.sockets = sockets
        elif flag not in flags:
            msg = (
                f"Charset flag error!. {flag} is not a valid charset flag. "
                f"Must be 'L' or 'N'")
            raise ValueError(msg)

    def _make_sockets(self) -> None:
        """
        Initializes the socket dictionary with equal k, v pairs for each
        character in the character set.
        """
        self.sockets = { l : l for l in self._charset }

    def _make_translation_arrays(self) -> None:
        """
        Makes the translation arrays for LG and SM contacts.
        """
        for index, socket_id in enumerate(self._charset):
            self.lg_contact_arr[index] = self._charset.index(self.sockets[socket_id])
            self.sm_contact_arr[index] = self._charset.index(self.sockets[socket_id])
