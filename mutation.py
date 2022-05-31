import random
from random import choice, uniform, random, sample
import numpy as np


def swap_mutation(ind, puzzle):
    """Swap mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    individual= ind.representation
    dict_val = []

    for i in range(9):
        for j in range(9):
            if puzzle[i, j] != 0:
                dict_val.append([i, j])

    dict_val = np.array(dict_val)

    # loop to check we don't modify an input value of the sudoku
    input_val = 1
    while input_val != 0:
        input_val = 0

        # Get two mutation points
        mut_points = sample(range(len(individual)), 3)

        for i in range(len(dict_val)):
            j = 0
            if (dict_val[i][j] == mut_points[j]) & (dict_val[i][j + 1] == mut_points[j + 1]):
                input_val = 1

        for i in range(len(dict_val)):
            j = 0
            if (dict_val[i][j] == mut_points[j]) & (dict_val[i][j + 1] == mut_points[j+2]):
                input_val = 1
        if mut_points[1] == mut_points[2]:
            input_val = 1

    # Swap them if they are not input values:
    individual[mut_points[0], mut_points[1]], individual[mut_points[0], mut_points[2]] = individual[mut_points[0], mut_points[2]], individual[mut_points[0], mut_points[1]]

    return individual


def inversion_mutation(individual, puzzle_in):
    """Inversion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # utilizing the solution key of the individuals
    inds = individual.solution_key

    # getting the number of rows in which to repeat the proccess
    inds_rows = len(inds)

    # looping the CYCLE over all the rows of the solution key, giving each row a 60% change of mutating

    for row in range(inds_rows):
        if random() < (0.6):
            # Position of the start and end of substring
            mut_points = sample(range(len(inds[row])), 2)
            # This method assumes that the second point is after (on the right of) the first one
            # Sort the list
            mut_points.sort()
            # Invert for the mutation
            inds[row][mut_points[0]:mut_points[1]] = inds[row][mut_points[0]:mut_points[1]][::-1]

    ir = np.array(puzzle_in)

    #generating a representation based on the solution key
    for i in range(9):
        temp = []
        k = 0
        for j in range(9):
            if (puzzle_in[i][j] == 0):
                ir[i][j] = inds[i][k]
                k = k + 1

    return ir