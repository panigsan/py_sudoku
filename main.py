# -*- coding: UTF-8 -*-
import utility
from PIL import Image
import sudoku
from colors import *

# ask for a board until there aren't parse errors
while True:
    # ask for the position of the board on the screen
    clicks = utility.ask_for_positions()

    print success("Points taken")
    print success("Taking a screenshot")

    # take a screenshot of the board
    im = utility.take_screenshot(clicks)

    # get a board from the image
    # it could throw a ValueError exception
    try:
        print success("Parsing the screenshot")
        board = utility.get_board_from_image(im)
        break
    except ValueError:
        print error("Error parsing the board. I need a new screenshot")

print success("Board taken")
#print board.to_string()
print sudoku.print_board(board)

print success("Solving the board")
solution = sudoku.complete_board(board)

print success("Solution")
#print solution.to_string()
print sudoku.print_board(board, solution)

width = clicks[1][0]-clicks[0][0]
height = clicks[1][1]-clicks[0][1]

print success("Filling the board with the solution")
utility.fill_board(board, solution, clicks[0][0],clicks[0][1],width,height)

print success("Done!")
