"""
Classes to catalogue objects on the canvas, and subsequently convert them to TI-BASIC commands.

Author: T. Bauwens
Date: 2020-09-12
"""
# Outline of conversion flow:
#  1. GUI interactions to canvas object
#  2. Canvas object to command text

# ToDo: Interaction in GUI with text (probably in Main.py, rather than here)
#   - Text object creation keybind
#   - Text object editing
#   - Draggable text
#   - Caps lock keybind for single (whole) text object
from src.CanvasDrawing import *


class Draw_Object:
    def __init__(self):
        self.is_selected = False

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    @staticmethod
    def drawSelection(nomargin_topleft_x, nomargin_topleft_y, nomargin_width, nomargin_height, thickness, margin,
                      dis, colour, grid_x, grid_y):
        pygame.draw.rect(dis, colour,
                         [nomargin_topleft_x - margin, nomargin_topleft_y - margin,
                          nomargin_width + 2 * margin, nomargin_height + 2 * margin],
                         thickness)


class Draw_Text(Draw_Object):
    def __init__(self, x, y, text, is_lower):
        super().__init__()
        self.x = x
        self.y = y
        self.setCase(is_lower)
        self.setText(text)

    def setCase(self, is_lower: bool):
        self.is_lower = is_lower
        self.letterheight = len( (UPPER_MATRICES if not is_lower else LOWER_MATRICES).get("A", [[]]) )

    def switchCase(self):
        self.setCase(not(self.is_lower))

    def setText(self, new_text):
        self.text = new_text
        self.cellcount = self.getCellCount()

    def getCellCount(self):
        count = 0
        for c in self.text:
            count += len((UPPER_MATRICES if not self.is_lower else LOWER_MATRICES).get(c, [[]])[0]) + 1
        return max(0, count - 1)

    def getHitbox(self, grid_x, grid_y):  # Note: measured in pixels
        return ((self.x*grid_x, self.y*grid_y),
                (self.cellcount*grid_x, self.letterheight*grid_y))

    def draw(self, dis, colour, grid_x, grid_y):
        textToCells(self.text, self.is_lower, self.x, self.y,
                    dis, colour, grid_x, grid_y)

        if self.is_selected:
            margin = 5
            thickness = 2
            hitbox = self.getHitbox(grid_x, grid_y)
            Draw_Object.drawSelection(hitbox[0][0], hitbox[0][1], hitbox[1][0], hitbox[1][1], thickness, margin,
                                      dis, COL_SELECTION, grid_x, grid_y)

    def toCommand(self):
        """
        Converts this text object to TI-BASIC Text() command. Note that for efficiency, the ending ") is left out.
        """
        return "Text({0}{1},{2},\"{3}".format("" if self.is_lower else "-1,", self.y, self.x, self.text.upper())