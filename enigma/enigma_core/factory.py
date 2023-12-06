"""



settings = {
    scrambler_char_flag:
    scrambler_turnover_flag:
    plugboard_char_flag:
    plugboard_mode:
    reflector:
    rotor_types:
    rotor_settings:
    ring_settings:
}
"""
from typing import Dict, List, Optional
from enigma_core.enigma_core.enigma import Enigma
from enigma_core.settings.settings import EQUIPMENT_DICT

def make_machine(machine_type: str, settings: Optional[Dict]=None) -> Enigma:
    """

    """
    settings = settings or {}
    try:
        EQUIPMENT_DICT[machine_type]
    except KeyError:
        raise ValueError(f"{machine_type} is not a valid machine type")
    else:
        enigma = Enigma(machine_type,
            scrambler_char_flag='L',
            plugboard_char_flag='L',
            plugboard_mode='S'
        )

        if settings:
            enigma.settings = settings
        return enigma

def machine_list() -> List[str]:
    """

    """
    return list(EQUIPMENT_DICT.keys())
