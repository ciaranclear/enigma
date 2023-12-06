
LETTERS = [chr(i) for i in range(65, 91)]

NUMBERS = [f"{str(i+1).rjust(2, '0')}" for i in range(26)]

EQUIPMENT_DICT = {
    "WEHRMACHT":{
        "ROTORS":{
            "I":{
                "wiring_chars":['E','K','M','F','L','G','D','Q','V','Z','N','T','O',
                                'W','Y','H','X','U','S','P','A','I','B','R','C','J'],
                "turnover_chars":['Q']
            },
            "II":{
                "wiring_chars":['A','J','D','K','S','I','R','U','X','B','L','H','W',
                                'T','M','C','Q','G','Z','N','P','Y','F','V','O','E'],
                "turnover_chars":['E']
            },
            "III":{
                "wiring_chars":['B','D','F','H','J','L','C','P','R','T','X','V','Z',
                                'N','Y','E','I','W','G','A','K','M','U','S','Q','O'],
                "turnover_chars":['V']
            },
            "IV":{
                "wiring_chars":['E','S','O','V','P','Z','J','A','Y','Q','U','I','R',
                                  'H','X','L','N','F','T','G','K','D','C','M','W','B'],
                 "turnover_chars":['J']
            },
            "V":{
                "wiring_chars":['V','Z','B','R','G','I','T','Y','U','P','S','D','N',
                                'H','L','X','A','W','M','J','Q','O','F','E','C','K'],
                "turnover_chars":['Z']}
            },
        "REFLECTORS":{
            "UKW-A":['E','J','M','Z','A','L','Y','X','V','B','W','F','C',
                     'R','Q','U','O','N','T','S','P','I','K','H','G','D'],
            "UKW-B":['Y','R','U','H','Q','S','L','D','P','X','N','G','O',
                     'K','M','I','E','B','F','Z','C','W','V','J','A','T'],
            "UKW-C":['F','V','P','J','I','A','O','Y','E','D','R','Z','X',
                     'W','G','C','T','K','U','Q','S','B','N','M','H','L']
        },
        "CELLS_MAP":{
            "REF":"REF",
            "RS":"R_ROT",
            "RM":"R_ROT",
            "RF":"R_ROT"
        },
    },

    "LUFTWAFFE":{
        "ROTORS":{
            "I":{
                "wiring_chars":['E','K','M','F','L','G','D','Q','V','Z','N','T','O',
                                 'W','Y','H','X','U','S','P','A','I','B','R','C','J'],
                "turnover_chars":['Q']
            },
            "II":{
                "wiring_chars":['A','J','D','K','S','I','R','U','X','B','L','H','W',
                                 'T','M','C','Q','G','Z','N','P','Y','F','V','O','E'],
                "turnover_chars":['E']
            },
            "III":{
                "wiring_chars":['B','D','F','H','J','L','C','P','R','T','X','V','Z',
                                 'N','Y','E','I','W','G','A','K','M','U','S','Q','O'],
                "turnover_chars":['V']
            },
            "IV":{
                "wiring_chars":['E','S','O','V','P','Z','J','A','Y','Q','U','I','R',
                                 'H','X','L','N','F','T','G','K','D','C','M','W','B'],
                "turnover_chars":['J']
            },
            "V":{
                "wiring_chars":['V','Z','B','R','G','I','T','Y','U','P','S','D','N',
                                 'H','L','X','A','W','M','J','Q','O','F','E','C','K'],
                "turnover_chars":['Z']
            },
            "VI":{
                "wiring_chars":['J','P','G','V','O','U','M','F','Y','Q','B','E','N',
                                 'H','Z','R','D','K','A','S','X','L','I','C','T','W'],
                "turnover_chars":['Z','M']
            },
            "VII":{
                "wiring_chars":['N','Z','J','H','G','R','C','X','M','Y','S','W','B',
                                 'O','U','F','A','I','V','L','P','E','K','Q','D','T'],
                "turnover_chars":['Z','M']
            },
            "VIII":{
                "wiring_chars":['F','K','Q','H','T','L','X','O','C','B','J','S','P',
                                 'D','Z','R','A','M','E','W','N','I','U','Y','G','V'],
                "turnover_chars":['Z','M']
            }
        },
        "REFLECTORS":{
            "UKW-B":['Y','R','U','H','Q','S','L','D','P','X','N','G','O',
                     'K','M','I','E','B','F','Z','C','W','V','J','A','T'],
            "UKW-C":['F','V','P','J','I','A','O','Y','E','D','R','Z','X',
                     'W','G','C','T','K','U','Q','S','B','N','M','H','L'],
            "UKW-D":['B','C','D','E','F','G','H','I','J','K','L','M','N',
                     'O','P','Q','R','S','T','U','V','W','X','Y','Z','A']
        },
        "CELLS_MAP":{
            "REF":"REF",
            "RS":"R_ROT",
            "RM":"R_ROT",
            "RF":"R_ROT"
        },
    },

    "ENIGMA M3 Kriegsmarine":{
        "ROTORS":{
            "I":{
                "wiring_chars":['E','K','M','F','L','G','D','Q','V','Z','N','T','O',
                                 'W','Y','H','X','U','S','P','A','I','B','R','C','J'],
                "turnover_chars":['Q']
            },
            "II":{
                "wiring_chars":['A','J','D','K','S','I','R','U','X','B','L','H','W',
                                 'T','M','C','Q','G','Z','N','P','Y','F','V','O','E'],
                "turnover_chars":['E']
            },
            "III":{
                "wiring_chars":['B','D','F','H','J','L','C','P','R','T','X','V','Z',
                                 'N','Y','E','I','W','G','A','K','M','U','S','Q','O'],
                "turnover_chars":['V']
            },
            "IV":{
                "wiring_chars":['E','S','O','V','P','Z','J','A','Y','Q','U','I','R',
                                 'H','X','L','N','F','T','G','K','D','C','M','W','B'],
                "turnover_chars":['J']
            },
            "V":{
                "wiring_chars":['V','Z','B','R','G','I','T','Y','U','P','S','D','N',
                                 'H','L','X','A','W','M','J','Q','O','F','E','C','K'],
                "turnover_chars":['Z']
            },
            "VI":{
                "wiring_chars":['J','P','G','V','O','U','M','F','Y','Q','B','E','N',
                                 'H','Z','R','D','K','A','S','X','L','I','C','T','W'],
                "turnover_chars":['Z','M']
                },
            "VII":{
                "wiring_chars":['N','Z','J','H','G','R','C','X','M','Y','S','W','B',
                                 'O','U','F','A','I','V','L','P','E','K','Q','D','T'],
                "turnover_chars":['Z','M']
                },
            "VIII":{
                "wiring_chars":['F','K','Q','H','T','L','X','O','C','B','J','S','P',
                                 'D','Z','R','A','M','E','W','N','I','U','Y','G','V'],
                "turnover_chars":['Z','M']
            }
        },
        "REFLECTORS":{
            "UKW-B":['Y','R','U','H','Q','S','L','D','P','X','N','G','O',
                     'K','M','I','E','B','F','Z','C','W','V','J','A','T'],
            "UKW-C":['F','V','P','J','I','A','O','Y','E','D','R','Z','X',
                     'W','G','C','T','K','U','Q','S','B','N','M','H','L']
        },
        "CELLS_MAP":{
            "REF":"REF",
            "RS":"R_ROT",
            "RM":"R_ROT",
            "RF":"R_ROT"
        },
    },
    "ENIGMA M4 u-boat":{
        "ROTORS":{
            "I":{
                "wiring_chars":['E','K','M','F','L','G','D','Q','V','Z','N','T','O',
                                 'W','Y','H','X','U','S','P','A','I','B','R','C','J'],
                "turnover_chars":['Q']
            },
            "II":{
                "wiring_chars":['A','J','D','K','S','I','R','U','X','B','L','H','W',
                                 'T','M','C','Q','G','Z','N','P','Y','F','V','O','E'],
                "turnover_chars":['E']
            },
            "III":{
                "wiring_chars":['B','D','F','H','J','L','C','P','R','T','X','V','Z',
                                 'N','Y','E','I','W','G','A','K','M','U','S','Q','O'],
                "turnover_chars":['V']
            },
            "IV":{
                "wiring_chars":['E','S','O','V','P','Z','J','A','Y','Q','U','I','R',
                                 'H','X','L','N','F','T','G','K','D','C','M','W','B'],
                "turnover_chars":['J']
            },
            "V":{
                "wiring_chars":['V','Z','B','R','G','I','T','Y','U','P','S','D','N',
                                 'H','L','X','A','W','M','J','Q','O','F','E','C','K'],
                "turnover_chars":['Z']
            },
            "VI":{
                "wiring_chars":['J','P','G','V','O','U','M','F','Y','Q','B','E','N',
                                 'H','Z','R','D','K','A','S','X','L','I','C','T','W'],
                "turnover_chars":['Z','M']
            },
            "VII":{
                "wiring_chars":['N','Z','J','H','G','R','C','X','M','Y','S','W','B',
                                 'O','U','F','A','I','V','L','P','E','K','Q','D','T'],
                "turnover_chars":['Z','M']
            },
            "VIII":{
                "wiring_chars":['F','K','Q','H','T','L','X','O','C','B','J','S','P',
                                 'D','Z','R','A','M','E','W','N','I','U','Y','G','V'],
                "turnover_chars":['Z','M']
            },
            "Beta":{
                "wiring_chars":['L','E','Y','J','V','C','N','I','X','W','P','B','Q',
                                 'M','D','R','T','A','K','Z','G','F','U','H','O','S'],
                "turnover_chars":[]
            },
            "Gamma":{
                "wiring_chars":['F','S','O','K','A','N','U','E','R','H','M','B','T',
                                 'I','Y','C','W','L','Q','P','Z','X','V','G','J','D'],
                "turnover_chars":[]
            }
        },
        "REFLECTORS":{
            "UKW-B":['E','N','K','Q','A','U','Y','W','J','I','C','O','P',
                     'B','L','M','D','X','Z','V','F','T','H','R','G','S'],
            "UKW-C":['R','D','O','B','J','N','T','K','V','E','H','M','L',
                     'F','C','W','Z','A','X','G','Y','I','P','S','U','Q']
        },
        "CELLS_MAP":{
            "REF":"REF",
            "R4":"F_ROT",
            "RS":"R_ROT",
            "RM":"R_ROT",
            "RF":"R_ROT"
        },
    }
}


