from itertools import product, permutations
from functools import reduce
from random import random, shuffle, randint, choice



class kenken_generator():
    
    def __init__(self, size=3):
        self.size = size
        self.cages = []

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

    def generate_kenken(self):
    # To generate a random kenken puzzle of specific size (Given)

    # Creation of the board
        kenken_board = [[((i + j) % self.size) + 1 for i in range(self.size)] for j in range(self.size)]

    # To shuffle rows only
        for _ in range(self.size):
            shuffle(kenken_board)

    # To shuffle columns only
        for col1 in range(self.size):
            for col2 in range(self.size):
                if random() > 0.5:
                    for row in range(self.size):
                        kenken_board[row][col1], kenken_board[row][col2] = kenken_board[row][col2], kenken_board[row][col1]

    # Divide the kenken_board from list of lists to cell to cell ex: (1,1):1 ==> cell 1 col.1 row.1 and the value = 1
    # j--> columns , i--> rows
    # kenken_board ==> Dict
        kenken_board = {(j + 1, i + 1): kenken_board[i][j] for i in range(self.size) for j in range(self.size)} 

        # To  return the keys only in list
        uncaged = sorted(kenken_board.keys(), key=lambda var: var[1])

        # cages = []
        while uncaged:

            self.cages.append([])

            # Random var to choose operation
            cage_size = randint(1, 4)
            cell = uncaged[0]
            uncaged.remove(cell)
            self.cages[-1].append(cell) 

            # cage_size ==> means that the size of the operation
            for _ in range(cage_size - 1):

                # Get the adjacents of the cell  
                adjacent_cells = [another_cell for another_cell in uncaged if kenken_generator.adjacent(cell, another_cell)]
                cell = choice(adjacent_cells) if adjacent_cells else None
                if not cell:
                    break
                uncaged.remove(cell)
                self.cages[-1].append(cell)

            #we get again cage_size bec we may not get cells in cage with the random no we generated but may be less than it
            cage_size = len(self.cages[-1])
            if cage_size == 1:
                # the freebie cell (No Operation) "# means No operation"
                cell = self.cages[-1][0]
                self.cages[-1] = ((cell, ), '#', kenken_board[cell])
                continue
            elif cage_size == 2:
                first_cell, second_cell = self.cages[-1][0], self.cages[-1][1]
                # To check that the division operation willnot get a remainder 
                if kenken_board[first_cell] / kenken_board[second_cell] > 0 and not kenken_board[first_cell] % kenken_board[second_cell]:
                    operator = "÷" 
                else:
                    operator = "-" 
            else:
                operator = choice("+*")

            # To get the result of an operation
            target_no = reduce(kenken_generator.operation(operator), [kenken_board[cell] for cell in self.cages[-1]])

            # put the cages in this format ==> (((X1, Y1), ..., (XN, YN)), <operation>, <target_no>)
            self.cages[-1] = (tuple(self.cages[-1]), operator, abs(int(target_no)))

        return self.cages


class kenken_data():
    def __init__(self):
        self.domains = {}
        self.neighbors = {}
        self.variables =[]

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

    def kenken_domains(self,board_size, cages):

        # domains = {}
        for cage in cages:
            members, operator, target_no = cage
            # product('ab', range(3)) --> ('a',0) ('a',1) ('a',2) ('b',0) ('b',1) ('b',2) different permutaions and combinations
            self.domains[members] = list(product(range(1, board_size + 1), repeat=len(members)))
            qualifies = lambda values: not kenken_data.conflicting(members, values, members, values) and kenken_data.satisfy(values, kenken_generator.operation(operator), target_no)
            self.domains[members] = list(filter(qualifies, self.domains[members]))

        return self.domains

    def get_neighbors_cages(self,cages):

        # neighbors = {}
        for members, _, _ in cages:
            self.neighbors[members] = []

        for A, _, _ in cages:
            for B, _, _ in cages:
                if A != B and B not in self.neighbors[A]:
                    if kenken_data.conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                        self.neighbors[A].append(B)
                        self.neighbors[B].append(A)

        return self.neighbors

    def get_variables(self,cages):
        self.variables = [members for members, _, _ in cages]
        return self.variables


