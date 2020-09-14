"""
Functions for drawing to the TI-BASIC grid.

Author: T. Bauwens
Date: 2020-09-12
"""
import pygame
from src.LettersToMatrices import *

# Outline of display flow:
#  1. Coordinate code to rectangle draw
#  2. Matrix to coordinates
#  3. Letters to matrices dictionary
#  4. GUI to letters

# CONSTANTS
# Colours
COL_TI_BLACK = (26, 28, 22)
COL_TI_GREY  = (158, 171, 136)
COL_SELECTION = (200, 0, 0)

# Grid cell pixel dimensions
GRID_X = 10
GRID_Y = 10

# Grid cell amounts
SCREEN_WIDTH  = 95
SCREEN_HEIGHT = 63

# FUNCTIONS AND CLASSES
# Grid layer class (because almost all drawing functions need arguments (display, colour, grid_x, grid_y); actually, they can just be methods for a grid, now that I think about it)
class Grid:
    def __init__(self, layer_colour: tuple=COL_TI_BLACK, gridcell_px_x: int=GRID_X, gridcell_px_y: int=GRID_Y,
                 cellcount_x: int=SCREEN_WIDTH, cellcount_y: int=SCREEN_HEIGHT):
        pygame.init()
        self.dis = pygame.display.set_mode((GRID_X * SCREEN_WIDTH, GRID_Y * SCREEN_HEIGHT))
        pygame.display.set_caption("TI-84+ Emulator")

        self.colour = layer_colour

        self.cellcount_x = cellcount_x
        self.cellcount_y = cellcount_y

        self.grid_x = gridcell_px_x
        self.grid_y = gridcell_px_y

    # Hierarchy of drawing functions
    def coordToCell(self, x: int, y: int):
        pygame.draw.rect(self.dis, self.colour, [x*self.grid_x, y*self.grid_y, self.grid_x, self.grid_y])

    def matrixToCells(self, matrix: list, topleft_x: int, topleft_y: int):
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x]:
                    self.coordToCell(topleft_x + x, topleft_y + y)

    def charToCells(self, character: str, lower: bool, topleft_x: int, topleft_y: int):
        self.matrixToCells(
            (UPPER_MATRICES if not lower else LOWER_MATRICES).get(character, [[]]), topleft_x, topleft_y
        )

    def textToCells(self, text: str, lower: bool, topleft_x: int, topleft_y: int):
        offset = 0
        for c in text:
            self.charToCells(c, lower, topleft_x + offset, topleft_y)
            offset += characterWidth(c, lower) + 1
