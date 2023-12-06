from collections import deque        


class UhrBox:

    POSITIONS = 40

    CONNECTIONS = [
        6, 31, 4, 29, 18, 39, 16, 25, 30, 23,
        28, 1, 38, 11, 36, 37, 26, 27, 24, 21,
        14, 3, 12, 17, 2, 7, 0, 33, 10, 35,
        8, 5, 22, 19, 20, 13, 34, 15, 32, 9
    ]

    PLUG_A_IDS = [
        '01A', '02A', '03A', '04A', '05A',
        '06A', '07A', '08A', '09A', '10A'
    ]

    PLUG_B_IDS = [
        '01B', '02B', '03B', '04B', '05B',
        '06B', '07B', '08B', '09B', '10B'
    ]

    PLUG_A_MAP = {
        0: ('01A','LG'), 2: ('01A','SM'),
        4: ('02A','LG'), 6: ('02A','SM'),
        8: ('03A','LG'), 10: ('03A','SM'),
        12: ('04A','LG'), 14: ('04A','SM'),
        16: ('05A','LG'), 18: ('05A','SM'),
        20: ('06A','LG'), 22: ('06A','SM'),
        24: ('07A','LG'), 26: ('07A','SM'),
        28: ('08A','LG'), 30: ('08A','SM'),
        32: ('09A','LG'), 34: ('09A','SM'),
        36: ('10A','LG'), 38: ('10A','SM')
    }

    PLUG_B_MAP = {
        0: ('07B','LG'), 2: ('07B','SM'),
        4: ('01B','LG'), 6: ('01B','SM'),
        8: ('08B','LG'), 10: ('08B','SM'),
        12: ('06B','LG'), 14: ('06B','SM'),
        16: ('02B','LG'), 18: ('02B','SM'),
        20: ('09B','LG'), 22: ('09B','SM'),
        24: ('05B','LG'), 26: ('05B','SM'),
        28: ('03B','LG'), 30: ('03B','SM'),
        32: ('10B','LG'), 34: ('10B','SM'),
        36: ('04B','LG'), 38: ('04B','SM')
    }

    def __init__(self) -> None:
        self.setting = 0
        self._rotor_tables = {}
        self._contacts_map = {}
        self._make_rotor_tables()
        self._make_contacts_map()

    def __str__(self) -> str:
        """
        Returns the string repressentation of the uhr box.
        """
        _str = f"UHR BOX SETTING {str(self.setting).rjust(2, '0')}\n"
        for _, c1 in self.PLUG_A_MAP.items():
            c2 = self._contacts_map[c1]
            _str += f"{c1[0]}{c1[1]} <----> {c2[0]}{c2[1]}\n"
        return _str

    def __repr__(self) -> str:
        """
        Returns the string repressentation of the uhr box.
        """
        return self.__str__()

    @property
    def rotor_setting(self) -> int:
        """
        Returns the uhr box rotor setting.
        """
        return self.setting

    @rotor_setting.setter
    def rotor_setting(self, setting: int) -> None:
        """
        Takes an uhr box rotor setting and sets the uhr box rotor to that 
        position.
        """
        if setting in range(self.POSITIONS):
            self.setting = setting
            self._make_contacts_map()
        else:
            msg = "Uhr Box setting eror!. "
            msg += f"{setting} is not a valid setting. "
            msg += "Must be in range 0 -> 39"
            raise ValueError(msg)

    def connected_contact_id(self, plug_id: str, contact_type: str) -> str:
        """
        Takes an uhr plug id and contatct type and returns the contact id of
        the connected contact.
        """
        self.valid_plug_id(plug_id)
        self.valid_contact_type(contact_type)
        return self._contacts_map[(plug_id, contact_type)]

    def valid_plug_id(self, plug_id: str) -> bool:
        """
        Takes an uhr plug id and returns True if valid else raises ValueError.
        """
        plug_ids = self.PLUG_A_IDS + self.PLUG_B_IDS
        if plug_id not in plug_ids:
            msg = f"Uhr Box Plug ID error! {plug_id} not a valid Plug ID."
            raise ValueError(msg)
        else:
            return True

    @staticmethod
    def valid_contact_type(contact_type: str) -> bool:
        """
        Takes a contact type and returns True if valid else raises a 
        ValueError.
        """
        contact_types = ["LG","SM"]
        if contact_type not in contact_types:
            msg = "Uhr Box Contact Type error! "
            msg += f"{contact_type} is not a valid contact type. "
            msg += "Must be 'LG' or 'SM'"
            raise ValueError(msg)
        else:
            return True

    def _make_contacts_map(self) -> None:
        """
        Makes a contact map that maps contact ids of connected uhr box 
        contacts.
        """
        contact_map = {}
        
        for t1, c1 in self.PLUG_A_MAP.items():
            t2 = self._rotor_tables[self.setting][t1]
            c2 = self.PLUG_B_MAP[t2]
            contact_map[c1] = c2
            contact_map[c2] = c1
        self._contacts_map = contact_map

    def _make_rotor_tables(self) -> None:
        """
        Makes a map of each uhr box rotor position to a rotor wiring 
        translation array for that rotor position.
        """
        table = {}

        connections = deque(self.CONNECTIONS)

        for i in range(self.POSITIONS):
            table[i] = [*connections]
            connections.rotate(-1)
            for j in range(len(connections)):
                num = connections[j] -1
                if num == -1:
                    num = self.POSITIONS -1
                connections[j] = num
        self._rotor_tables = table
