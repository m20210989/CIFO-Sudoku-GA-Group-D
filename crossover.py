import random
from random import choice, uniform, random, sample
import numpy as np


def pmx_co(P1, P2, puzzle_in):
    # Implementation of partially matched/mapped crossover.
    # Args:
    #    P1 (Individual): First parent for crossover.
    #    P2 (Individual): Second parent for crossover.
    # Returns:
    #    Individuals: Two offspring, resulting from the crossover.

    #########################################################
    # function to generate each single row of a single offspring
    def PMX(x, y):
        co_points = sample(range(len(x)), 2)
        co_points.sort()

        o = [None] * len(x)

        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

        #points in window of x that are outside or y
        z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])

        for digit in z:
            index = y.index(x[y.index(digit)]) #for a given digit, it cheks what digit of x is in the equivalent index, and checks where this digit is indexed in y
            while o[index] is not None: #checks whether the position found above is not filled in o, if yes it then re-assigns the digit
                temp = index
                index = y.index(x[temp])
            o[index] = digit

        while None in o:
            index = o.index(None)
            o[index] = y[index]

        return o

    ##########################################################

    # utilizing the solution key of the individuals
    p1 = P1.solution_key
    p2 = P2.solution_key

    # getting the number of rows in which to repeat the process
    p1_rows = len(p1)

    # creating lists of offspring
    o1 = []
    o2 = []
    # looping the pmx over all the rows of the puzzle
    for row in range(p1_rows):
        co_points = sample(range(len(p1[row])), 2)
        co_points.sort()

        o1.append(PMX(p1[row], p2[row]))
        o2.append(PMX(p2[row], p1[row]))

    #creating the representation from the generated solution keys
    or1 = np.array(puzzle_in)

    for i in range(9):
        k = 0
        temp = []
        for j in range(9):
            if (puzzle_in[i][j] == 0):
                or1[i][j] = o1[i][k]
                k = k + 1

    or2 = np.array(puzzle_in)

    for i in range(9):
        temp = []
        k = 0
        for j in range(9):
            if (puzzle_in[i][j] == 0):
                or2[i][j] = o2[i][k]
                k = k + 1

    return o1, or1, o2, or2


def cycle_co(P1, P2, puzzle_in):
    # Implementation cycle crossover.
    # Args:
    #    P1 (Individual): First parent for crossover.
    #    P2 (Individual): Second parent for crossover.
    # Returns:
    #    Individuals: Two offspring, resulting from the crossover.

    #########################################################
    # function to generate each single row of a single offspring
    def CYCLE(rp1, rp2):
        # Args:
        #    rp1 (Individual): First parent's row for crossover.
        #    rp2 (Individual): Second parent's row for crossover.

        # Returns:
        #    rows: Two rows, one for each offspring, resulting from the crossover.

        # Offspring row placeholders - None values make it easy to debug for errors
        rowoffspring1 = [None] * len(rp1)
        rowoffspring2 = [None] * len(rp2)
        # While there are still None values in the row, get the first index of
        # None and start a "cycle" according to the cycle crossover method
        while None in rowoffspring1:
            index = rowoffspring1.index(None)

            val1 = rp1[index]
            val2 = rp2[index]

            while val1 != val2:
                rowoffspring1[index] = rp1[index]
                rowoffspring2[index] = rp2[index]
                val2 = rp2[index]
                index = rp1.index(val2)

            for element in rowoffspring1:
                if element is None:
                    index = rowoffspring1.index(None)
                    if rowoffspring1[index] is None:
                        rowoffspring1[index] = rp2[index]
                        rowoffspring2[index] = rp1[index]

        return rowoffspring1, rowoffspring2

    ##########################################################

    # utilizing the solution key of the individuals
    p1 = P1.solution_key
    p2 = P2.solution_key

    # getting the number of rows in which to repeat the proccess
    p1_rows = len(p1)

    # creating lists of offspring
    o1 = []
    o2 = []
    # looping the CYCLE over all the rows of the puzzle
    for row in range(p1_rows):
        rowo1, rowo2 = CYCLE(p1[row], p2[row])
        o1.append(rowo1)
        o2.append(rowo2)

    ###creating the corresponding representations of the offspring based on the obtained solution keys

    or1 = np.array(puzzle_in)

    for i in range(9):
        k = 0
        temp = []
        for j in range(9):
            if (puzzle_in[i][j] == 0):
                or1[i][j] = o1[i][k]
                k = k + 1

    or2 = np.array(puzzle_in)

    for i in range(9):
        temp = []
        k = 0
        for j in range(9):
            if (puzzle_in[i][j] == 0):
                or2[i][j] = o2[i][k]
                k = k + 1

    return o1, or1, o2, or2