from typing import OrderedDict, Dict


class Histogram:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [str(i) for i in range(10)]

    def __init__(self, input_str: str, output_str: str) -> None:
        self._input_str = input_str
        self._output_str = output_str
        self._alphanum_map = None
        self._alpha_map = None
        self._input_alpha_strings = None
        self._input_alphanum_strings = None
        self._output_strings = None
        self._make_translation_maps()
        self._make_character_bins()
        self._fill_histogram_bins()
        self.make_hist_string_dicts()

    def __str__(self) -> str:
        _str = ""
        for i in range(31):
            _str += self._input_alpha_strings[i]
            _str += "  "
            _str += self._input_alphanum_strings[i]
            _str += "  "
            _str += self._output_strings[i]
            _str += '\n'
        _str += '\n'
        _str += "    * = Full percent increment\n"
        _str += "    : = Greater than or equal to half of the percent increment\n"
        _str += "    . = Greater than 0 but less than half of the percent increment\n"
        return _str        

    @staticmethod
    def valid_character(character, filter: Dict[str, str]) -> str:
        try:
            filter[character]
        except KeyError:
            msg = f"{character} is not a valid histogram character"
            raise ValueError(msg)
        else:
            return filter[character]

    def hist_string(self) -> str:
        return self.__str__()

    def make_hist_string_dicts(self) -> None:
        self._input_alpha_strings = self.make_hist_string_dict(self._input_alpha_chars, "INPUT ALPHA CHARACTERS")
        self._input_alphanum_strings = self.make_hist_string_dict(self._input_alphanum_chars, "INPUT ALPHANUM CHARACTERS")
        self._output_strings = self.make_hist_string_dict(self._outp_alpha_chars, "OUTPUT ALPHA CHARACTERS")

    def make_hist_string_dict(
            self, 
            _dict: Dict[str, Dict], label: str
        ) -> Dict[int, Dict[int, str]]:
        bars = self.make_hist_bars(_dict)
        return self._make_hist_lines(bars, label)

    def make_hist_bars(self, _dict: Dict[str, Dict]) -> Dict[str, str]:
        hist_bars = OrderedDict((c, "") for c in _dict)

        for c in _dict:
            percent = _dict[c]["PERCENT"]
            _str = "{:.1f}".format(percent)
            _str = "{:0>5}".format(_str)
            _str = _str [::-1]
            _str += '-'
            _str += c
            _str += '|'
            _str += '-'
            if percent == 0:
                _str += f"{' '*19}"
            else:
                whole = int(percent // 1)
                fract = percent % 1
                if whole <= 10:
                    _str += f"{'*'*whole}"
                    if 0 < fract < 0.5:
                        _str += '.'
                    elif fract >= 0.5:
                        _str += ':'
                elif whole > 10:
                    _str += f"{'*'*int((whole/(100/9))+10)}"
                    if 0 < percent%10 < 5:
                        _str += '.'
                    elif 5 <= percent%10:
                        _str += ':'
                _str += c
            _str = _str.ljust(29, ' ')
            hist_bars[c] = _str
        return hist_bars

    def _make_hist_lines(self, _dict, x_axis_label) -> Dict[int, Dict[int, str]]:
        y_axis = [
            '    |','    |','    |','  % |',
            '    |','    |','    |','    |',
            '  0-|','  1-|','  2-|','  3-|',
            '  4-|','  5-|','  6-|','  7-|',
            '  8-|','  9-|',' 10-|',' 20-|',
            ' 30-|',' 40-|',' 50-|',' 60-|',
            ' 70-|',' 80-|',' 90-|','100-|',
            ' %  |'
        ]
        lines= {i+2:y_axis[i] for i in range(len(y_axis))}
        for i in range(len(y_axis)):
            for j in _dict:
                lines[i+2] += _dict[j][i]
        lines[1] = f"    -{'-'*len(_dict)}"
        lines[0] = f"     {x_axis_label.center(len(_dict), ' ')}"
        return {abs(i-len(lines)+1) : lines[i] for i in range(len(lines))}

    def _fill_histogram_bins(self) -> None:
        self._fill_bins(self._input_str, self._input_alpha_chars, self._alpha_map)
        self._fill_bins(self._input_str, self._input_alphanum_chars, self._alphanum_map)
        self._fill_bins(self._output_str, self._outp_alpha_chars, self._alpha_map)

    def _fill_bins(
            self, 
            _str: str, 
            bins: Dict[str, Dict], 
            filter: Dict[str, str]
        ) -> None:
        for char in _str:
            char = char.upper()
            char = self.valid_character(char, filter)
            bins[char]["COUNT"] += 1
        for char in bins:
            count = bins[char]["COUNT"]
            bins[char]["PERCENT"] = 100 * (float(count)/len(_str))
            
    def _make_translation_maps(self) -> None:
        """

        """
        self._alphanum_map = {str(n) : str(n) for n in range(10)}
        for l in self.LETTERS:
            self._alphanum_map[l] = l
        self._alpha_map = {
            '0':'P','1':'Q',
            '2':'W','3':'E',
            '4':'R','5':'T',
            '6':'Z','7':'U',
            '8':'I','9':'O'
            }
        for l in self.LETTERS:
            self._alpha_map[l] = l


    def _make_character_bins(self) -> None:
        self._input_alpha_chars = {c:{"COUNT":0, "PERCENT":0} for c in self.LETTERS}
        self._input_alphanum_chars = {c:{"COUNT":0, "PERCENT":0} for c in self.LETTERS}
        self._outp_alpha_chars = {c:{"COUNT":0, "PERCENT":0}for c in self.LETTERS}
        for num in self.NUMBERS:
            self._input_alphanum_chars[num] = {"COUNT":0, "PERCENT":0}
