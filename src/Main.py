"""
TI-BASIC Canvas to Command Conversion Tool

Author: T. Bauwens
Date: 2020-09-12
"""
from src.DrawObjects import *

# ToDo:
#   - Since the combination "dis, colour, grid_x, grid_y" is so popular, I think we should make it a separate class,
#     and associate such an object with the app itself.

def rectContainsCoord(rect, pos):  # rect is of the form: ( (TL_x,TL_y) , (width,height) )
    return rect[0][0] <= pos[0] <= rect[0][0] + rect[1][0] and rect[0][1] <= pos[1] <= rect[0][1] + rect[1][1]


class App:
    def __init__(self):
        self.canvas_objects = []  # Last in the list is topmost layer on-canvas.
        self.quit = False

    def addCanvasObject(self, obj: Draw_Object):
        self.canvas_objects.append(obj)

    def eventHandler(self, event):
        print(event)
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_obj = None
            for obj in self.canvas_objects:
                obj.deselect()
                if rectContainsCoord(obj.getHitbox(GRID_X, GRID_Y), event.pos):
                    selected_obj = obj
            if selected_obj is not None:
                selected_obj.select()

    def drawObjects(self, dis, colour, grid_x, grid_y):
        for obj in self.canvas_objects:
            obj.draw(dis, colour, grid_x, grid_y)

    def main(self):
        pygame.init()
        dis = pygame.display.set_mode((GRID_X*SCREEN_WIDTH, GRID_Y*SCREEN_HEIGHT))
        pygame.display.set_caption("TI-84+ Emulator")

        t = Draw_Text(20, 30, "Hello world", is_lower=False)
        self.addCanvasObject(t)

        # i = 0
        while not self.quit:
            dis.fill(COL_TI_GREY)
            self.drawObjects(dis, COL_TI_BLACK, GRID_X, GRID_Y)

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