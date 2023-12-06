

class Plugboard:

    def __init__(self) -> None:
        """
        Initialize the connection lists.
        """
        self.lg_contact_arr = [i for i in range(26)]
        self.sm_contact_arr = [i for i in range(26)]

    def __repr__(self) -> str:
        """
        Returns the string repressentation of the plugboard. Show which LG
        connection is connected to which SM connection.
        """
        conns = zip(self.lg_contact_arr, self.sm_contact_arr)
        pb_str = "L     S\n"
        for conn in conns:
            pb_str += f"{conn[0]} <-> {conn[1]}\n"
        return pb_str

    def lg_contact_output(self, index: int) -> int:
        """
        Takes an index in range 0-25. Returns the number at that index in the
        LG contact array.
        """
        try:
            index = self.lg_contact_arr[index]
        except Exception as e:
            raise e
        else:
            return index

    def sm_contact_output(self, index: int) -> int:
        """
        Takes an index in range 0-25. Returns the number at that index in the
        SM contact array.
        """
        try:
            index = self.sm_contact_arr[index]
        except Exception as e:
            raise e
        else:
            return index