MORSE_CODE = {
      'A':'. _',
      'B':'_ . . .',
      'C':'_ . _ .',
      'D':'_ . .',
      'E':'.',
      'F':'. . _ .',
      'G':'_ _ .',
      'H':'. . . .',
      'I':'. .',
      'J':'. _ _ _',
      'K':'_ . _',
      'L':'. _ . .',
      'M':'_ _',
      'N':'_ .',
      'O':'_ _ _',
      'P':'. _ _ .',
      'Q':'_ _ . _',
      'R':'. _ .',
      'S':'. . .',
      'T':'_',
      'U':'. . _',
      'V':'. . . _',
      'W':'. _ _',
      'X':'_ . . _',
      'Y':'_ . _ _',
      'Z':'_ _ . .',
      '1':'. _ _ _ _',
      '2':'. . _ _ _',
      '3':'. . . _ _',
      '4':'. . . . _',
      '5':'. . . . .',
      '6':'_ . . . .',
      '7':'_ _ . . .',
      '8':'_ _ _ . .',
      '9':'_ _ _ _ .',
      '0':'_ _ _ _ _',
      '. _':'A',
      '_ . . .':'B',
      '_ . _ .':'C',
      '_ . .':'D',
      '.':'E',
      '. . _ .':'F',
      '_ _ .':'G',
      '. . . .':'H',
      '. .':'I',
      '. _ _ _':'J',
      '_ . _':'K',
      '. _ . .':'L',
      '_ _':'M',
      '_ .':'N',
      '_ _ _':'O',
      '. _ _ .':'P',
      '_ _ . _':'Q',
      '. _ .':'R',
      '. . .':'S',
      '_':'T',
      '. . _':'U',
      '. . . _':'V',
      '. _ _':'W',
      '_ . . _':'X',
      '_ . _ _':'Y',
      '_ _ . .':'Z',
      '. _ _ _ _':'1',
      '. . _ _ _':'2',
      '. . . _ _':'3',
      '. . . . _':'4',
      '. . . . .':'5',
      '_ . . . .':'6',
      '_ _ . . .':'7',
      '_ _ _ . .':'8',
      '_ _ _ _ .':'9',
      '_ _ _ _ _':'0'
}

