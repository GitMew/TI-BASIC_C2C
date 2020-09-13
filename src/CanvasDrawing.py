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


# Hierarchy of drawing functions
def coordToCell(x: int, y: int,
                dis, colour, grid_x: int=GRID_X, grid_y: int=GRID_Y):
    pygame.draw.rect(dis, colour, [x*grid_x, y*grid_y, grid_x, grid_y])


def matrixToCells(matrix: list, topleft_x: int, topleft_y: int,
                  dis, colour, grid_x: int=GRID_X, grid_y: int=GRID_Y):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x]:
                coordToCell(topleft_x + x, topleft_y + y, dis, colour, grid_x, grid_y)


def charToCells(character: str, lower: bool, topleft_x: int, topleft_y: int,
                dis, colour, grid_x: int=GRID_X, grid_y: int=GRID_Y):
    matrixToCells(
        (UPPER_MATRICES if not lower else LOWER_MATRICES).get(character, [[]]), topleft_x, topleft_y,
        dis, colour, grid_x, grid_y
    )


def textToCells(text: str, lower: bool, topleft_x: int, topleft_y: int,
                dis, colour, grid_x: int=GRID_X, grid_y: int=GRID_Y):
    offset = 0
    for c in text:
        charToCells(c, lower, topleft_x + offset, topleft_y,
                    dis, colour, grid_x, grid_y)
        offset += len((UPPER_MATRICES if not lower else LOWER_MATRICES).get(c,[[]])[0]) + 1
