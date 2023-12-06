import re
from typing import Optional


class EnigmaFormatter:
    WIDTH = 116
    BORDER = '*'
    BOUNDARY = ['(',')']
    GROUP = 5

    @staticmethod
    def line(title: Optional[str]=None) -> str:
        ef = EnigmaFormatter
        if title:
            title = f"{ef.BOUNDARY[0]}{title}{ef.BOUNDARY[1]}"
            return title.center(ef.WIDTH, ef.BORDER)
        else:
            return f"{ef.BORDER*ef.WIDTH}"

    @staticmethod
    def center(text: str) -> str:
        """
        
        """
        ef = EnigmaFormatter
        pad = 0
        lines = text.split('\n')
        longest = len(max(lines, key=len))
        if longest < ef.WIDTH:
            pad = (ef.WIDTH - longest)//2
        for i in range(len(lines)):
            lines[i] = f"{' '*pad}" + lines[i]
        return '\n'.join(lines)

    @staticmethod
    def group_string(text: str, padding: Optional[int]=0) -> str:
        ef = EnigmaFormatter
        groups = [text[i:i+ef.GROUP] for i in range(0, len(text), ef.GROUP)]
        gpl = ((ef.WIDTH+1)-(padding*2))//(ef.GROUP+1)
        lines = [groups[i:i+gpl] for i in range(0, len(groups), gpl)]
        for i in range(len(lines)):
            lines[i] = ' '.join(lines[i])
        return ef.center('\n'.join(lines))

    @staticmethod
    def wrap_string1(text: str, padding: Optional[int]=0) -> str:
        ef = EnigmaFormatter
        pat = r'[\w]+'
        results = re.finditer(pat, text)
        _str = ''
        line = ""
        for result in results:
            word = result.group()
            # if adding space exceeds limit add newline but no space
            # if adding word exceeds limit move to next line
            # if adding word doesnt exceed limit add word
            #
            max_length = ef.WIDTH - (padding*2)
            if len(line) + len(word) >= max_length:
                line += '\n'
                line += word
                _str += line
                line = ""
            else:
                line += ' '
                line += word
        return ef.center(_str)

    @staticmethod
    def wrap_string(text: str, padding: Optional[int]=0) -> str:
        def line_length(line):
            length = 0
            for word in line:
                length += len(word)
            return length + len(line)

        def concat_word(word, line, lines):
            while word:
                # if word length greater than max_length wrap word
                if len(word) > max_length:
                    remaining = max_length - line_length(line)
                    _word = word[0:remaining]
                    word = word[remaining:-1]
                    line.append(_word)
                    lines.append(line)
                    line = []
                # add word if it will not exceed max_length
                elif len(word) + line_length(line) < max_length:
                    line.append(word)
                    break
                # if max_length will be exceeded start new line
                else:
                    lines.append(line)
                    line = []
                    line.append(word)
                    break
            return line, lines

        ef = EnigmaFormatter
        max_length = ef.WIDTH - (padding*2)
        line = []
        lines = []
        pat = r'[\w]+'
        results = re.finditer(pat, text)
        for result in results:
            word = result.group()
            line, lines = concat_word(word, line, lines)
        if line: lines.append(line)
        for i in range(len(lines)):
            lines[i] = ' '.join(lines[i])
        return ef.center('\n'.join(lines))
