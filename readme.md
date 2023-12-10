# ENIGMA MACHINE
This is a command line enigma simulation tool which also includes additional tools such as a code sheet generator, zygalski sheet generators, indicator generators, permutation filter and statistical tools.

## MENUS

### START MENU
To see the start menu you can use python enigma.py -h
```code
usage: enigma.py [-h]
                 {interactive_enigma,enigma_simulator,code_sheet,statistics,indicators,permutations,zygalski_sheets,wehrmacht_catalog}

positional arguments:
  {interactive_enigma,enigma_simulator,code_sheet,statistics,indicators,permutations,zygalski_sheets,wehrmacht_catalog}
    interactive_enigma  interactive enigma
    enigma_simulator    cli enigma
    code_sheet          returns an enigma code sheet
    statistics          provides bigram trigram and index of coincidence values
    indicators          generates and filters enigma indicators
    permutations        solves for rotor permutations
    zygalski_sheets     generates zygalski sheets
    wehrmacht_catalog   generates the wehrmacht zygalski sheet data

optional arguments:
  -h, --help            show this help message and exit
```

### INTERACTIVE ENIGMA MENU
The interactive enigma is an interactive simulation of the enigma machine. You can navigate various menus to setup the enigma scrambler and plugboard. Both stecker and uhr box plugboards are simulated. You can also transmit and recieve mesages from another enigma machine using its IP address.
```code
usage: enigma.py interactive_enigma [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### ENIGMA SIMULATOR
Takes command line input to select an enigma machine, setup the scrambler and plugboard and produce an enigma message.
```code
usage: enigma.py enigma_simulator [-h] (-i INPUT_FILE | --message MESSAGE) [--rot-settings ROT_SETTINGS] [--rng-settings RNG_SETTINGS]
                                  [--scrambler-mode SCRAMBLER_MODE] [-c CHARSET] [--plugboard-mode PLUGBOARD_MODE]
                                  [--uhr-box-setting UHR_BOX_SETTING] [--plugboard-connections PLUGBOARD_CONNECTIONS] [-o OUTPUT_FILE]
                                  machine reflector rotors

positional arguments:
  machine               Enigma machine type ( WEHRMACHT | LUFTWAFFE | ENIGMA M3 Kriegsmarine | ENIGMA M4 u-boat )
  reflector             Reflector type in format "REF" 
                        WEHRMACHT                ( UKW-A | UKW-B | UKW-C )
                        LUFTWAFFE                ( UKW-B | UKW-C | UKW-D )
                        ENIGMA M3 Kriegsmarine   ( UKW-B | UKW-C )
                        ENIGMA M4 u-boat         ( UKW-B | UKW-C )
  rotors                Rotor types in format "R4,RS,RM,RF" or "RS,RM,RF" where
                        R4 = Static Rotor if applicable
                        RS = Slow Rotor
                        RM = Middle Rotor
                        RF = Fast Rotor
                         
                        WEHRMACHT                (  )              [I, II, III, IV, V]
                        LUFTWAFFE                (  )              [I, II, III, IV, V, VI, VII, VIII]
                        ENIGMA M3 Kriegsmarine   (  )              [I, II, III, IV, V, VI, VII, VIII]
                        ENIGMA M4 u-boat         ( Beta | Gamma )  [I, II, III, IV, V, VI, VII, VIII]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The input file path
  --message MESSAGE     The message string
  --rot-settings ROT_SETTINGS
                        Rotor settings in format [R4,RS,RM,RF] or [RS,RM,RF]
  --rng-settings RNG_SETTINGS
                        Ring settings in format [RS,RM,RF]
  --scrambler-mode SCRAMBLER_MODE
                        Scrambler turnover mode ( True | False )
  -c CHARSET, --charset CHARSET
                        Machine character set ( L | N ) where
                        L = Letters
                        N = Numbers
  --plugboard-mode PLUGBOARD_MODE
                        Plugboard mode ( S | U ) where
                        S = Stecker
                        U = Uhr Box
  --uhr-box-setting UHR_BOX_SETTING
                        Uhr box setting in range 0 - 39
  --plugboard-connections PLUGBOARD_CONNECTIONS
                        Plugboard settings for stecker mode
                        in format [AB,CD,EF,GH,IJ,KL,M,N,O,P,QR,ST] letters mode
                        in format [1 2,3 4,5 6,7 8,9 10,11 12,13,14,15 16,17,18,19 20] numbers mode
                        Plugboard settings for uhr box mode
                        in format "A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]" letter mode
                        in format "A=[1,2,3,4,5,6,7,8,9,10] B=[11,12,13,14,15,16,17,18,19,20]" number mode
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The output file path
```

### CODE SHEET GENERATOR MENU
Generates code sheets for all enigma machines. Can generate code sheets for stecker and uhr box plugboards.
```code
usage: enigma.py code_sheet [-h] [-o OUTPUT_FILE] machine format plugboard-mode days charset

positional arguments:
  machine               Enigma machine type ( WEHRMACHT | LUFTWAFFE | ENIGMA M3 Kriegsmarine | ENIGMA M4 u-boat )
  format                output format ( string format "S" | json format "J" )
  plugboard-mode        Plugboard mode ( stecker "S" | uhr box "U" )
  days                  Number of days integer value 1-999
  charset               Machine character set ( letters "L" | numbers "N" )

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The output-file path
```

### STATISTICS MENU
Can provide various statistics for text such as trigrams, bigrams and index of coincidence.
```code
usage: enigma.py statistics [-h] (-s INPUT_STRING | -i INPUT_FILE) (-b | -t | -ioc) [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -s INPUT_STRING, --input-string INPUT_STRING
  -i INPUT_FILE, --input-file INPUT_FILE
  -b, --bigram
  -t, --trigram
  -ioc, --index_of_coincidence
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
```

### INDICATORS MENU
Can generate the six character indicators that the germans used to setup there enigma machines. Can also filter an indicators file for females.
```code
usage: enigma.py indicators [-h] {generate_indicators,filter_indicators} ...

positional arguments:
  {generate_indicators,filter_indicators}
    generate_indicators
                        generates indicators
    filter_indicators   filters females from indicators

optional arguments:
  -h, --help            show this help message and exit
```

### PERMUTATIONS MENU
Takes an indicators file and returns the scrambler permutations that can produce all of the females in the indicators file.
```code
usage: enigma.py permutations [-h] indicators_file

positional arguments:
  indicators_file  indicators file path

optional arguments:
  -h, --help       show this help message and exit
```

### ZYGALSKI SHEETS MENU 
Can produce zygalski sheets in text or svg format.
```code
usage: enigma.py zygalski_sheets [-h] {svg_sheet,text_sheet} ...

positional arguments:
  {svg_sheet,text_sheet}
    svg_sheet           generates svg sheets
    text_sheet          generates text sheets

optional arguments:
  -h, --help            show this help message and exit
```

### WEHRMACHT CATALOG MENU
Can be used to create the wehrmacht catalog that is required to solve for scrambler permutations. The catalog is also used to produce zygalski sheets faster.
```code
usage: enigma.py wehrmacht_catalog [-h] (-c | -m | -f)

optional arguments:
  -h, --help  show this help message and exit
  -c          check if the catalog exists
  -m          make wehrmacht catalog
  -f          force remake of the wehrmacht catalog
```