#tracing
# cages = generate_kenken(4)
# domains=kenken_domains(4,cages)
# neighbors=get_neighbors_cages(cages)
# print("cages: ",cages)
# print("domains: ",domains)
# print("neighbors: ",neighbors)
# p= list(product(range(1, 4 + 1), repeat=3))
# print("p: ",p)
# print("no of p= ",len(p))
# p:  [(1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4), 
# (1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 2, 4), (1, 3, 1),
#  (1, 3, 2), (1, 3, 3), (1, 3, 4), (1, 4, 1), (1, 4, 2),
#  (1, 4, 3), (1, 4, 4), (2, 1, 1), (2, 1, 2), (2, 1, 3), 
# (2, 1, 4), (2, 2, 1), (2, 2, 2), (2, 2, 3), (2, 2, 4),
#  (2, 3, 1), (2, 3, 2), (2, 3, 3), (2, 3, 4), (2, 4, 1),
#  (2, 4, 2), (2, 4, 3), (2, 4, 4), (3, 1, 1), (3, 1, 2),
#  (3, 1, 3), (3, 1, 4), (3, 2, 1), (3, 2, 2), (3, 2, 3), 
# (3, 2, 4), (3, 3, 1), (3, 3, 2), (3, 3, 3), (3, 3, 4),
#  (3, 4, 1), (3, 4, 2), (3, 4, 3), (3, 4, 4), (4, 1, 1), 
# (4, 1, 2), (4, 1, 3), (4, 1, 4), (4, 2, 1), (4, 2, 2), (4, 2, 3),
#  (4, 2, 4), (4, 3, 1), (4, 3, 2), (4, 3, 3), (4, 3, 4), (4, 4, 1),
#  (4, 4, 2), (4, 4, 3), (4,4, 4)]

# cages:  [(((1, 1), (2, 1)), '-', 1),
#  (((3, 1), (4, 1), (4, 2), (3, 2)), '+', 8), 
# (((1, 2), (2, 2), (2, 3)), '*', 24),
#  (((1, 3), (1, 4), (2, 4)), '*', 2),
#  (((3, 3), (4, 3), (4, 4), (3, 4)), '*', 72)]

# domains:  {((1, 1), (2, 1)): [(1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)],
#  ((3, 1), (4, 1), (4, 2), (3, 2)): [(1, 2, 1, 4), (1, 2, 3, 2), (1, 3, 1, 3), (1, 4, 1, 2), (2, 1, 2, 3), (2, 1, 4, 1), (2, 3, 2, 1), (3, 1, 3, 1), (3, 2, 1, 2), (4, 1, 2, 1)], 
# ((1, 2), (2, 2), (2, 3)): [(2, 3, 4), (2, 4, 3), (3, 2, 4), (3, 4, 2), (4, 2, 3), (4, 3, 2)],
#  ((1, 3), (1, 4), (2, 4)): [(1, 2, 1)], 
# ((3, 3), (4, 3), (4, 4), (3, 4)): [(2, 3, 4, 3), (3, 2, 3, 4), (3, 4, 3, 2), (4, 3, 2, 3)]}

# neighbors:  {((1, 1), (2, 1)): [((3, 1), (4, 1), (4, 2), (3, 2)), ((1, 2), (2, 2), (2, 3)), ((1, 3), (1, 4), (2, 4))],
#  ((3, 1), (4, 1), (4, 2), (3, 2)): [((1, 1), (2, 1)), ((1, 2), (2, 2), (2, 3)), ((3, 3), (4, 3), (4, 4), (3, 4))],
#  ((1, 2), (2, 2), (2, 3)): [((1, 1), (2, 1)), ((3, 1), (4, 1), (4, 2), (3, 2)), ((1, 3), (1, 4), (2, 4)), ((3, 3), (4, 3), (4, 4), (3, 4))], 
# ((1, 3), (1, 4), (2, 4)): [((1, 1), (2, 1)), ((1, 2), (2, 2), (2, 3)), ((3, 3), (4, 3), (4, 4), (3, 4))],
#  ((3, 3), (4, 3), (4, 4), (3, 4)): [((3, 1), (4, 1), (4, 2), (3, 2)), ((1, 2), (2, 2), (2, 3)), ((1, 3), (1, 4), (2, 4))]}