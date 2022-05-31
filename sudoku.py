from charles import Population, Individual
from data import very_easy, easy, moderate, hard
from selection import fps, tournament, ranking
from mutation import swap_mutation, inversion_mutation
from crossover import pmx_co, cycle_co

pop = Population(
    size=500,
    replacement=False,
    optim="max",
    puzzle=very_easy
)

pop.evolve(
    gens=100,
    select=ranking,
    crossover=cycle_co,
    mutate=swap_mutation,
    co_p=0.9,
    mu_p=0.3,
    elitism=True)
