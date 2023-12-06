from typing import Optional, Dict, List, Any


class WiringError(Exception):

    def __init__(self, msg, error_code):
        """
        Takes an error message to initialize exeption.
        """
        self.error_code = error_code
        super().__init__(msg)


class WiringCharactersDescriptor:

    CHARSET = [chr(i) for i in range(65, 91)]

    def __init__(self, self_wired: Optional[bool]=False) -> None:
        """

        """
        self.self_wired = self_wired

    def __set_name__(self, owner: str, name: str) -> None:
        """

        """
        self.private_name = '_' + name

    def __get__(self, obj: Any, objtype: Optional[type]=None) -> List[str]:
        """

        """
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, val: List[str]) -> None:
        """

        """

        # check is list
        if type(val) != list:
            msg = (f"{obj.device_id} wire list is type "
                   f"{type(val)}. Must be type list")
            raise WiringError(msg, 1)

        # check list is correct length
        if len(val) != len(self.CHARSET):
            msg = (f"{obj.device_id} wire list is length {len(val)}. "
                   f"Must be length {len(self.CHARSET)}")
            raise WiringError(msg, 2)

        # check for invalid characters
        invalid_chars = [c for c in val if c not in self.CHARSET]
        if invalid_chars:
            msg = (f"Invalid character(s) '{','.join(invalid_chars)}' "
                   f"in wiring for {obj.device_id}. "
                   f"Wiring list must contain characters A-Z.")
            raise WiringError(msg, 3)

        # check for duplicate characters
        duplicate = [c for c in val if val.count(c) > 1]
        duplicate = list(set(duplicate))
        if duplicate:
            msg = (f"Duplicate character(s) '{','.join(duplicate)}'"
                   f" in wiring list for {obj.device_id}")
            raise WiringError(msg, 4)
        
        # check for self wired if applicable
        self_wired_chars = [c for i, c in enumerate(val) if c == self.CHARSET[i]]
        if not self.self_wired and self_wired_chars:
            msg = (f"Character(s) '{','.join(self_wired_chars)}' are "
                   f"self wired for {obj.device_id}. Self wired "
                   f"characters are not permitted for this device.")
            raise WiringError(msg, 5)

        val = [char.upper() for char in val]
        setattr(obj, self.private_name, val)
