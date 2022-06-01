from csp_algorithms import backtracking_search
from draw_kenken import draw
from itertools import product, permutations
from functools import reduce
from random import random, shuffle, randint, choice
from time import time
import pygame




def operation(operator):
    # This Function is used to determine the operation that each cage is contained
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '÷':
        return lambda a, b: a / b
    elif operator == '*':
        return lambda a, b: a * b
    else:
        return None
        
def adjacent(cell, other):
    # This function checks that two coordinates cells are adjacent or not
    # ex: cell =(2,1) --> x_1 = 2 , y_1 = 1

    x_1, y_1 = cell 
    x_2, y_2 = other
    difference_x, difference_y = x_1 - x_2, y_1 - y_2
    return (difference_x == 0 and abs(difference_y) == 1) or (difference_y == 0 and abs(difference_x) == 1)

def generate_kenken(board_size):
# To generate a random kenken puzzle of specific size (Given)

# Creation of the board
    kenken_board = [[((i + j) % board_size) + 1 for i in range(board_size)] for j in range(board_size)]

# To shuffle rows only
    for _ in range(board_size):
        shuffle(kenken_board)

# To shuffle columns only
    for col1 in range(board_size):
        for col2 in range(board_size):
            if random() > 0.5:
                for row in range(board_size):
                    kenken_board[row][col1], kenken_board[row][col2] = kenken_board[row][col2], kenken_board[row][col1]

# Divide the kenken_board from list of lists to cell to cell ex: (1,1):1 ==> cell 1 col.1 row.1 and the value = 1
# j--> columns , i--> rows
# kenken_board ==> Dict
    kenken_board = {(j + 1, i + 1): kenken_board[i][j] for i in range(board_size) for j in range(board_size)} 

    # To  return the keys only in list
    uncaged = sorted(kenken_board.keys(), key=lambda var: var[1])

    cages = []
    while uncaged:

        cages.append([])

        # Random var to choose operation
        cage_size = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        cages[-1].append(cell) 

        # cage_size ==> means that the size of the operation
        for _ in range(cage_size - 1):

            # Get the adjacents of the cell  
            adjacent_cells = [another_cell for another_cell in uncaged if adjacent(cell, another_cell)]
            cell = choice(adjacent_cells) if adjacent_cells else None
            if not cell:
                break
            uncaged.remove(cell)
            cages[-1].append(cell)

        cage_size = len(cages[-1])
        if cage_size == 1:
            # the freebie cell (No Operation) "# means No operation"
            cell = cages[-1][0]
            cages[-1] = ((cell, ), '#', kenken_board[cell])
            continue
        elif cage_size == 2:
            first_cell, second_cell = cages[-1][0], cages[-1][1]
            # To check that the division operation willnot get a remainder 
            if kenken_board[first_cell] / kenken_board[second_cell] > 0 and not kenken_board[first_cell] % kenken_board[second_cell]:
                operator = "÷" 
            else:
                operator = "-" 
        else:
            operator = choice("+*")

        # To get the result of an operation
        target_no = reduce(operation(operator), [kenken_board[cell] for cell in cages[-1]])

        # put the cages in this format ==> (((X1, Y1), ..., (XN, YN)), <operation>, <target_no>)
        cages[-1] = (tuple(cages[-1]), operator, abs(int(target_no)))

    return cages

def conflicting(A, a, B, b):
# To check that there is no conflicting for any two variables that that every member of variable A
    # which shares the same row or column with a member of variable B must not have the same value

    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if ((mA[0] == mB[0]) != (mA[1] == mB[1])) and ma == mb:
                return True

    return False

def satisfy(values, operation, target_no):
    # To check if the the numbers applied is specifed the target_no by applying the operation
    # Using permutations to determine the satisfiability of an operation
    for value in permutations(values):
        if reduce(operation, value) == target_no:
            return True

    return False

def kenken_domains(board_size, cages):

    domains = {}
    for cage in cages:
        members, operator, target_no = cage
        domains[members] = list(product(range(1, board_size + 1), repeat=len(members)))
        qualifies = lambda values: not conflicting(members, values, members, values) and satisfy(values, operation(operator), target_no)
        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def get_neighbors_cages(cages):

    neighbors = {}
    for members, _, _ in cages:
        neighbors[members] = []

    for A, _, _ in cages:
        for B, _, _ in cages:
            if A != B and B not in neighbors[A]:
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors

