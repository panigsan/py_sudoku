# -*- coding: UTF-8 -*-
import random
from colors import *
import os
from time import sleep

clear = lambda: os.system("clear")

# print constants
table_values = {
"up_left" : u'\u250F',
"up_right" : u'\u2513',
"down_left" : u'\u2517',
"down_right" : u'\u251B',
"horizontal"  : u'\u2501',
"vertical" : u'\u2503',
"up_down" : u'\u2533',
"down_up" : u'\u253B',
"left_right" : u'\u2523',
"right_left" : u'\u252B',
"center" : u'\u254B'}

class Board(object):

    values = None

    def __init__(self):
        self.init_board()

    def init_board(self):
        # initialize the board
        self.values = [[0 for i in range(0,9)] for i in range(0,9)]

    def get_next_valid_boards(self, x, y):
        boards = []
        for number in self.get_valid_numbers(x,y):
            # create a new baord
            temp = Board()

            # copy the values from the source
            temp.values = [row[:] for row in self.values]

            temp.values[x][y] = number

            boards.append(temp)

        return boards

    # Return a list of valid numbers in the given position
    def get_valid_numbers(self, x, y):
        valid_numbers = []

        if self.values[x][y]!=0:
            return valid_numbers

        for i in range(1,10):
            if self.is_valid_number(x,y,i):
                valid_numbers.append(i)

        return valid_numbers

    # Return True if it's a valid position for the given number
    def is_valid_number(self, x, y, number):

        # check if it's a valid number
        if not (1 <= number <= 9):
            return False

        # check if it's a valid position
        if not (0 <= x <= 8 and 0 <= y <= 8):
            return False

        # check the line
        for j in range(0,9):
            if self.values[j][y]==number:
                return False

        # check the column
        for i in range(0,9):
             if self.values[x][i]==number:
                 return False

        block_x = x / 3
        block_y = y / 3

        block_x *= 3
        block_y *= 3

        for i in range(block_y, block_y + 3):
            for j in range(block_x, block_x + 3):
                if i != y and j != x:
                    if self.values[j][i]==number:
                        return False



        return True

    def get_number_of_elements(self):
        count = 0
        for i in range(0,9):
            for j in range(0,9):
                count += 1 if self.values[j][i]!=0 else 0
        return count

def is_valid_board(board):
    for i in range(0,9):
        for j in range(0,9):
            if not board.is_valid_number(j,i,board.values[j][i]):
                return False
    return True

def generate_full_board():
    start_board = Board()
    return complete_board(start_board)

def complete_board(board, x=0, y=0):
    #clear()
    #print board.to_string()
    #sleep(0.001)
    if board.get_number_of_elements() == 81:
        return board

    next_x = x-1
    next_y = y

    # search for a new empty position
    while True:
        next_x += 1
        if next_x==9:
            next_x = 0
            next_y += 1
        if next_y==9:
            next_y=0

        if board.values[next_x][next_y] == 0:
            break

    for next_board in board.get_next_valid_boards(next_x,next_y):
        temp = complete_board(next_board, next_x, next_y)
        if temp != None:
            return temp

    return None

def print_board(start_board, solution_board=Board()):

        text = '\n'

        # first line
        text += table_values["up_left"] + table_values["horizontal"]*3
        text += (table_values["up_down"] + table_values["horizontal"]*3)*2
        text += table_values["up_right"] + "\n"

        # first 3 lines
        for i in range(0,3):
            # left bound
            text += table_values["vertical"]

            for j in range(0,3):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"]

            for j in range(3,6):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"]

            for j in range(6,9):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"] + "\n"

        text += table_values["left_right"] + table_values["horizontal"]*3
        text += (table_values["center"] + table_values["horizontal"]*3)*2
        text += table_values["right_left"] + "\n"

        # second 3 lines
        for i in range(3,6):
            # left bound
            text += table_values["vertical"]

            for j in range(0,3):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"]

            for j in range(3,6):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"]

            for j in range(6,9):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"] + "\n"

        text += table_values["left_right"] + table_values["horizontal"]*3
        text += (table_values["center"] + table_values["horizontal"]*3)*2
        text += table_values["right_left"] + "\n"

        # third 3 lines
        for i in range(6,9):
            # left bound
            text += table_values["vertical"]

            for j in range(0,3):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"]

            for j in range(3,6):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"]

            for j in range(6,9):
                text += _get_colored_cell(start_board, solution_board, j, i)
            text += table_values["vertical"] + "\n"


        # last line
        text += table_values["down_left"] + table_values["horizontal"]*3
        text += (table_values["down_up"] + table_values["horizontal"]*3)*2
        text += table_values["down_right"] + "\n"

        return text

def _get_colored_cell(start_board, solution_board, j, i):
    if start_board.values[j][i] != 0:
        return color(str(start_board.values[j][i]), "bold", "fg_green")
    elif solution_board.values[j][i] != 0:
        return color(str(solution_board.values[j][i]), "fg_light_blue")
    else:
        return " "



