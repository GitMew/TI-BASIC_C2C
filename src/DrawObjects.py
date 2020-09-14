"""
Classes to catalogue objects on the canvas, and subsequently convert them to TI-BASIC commands.

Author: T. Bauwens
Date: 2020-09-12
"""
# Outline of conversion flow:
#  1. GUI interactions to canvas object
#  2. Canvas object to command text
from src.CanvasDrawing import *


class Draw_Object:
    def __init__(self):
        self.is_selected = False
        self.drag = None  # When not None, stores relative mouse coordinates when dragging the object.

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False
        self.drag = None

    @staticmethod
    def drawSelection(G: Grid, nomargin_topleft_x, nomargin_topleft_y, nomargin_width, nomargin_height, thickness, margin, sel_colour: tuple=COL_SELECTION):
        pygame.draw.rect(G.dis, sel_colour,
                         [nomargin_topleft_x - margin, nomargin_topleft_y - margin,
                          nomargin_width + 2 * margin, nomargin_height + 2 * margin],
                         thickness)


class Draw_Text(Draw_Object):
    def __init__(self, x, y, text, is_lower):
        super().__init__()
        # Default values as field declarations
        self.x = 0
        self.y = 0
        self.text = ""  # This is needed for setCase to work at initialisation

        self.cellcount = 0
        self.is_lower = False
        self.letterheight = 0
        self.cursor = 0

        # Actual setters
        self.setPos(x, y)
        self.setCase(is_lower)  # This is needed for setText to work at initialisation
        self.setText(text)

    def setPos(self, x: int, y: int):
        """
        Sets grid cell coordinates for this text.
        """
        self.x = x
        self.y = y

    def setCase(self, is_lower: bool):
        self.is_lower = is_lower
        self.letterheight = len( (UPPER_MATRICES if not is_lower else LOWER_MATRICES).get("A", [[]]) )
        self.cellcount = self.getCellCount()

    def switchCase(self):
        self.setCase(not(self.is_lower))

    def setText(self, new_text):
        self.text = new_text
        self.cellcount = self.getCellCount()

    def getCellCount(self):
        return charstringWidth(self.text, self.is_lower)

    def getHitbox(self, G: Grid):
        """
        Returns a tuple of 2-tuples: (topleft_x, topleft_y) and (width, height). All are measured in pixels!
        """
        return ((self.x*G.grid_x, self.y*G.grid_y),
                (self.cellcount*G.grid_x, self.letterheight*G.grid_y))

    def addTextAtCursor(self, added_text):
        self.setText(self.text[:self.cursor] + added_text + self.text[self.cursor:])
        self.cursor += len(added_text)

    def removeTextAtCursor(self, amount):
        new_cursor = max(0, self.cursor - amount)
        self.setText(self.text[:new_cursor] + self.text[self.cursor:])
        self.cursor = new_cursor

    def moveCursor(self, amount):
        self.cursor = min(max(self.cursor + amount, 0), len(self.text))

    def selectedMouseEvent(self, event, G: Grid):
        """
        Function handling mouse events inside the object when it is selected.
        """
        # ToDo:
        #  x Function for rebasing cursor based on mouse click
        #       > Maybe this is really just too difficult. I CAN get away with using arrow keys, though!
        #  x Function for clickdrag
        #       x Find a solution to the problem that the below MOUSEDOWN clause is run when the user clicks OUT of the
        #           text, thereby setting a drag for next time. > Fixed by resetting the drag at deselect.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                self.drag = (pos[0] - self.x*G.grid_x, pos[1] - self.y*G.grid_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = None
        elif event.type == pygame.MOUSEMOTION:
            if self.drag is not None:
                pos = pygame.mouse.get_pos()
                self.setPos(pos[0] // G.grid_x - self.drag[0] // G.grid_x,
                            pos[1] // G.grid_y - self.drag[1] // G.grid_y)

    def draw(self, G: Grid):
        G.textToCells(self.text, self.is_lower, self.x, self.y)

        if self.is_selected:
            # Box
            margin = 5
            thickness = 2
            hitbox = self.getHitbox(G)
            Draw_Object.drawSelection(G, hitbox[0][0], hitbox[0][1], hitbox[1][0], hitbox[1][1], thickness, margin)

            # Cursor
            # ToDo:
            #  - Should maybe blink
            #  X Position is (sadly) more complicated. It should be based on the string. We have this calculation already
            #    for the entire string (see getCellCount), so really, we need to put the functionality into one function.
            cursor_width = 2
            cursor_height = hitbox[1][1]
            cursor_offset = charstringWidth(self.text[:self.cursor], self.is_lower)
            pygame.draw.rect(G.dis, COL_SELECTION,
                [hitbox[0][0] + (cursor_offset + (0.5 if cursor_offset != 0 else -0.5))*G.grid_x, hitbox[0][1],
                 cursor_width, cursor_height])

    def toCommand(self):
        """
        Converts this text object to TI-BASIC Text() command. Note that for efficiency, the ending ") is left out.
        """
        return "Text({0}{1},{2},\"{3}".format("" if self.is_lower else "-1,", self.y, self.x, self.text.upper())
