import random
from random import choice, uniform, random, sample
from operator import attrgetter

# #### FSP (or Roulette Wheel Selection)
    # - **Obs**: added code for minimization.

def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual
    elif population.optim == "min":
        # Sum total fitness
        total_fitness = sum([1 / (i.fitness) for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += 1 / individual.fitness

            if position > spin:
                return individual
    else:
        raise Exception("No optimization specified (min or max).")


# Ranking Selection
    # **Obs**: implemented code for both maximization and minimization.

def ranking(population):
    """Ranking selection implementation.

    Args:
        populattion(Population): The population we want to select from.

    Returns:
        Individual: best fitness?
    """
    if population.optim == 'max':
        # sort population according to their fitness value
        sorted_fitnesses = sorted(population, key=attrgetter('fitness'), reverse=False)
        # Sum of fitness - using Gaussian sum
        total_fitness = (len(population) + 1) * len(population) / 2
        ranked_scores = [i/total_fitness for i in range(0, len(population))]
        spin = uniform(0, sum(ranked_scores))
        position = 0
        # Find individual in the position of the spin
        for index, rank in enumerate(ranked_scores):
            position += rank
            if position > spin:
                return sorted_fitnesses[index]
    elif population.optim == 'min':
        # sort population according to their fitness value
        sorted_fitnesses = sorted(population, key=attrgetter('fitness'), reverse=True)
        # Sum of fitness - using Gaussian sum
        total_fitness = (len(population) + 1) * len(population) / 2
        ranked_scores = [i/total_fitness for i in range(0, len(population))]
        spin = uniform(0, sum(ranked_scores))
        position = 0
        # Find individual in the position of the spin
        for index, rank in enumerate(ranked_scores):
            position += rank
            if position > spin:
                return sorted_fitnesses[index]
    else:
        raise Exception("No optimization specified (min or max).")
# Tournament Selection
    # **Obs**: Nothing was modified since the code was fully implemented in class.

def tournament(population, size=10):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]
    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")
