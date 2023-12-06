from typing import Optional, List, Any
from enigma_core.settings.settings import LETTERS


class TurnoverListError(Exception):

    def __init__(self, msg):
        """

        """
        super().__init__(msg)


class TurnoverListDescriptor(object):

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
        for char in val:
           if char not in LETTERS:
               raise TurnoverListError(f"")
        turnovers = [LETTERS.index(c) for c in val]
        setattr(obj, self.private_name, turnovers)
