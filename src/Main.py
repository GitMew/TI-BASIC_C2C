"""
TI-BASIC Canvas to Command Conversion Tool

Author: T. Bauwens
Date: 2020-09-12
"""
from src.DrawObjects import *

# ToDo:
#   x Since the combination "dis, colour, grid_x, grid_y" is so popular, I think we should make it a separate class,
#     and associate such an object with the app itself.
#   x Pointer cursor

# ToDo: Interaction in GUI with text (probably in Main.py, rather than here)
#   x Text object creation keybind
#   x Text object editing
#   x Caps lock keybind for single (whole) text object
#   x Draggable text
#   x Add movable text cursor (via arrow keys) (could be blinking, but eh ...)


def rectContainsCoord(rect, pos):  # rect is of the form: ( (TL_x,TL_y) , (width,height) )
    return rect[0][0] <= pos[0] <= rect[0][0] + rect[1][0] and rect[0][1] <= pos[1] <= rect[0][1] + rect[1][1]


class App:
    def __init__(self):
        # Graphics
        self.G = Grid()
        self.canvas_objects = []  # Last in the list is topmost layer on-canvas.

        # Internals
        self.cursor = pygame.mouse.get_pos()
        self.focused = None
        self.quit = False

    def addCanvasObject(self, obj: Draw_Object):
        self.canvas_objects.append(obj)

    def focusCanvasObject(self, obj: Draw_Object):
        obj.select()
        self.focused = obj

    def defocus(self):
        if self.focused is not None:
            self.focused.deselect()
        self.focused = None

    def eventHandler(self, event):  # Note: the if elif elif elif cascade determines overriding priority!
        # Window controls
        if event.type == pygame.QUIT:
            self.quit = True

        # Textbox controls
        elif isinstance(self.focused, Draw_Text):
            ##print("Textbox control")
            if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_CAPSLOCK:  # Capslock uses the KeyUp/KeyDown functionality for off/on.
                self.focused.switchCase()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.focused.removeTextAtCursor(1)
                elif event.key == pygame.K_RETURN:  # ToDo: Might want to make this an actual return
                    self.defocus()
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.focused.moveCursor(1 if event.key == pygame.K_RIGHT else -1)
                else:
                    self.focused.addTextAtCursor(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                self.focused.selectedMouseEvent(event, self.G)

        # Letter controls (if NOT in textbox)
        elif event.type == pygame.KEYDOWN:
            ##print("General key controls")
            c = event.unicode.lower()
            if c == "t":  # new [T]ext
                pos = pygame.mouse.get_pos()
                new_obj = Draw_Text(pos[0] // self.G.grid_x, pos[1] // self.G.grid_x, "", is_lower=False)
                self.  addCanvasObject(new_obj)
                self.focusCanvasObject(new_obj)
            if c == "p":  # [P]rint canvas commands (and write [P]rogram)
                print("=============\nProgram: ")
                lines = []
                for obj in self.canvas_objects:
                    line = obj.toCommand()
                    lines.append(line)
                    print(line)
                print("=============")
                # ToDo: Can you write .8xp files in Python?

        # General mouse controls (this goes last so that things don't happen to an objected that's theoretically already deselected.
        if event.type == pygame.MOUSEMOTION:
            ##print("General mouse movement")
            self.cursor = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ##print("General mouse buttons")
            selected_obj = None
            for obj in self.canvas_objects:
                if rectContainsCoord(obj.getHitbox(self.G), event.pos):
                    if selected_obj is not None:
                        selected_obj.deselect()
                    selected_obj = obj
                else:
                    obj.deselect()
            if selected_obj is not None:
                self.focusCanvasObject(selected_obj)
            else:
                self.defocus()

    def drawObjects(self):
        for obj in self.canvas_objects:
            obj.draw(self.G)

    def drawCursor(self):
        self.G.coordToCell(self.cursor[0] // self.G.grid_x, self.cursor[1] // self.G.grid_y)

    def main(self):
        g = Grid()
        dis = g.dis

        t = Draw_Text(20, 30, "Hello world", is_lower=False)
        self.addCanvasObject(t)

        # i = 0
        while not self.quit:
            dis.fill(COL_TI_GREY)
            self.drawObjects()
            self.drawCursor()

            # Event handler
            for event in pygame.event.get():
                self.eventHandler(event)

            # i += 1
            # coordToCell(i // 100, 15, dis, COL_TI_BLACK, GRID_X, GRID_Y)
            #
            # charToCells("A", False, 0, 0,
            #             dis, COL_TI_BLACK, GRID_X, GRID_Y)
            # charToCells("B", False, 0, 8,
            #             dis, COL_TI_BLACK, GRID_X, GRID_Y)
            # textToCells("test sentence", True, 0, 16,
            #             dis, COL_TI_BLACK, GRID_X, GRID_Y)
            #
            # t.draw(dis, COL_TI_BLACK, GRID_X, GRID_Y)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    root = App()
    root.main()