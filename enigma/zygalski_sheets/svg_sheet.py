

class SVGZygalskiSheet:

    CELL_SIZE = 12
    CELL_BORDER_WIDTH = 1
    CELLS_RECT_BORDER_WIDTH = 1
    SHEET_HEADER_HEIGHT = 10
    SHEET_BORDER_WIDTH = 12
    LETS_LEFT_OFFSET = -8.5
    LETS_RIGHT_OFFSET = 578.5
    LETS_TOP_OFFSET = -3.5
    LETS_BOTTOM_OFFSET = 583.5
    SHEET_ID_X = 20
    SHEET_ID_Y = 20
    LETS_SIZE = 7
    LETS_FONT = "sans-serif"
    SHEET_ID_SIZE = 7
    SHEET_ID_FONT = "sans-serif"
    TRUE = "#ffffff"
    FALSE = "#000000"

    def __init__(self):
        """

        """
        pass

    def render_sheet(self, data, sheet_id, group):
        """

        """
        self.data = data
        self.sheet_id = sheet_id
        self.group = group
        self.svg = ""
        self.render_sheet_rect()
        self.render_cells_rect()
        self.render_letters()
        self.render_cells()
        self.svg += "</g>\n"
        self.render_sheet_id()
        self.svg += "</g>\n"
        self.svg += "</svg>"

        return self.svg

    def render_sheet_rect(self):
        """

        """
        self.svg += "<?xml version='1.0' encoding='utf-8'?>\n"
        self.svg += "<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg' fill='#000000'>\n"
        self.svg += "<g transform='scale(0.125)'>\n"
        self.svg += f"<rect fill='#000000' height='{self.sheet_height()}' width='{self.sheet_width()}'/>\n"


    def render_cells_rect(self):
        """

        """
        self.svg += (f"<g id='cells_rect' "
                     f"transform='translate({self.SHEET_BORDER_WIDTH},{self.SHEET_BORDER_WIDTH + self.SHEET_HEADER_HEIGHT})'>\n")
        self.svg += (f"<rect height='{self.cells_rect_size()}' "
                     f"width='{self.cells_rect_size()}' "
                     f"stroke='#FFFFFF'/>\n")

    def render_letters(self):
        """

        """
        LETTERS = [chr(i) for i in range(65,91)]
        for i in range(26):
            self.svg += (f"<text x='{self.LETS_LEFT_OFFSET}' "
                         f"y='{(i*11) + 9}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")
            self.svg += (f"<text x='{self.LETS_LEFT_OFFSET}' "
                         f"y='{((i+26)*11) + 9}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")
            self.svg += (f"<text x='{self.LETS_RIGHT_OFFSET}' "
                         f"y='{(i*11) + 9}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")
            self.svg += (f"<text x='{self.LETS_RIGHT_OFFSET}' "
                         f"y='{((i+26)*11) + 9}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")

            self.svg += (f"<text x='{(i*11) + 4}' "
                         f"y='{self.LETS_TOP_OFFSET}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")
            self.svg += (f"<text x='{((i+26)*11) + 4}' "
                         f"y='{self.LETS_TOP_OFFSET}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")
            self.svg += (f"<text x='{(i*11) + 4}' "
                         f"y='{self.LETS_BOTTOM_OFFSET}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")
            self.svg += (f"<text x='{((i+26)*11) + 4}' "
                         f"y='{self.LETS_BOTTOM_OFFSET}' "
                         f"fill='#FFFFFF' "
                         f"font-family='monospace' "
                         f"font-size='8'>{LETTERS[i]}</text>\n")

    def render_cells(self):
        """

        """
        LETTERS = [chr(i) for i in range(65,91)]
        for x in range(52):
            for y in range(52):
                lx = LETTERS[x%26]
                ly = LETTERS[y%26]
                cell_data = self.data["data"][f"{lx}{ly}"][self.group]
                females = ""
                if cell_data:
                    for pair in cell_data:
                        pair.sort()
                    cell_data = [f"{pair[0]}{pair[1]}" for pair in cell_data]
                    cell_data = list(set(cell_data))
                    females = ','.join(cell_data)
                    fill = "#ffffff"
                else:
                    fill = "#000000"
                quadrant = ""
                if x < 26 and y < 26:
                    quadrant = "ul"
                elif x >= 26 and y < 26:
                    quadrant = "ur"
                elif x < 26 and y >= 26:
                    quadrant = "ll"
                elif x >= 26 and y >= 26:
                    quadrant = "lr"
                self.svg += (f"<rect id='{lx}{ly}-{quadrant}' "
                             f"females='{females}' "
                             f"stroke='#000000' "
                             f"fill='{fill}' "
                             f"width='{self.CELL_SIZE}' "
                             f"height='{self.CELL_SIZE}' "
                             f"x='{(x*11)+1}' "
                             f"y='{(y*11)+1}'/>\n")

    def render_sheet_id(self):
        """

        """
        self.svg += (f"<text id='sheet_id' "
                     f"x='16' "
                     f"y='8' "
                     f"fill='#FFFFFF' "
                     f"font-family='monospace' "
                     f"font-size='7'>{self.sheet_id}</text>\n")

    def cells_rect_size(self):
        """

        """
        return ((self.CELL_SIZE - self.CELL_BORDER_WIDTH) * 52) + self.CELL_BORDER_WIDTH + (self.CELL_BORDER_WIDTH * 2)

    def sheet_width(self):
        """

        """
        return self.cells_rect_size() + (self.CELLS_RECT_BORDER_WIDTH * 2) + (self.SHEET_BORDER_WIDTH * 2)

    def sheet_height(self):
        """

        """
        return self.sheet_width() + self.SHEET_HEADER_HEIGHT
    