import random
from random import choice, uniform, random, sample
import numpy as np
from operator import attrgetter
from copy import deepcopy
from matplotlib import pyplot as plt


class Individual:
    def __init__(
            self,
            puzzle_in=None,
            representation=None,
            solution_key=None,
            replacement=False,
            fitness=None
    ):
        if representation is None:
            list_poss = []
            list_numbers = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            dummy_1 = []
            dummy_2 = []
            dummy_3 = []
            sudoku = np.array(puzzle_in)

            puzzle = np.array(puzzle_in)
            solution = []

            for i in range(9):
                for j in range(9):
                    col = set(puzzle[i][:])
                    row = set(puzzle[:, j])
                    dummy_1 = (col | row)
                    if (i < 3):
                        if (j < 3):
                            block = np.unique(puzzle[0:0 + 3, 0:0 + 3])
                        elif (j < 6):
                            block = np.unique(puzzle[0:0 + 3, 3:3 + 3])
                        else:
                            block = np.unique(puzzle[0:0 + 3, 6:6 + 3])
                    elif (i < 6):
                        if (j < 3):
                            block = np.unique(puzzle[3:3 + 3, 0:+3])
                        elif (j < 6):
                            block = np.unique(puzzle[3:3 + 3, 3:+3])
                        else:
                            block = np.unique(puzzle[3:3 + 3, 6:+3])
                    else:
                        if (j < 3):
                            block = np.unique(puzzle[6:6 + 3, 0:+3])
                        elif (j < 6):
                            block = np.unique(puzzle[6:6 + 3, 3:+3])
                        else:
                            block = np.unique(puzzle[6:6 + 3, 6:+3])
                    block = set(block)
                    dummy_2 = (dummy_1 | block)
                    dummy_3 = (dummy_2 ^ list_numbers)
                    list_poss.append(dummy_3)
            ### the puzzle will be solved without forcing the rows to have solely unique digits###
            if replacement is True:
                k = 0
                for i in range(9):
                    temp = []
                    for j in range(9):
                        if (puzzle[i][j] == 0):
                            sudoku[i][j] = choice(list(list_poss[k]))
                            temp.append(sudoku[i][j])
                            k = k + 1
                    solution.append(temp)
            ### the puzzle will be solved forcing each row to contain all digits 1-9###
            elif replacement is False:

                for i in range(9):
                    row_dig = set(sudoku[i]) - set([0])
                    while len(row_dig) < 9:
                        sudoku[i] = puzzle[i]
                        for j in range(9):
                            if (puzzle[i][j] == 0):
                                possible_digits = list(set(list(list_poss[9 * i + j])) - set(sudoku[i]))
                                if len(possible_digits) == 0:
                                    break
                                else:
                                    sudoku[i][j] = choice(possible_digits)
                        row_dig = set(sudoku[i]) - set([0])

            self.representation = sudoku
            ###generating the solution key for the computed representation###
            solution = []
            for i in range(9):
                temp = []
                for j in range(9):
                    if (puzzle_in[i][j] == 0):
                        temp.append(self.representation[i][j])
                solution.append(temp)

            self.solution_key = solution
        #### option to create an individual from a realized representation instead of generating a new solution ###
        else:
            self.representation = representation
            solution = []
            for i in range(9):
                temp = []
                for j in range(9):
                    if (puzzle_in[i][j] == 0):
                        temp.append(self.representation[i][j])
                solution.append(temp)

            self.solution_key = solution

        self.fitness = self.get_fitness()

    def get_fitness(self):

        # '''Calculates the fitness function based on the unique value for the rows, columns and blocks.
        # This is a maximization problem so the solution is 243'''
        fitness_row = 0
        fitness_col = 0
        fitness_block = 0

        for i in range(9):
            fitness_row += len(set(self.representation[i][:]))
            fitness_col += len(set(self.representation[:, i]))

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                unique = np.unique(self.representation[i:i + 3, j:j + 3])
                fitness_block += len(unique)

        fitness_total = fitness_row + fitness_col + fitness_block
        return fitness_total

        # This is a minimization problem so the best solution is 0

        # fitness_row = 0
        # fitness_col = 0
        # fitness_block = 0

        #   for i in range(9):
        #       fitness_row += 9-(len(set(self.representation[i][:])))
        #       fitness_col += 9-(len(set(self.representation[:, i])))

        #       for i in range(0, 9, 3):
        #           for j in range(0, 9, 3):
        #               unique = np.unique(self.representation[i:i + 3, j:j + 3])
        #               fitness_block += 9-(len(unique))

        # fitness_total = fitness_row + fitness_col + fitness_block
        # return fitness_total

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value


# def __repr__(self):
#    return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        for _ in range(size):
            self.individuals.append(
                Individual(
                    replacement=kwargs["replacement"],
                    puzzle_in=kwargs["puzzle"]
                )
            )
        self.puzzle = kwargs["puzzle"]

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):
        best_fitnesses=[]
        for gen in range(gens):
            new_pop = []

            if elitism == True:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    o1, or1, o2, or2 = crossover(parent1, parent2, self.puzzle)
                    offspring1 = Individual(representation=or1,puzzle_in=self.puzzle)
                    offspring2 = Individual(representation=or2,puzzle_in=self.puzzle)

                else:
                    offspring1, offspring2 = parent1, parent2

                # Mutation
                if random() < mu_p:
                    roffspring1 = mutate(offspring1, self.puzzle)
                    offspring1 = Individual(representation=roffspring1,puzzle_in=self.puzzle)
                if random() < mu_p:
                    roffspring2 = mutate(offspring2, self.puzzle)
                    offspring1 = Individual(representation=roffspring2, puzzle_in=self.puzzle)
                new_pop.append(offspring1)
                if len(new_pop) < self.size:
                    new_pop.append(offspring2)

            if elitism == True:
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    least = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(least))
                new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness")).fitness}')
                best_fitnesses.append(max(self, key=attrgetter("fitness")))
            elif self.optim == "min":
                print(f'Best Individual: {min(self, key=attrgetter("fitness")).fitness}')
                best_fitnesses.append(min(self, key=attrgetter("fitness")))
        best_fitness_values=[]
        for i in best_fitnesses:
            best_fitness_values.append(i.fitness)

        plt.plot(best_fitness_values)
        plt.ylabel('Fitness')
        plt.xlabel('Generation')
        print(best_fitnesses[-1].representation)
        plt.show()

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"