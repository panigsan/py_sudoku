# -*- coding: UTF-8 -*-
# Mouse-Keyboard interaction
from pymouse import PyMouseEvent
from pymouse import PyMouse
from pykeyboard import PyKeyboard
# Image stuff
import pyscreenshot as ImageGrab
from PIL import Image
import pytesseract
# Others
from time import sleep
import os

import sudoku


clear = lambda: os.system("clear")

class Clicker(PyMouseEvent):

    clicks_counter = 0
    positions = {
            0: "up_left",
            1: "down_right"
            }

    clicks = {
            0: (-1,-1),
            1: (-1,-1),
            }

    def __init__(self):
        PyMouseEvent.__init__(self)
        self.print_message()

    def print_message(self):
        print "Click for '%s'" % self.positions[self.clicks_counter]

    def click(self, x, y, button, press):
        if not press:
            return

        self.clicks[self.clicks_counter] = (x,y)

        self.clicks_counter += 1

        if self.clicks_counter >= 2:
            self.stop()
            return

        self.print_message()

def ask_for_positions():
    clicker = Clicker()
    clicker.run()
    return clicker.clicks

def take_screenshot(positions):
    bbox = (positions[0][0],positions[0][1],positions[1][0],positions[1][1])
    im = ImageGrab.grab(bbox)
    return im

# (NOT USED) replace the given colors with white and return the new image
def clean_image(image, colors_to_exclude=[(102,102,150,255),(220,220,237,255)]):
    image = image.convert("RGBA")

    pixdata = image.load()

    for y in xrange(image.size[1]):
        for x in xrange(image.size[0]):
            if pixdata[x, y] in colors_to_exclude:
                pixdata[x, y] = (255, 255, 255, 255)
    image.save("temp.png")

    return Image.open("temp.png")

# Given the image of the board, return a board obj
# Throws a ValueError if there's a problem
def get_board_from_image(im):
    width, height = im.size

    cell_width = width / 9
    cell_height = height / 9

    board = sudoku.Board()

    for i in range(0,9):
        for j in range(0,9):
            # crop the cell with a small margin to remove the borders
            cell_image = im.crop((
                int((j+0.1)*cell_width),
                int((i+0.1)*cell_height),
                int((j+0.1)*cell_width+cell_width*0.8),
                int((i+0.1)*cell_height+cell_height*0.8)))

            try:
                board.values[j][i] = cell_to_number(cell_image)
            except ValueError:
                raise

    return board

# Given the image of a cell, return the digit value
# Throw a ValueError if it cannot parse the image
def cell_to_number(cell):
    text = pytesseract.image_to_string(cell,config="-psm 6")

    if text == "":
        return 0

    try:
        return int(text)
    except ValueError:
        #print "%r is not a number" % text
        raise

# Fill the board in the screen
def fill_board(start_board, solution_board, x,y,width,height):
    cell_width = width / 9
    cell_height = height / 9

    mouse = PyMouse()
    keyboard = PyKeyboard()

    for i in range(0,9):
        for j in range(0,9):
            # insert only empty cell
            if start_board.values[j][i] == 0:
                sleep(0.1)
                mouse.click(x + cell_width*(j+0.5), y+cell_height*(i+0.5))
                sleep(0.01)
                keyboard.tap_key(str(solution_board.values[j][i]))




