from deap import base
from deap import creator
from deap import tools

import random
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import elitism

def run_himmelblau_optimization_genetic(DIMENSIONS = 2, BOUND_LOW = -5.0, BOUND_UP = 5.0, POPULATION_SIZE = 300, P_CROSSOVER = 0.9, P_MUTATION = 0.5, MAX_GENERATIONS = 300, HALL_OF_FAME_SIZE = 30, CROWDING_FACTOR = 20.0, RANDOM_SEED = 42):

    random.seed(RANDOM_SEED)

    toolbox = base.Toolbox()

    # define a single objective, minimizing fitness strategy:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    # create the Individual class based on list:
    creator.create("Individual", list, fitness=creator.FitnessMin)


    # helper function for creating random float numbers uniformaly distributed within a given range [low, up]
    # it assumes that the range is the same for every dimension
    def randomFloat(low, up):
        return [random.uniform(a, b) for a, b in zip([low] * DIMENSIONS, [up] * DIMENSIONS)]

    # create an operator that randomly returns a float in the desired range and dimension:
    toolbox.register("attr_float", randomFloat, BOUND_LOW, BOUND_UP)

    # create the individual operator to fill up an Individual instance:
    toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.attr_float)

    # create the population operator to generate a list of individuals:
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


    # Himmelblau function as the given individual's fitness:
    def himmelblau(individual):
        x = individual[0]
        y = individual[1]
        f = (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2
        return f,  # return a tuple

    toolbox.register("evaluate", himmelblau)

    # genetic operators:
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=CROWDING_FACTOR)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=CROWDING_FACTOR, indpb=1.0/DIMENSIONS)


    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with elitism:
    population, logbook = elitism.eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                                ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print info for best solution found:
    best = hof.items[0]
    print("-- Best Individual = ", best)
    print("-- Best Fitness = ", best.fitness.values[0])

    print("- Best solutions are:")
    for i in range(HALL_OF_FAME_SIZE):
        print(i, ": ", hof.items[i].fitness.values[0], " -> ", hof.items[i])


    # extract statistics:
    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    return minFitnessValues, meanFitnessValues, population


minFitnessValues_42, meanFitnessValues_42, population_42 = run_himmelblau_optimization_genetic(RANDOM_SEED=42)

# random with seed 13 for comparison:
minFitnessValues_13, meanFitnessValues_13, population_13 = run_himmelblau_optimization_genetic(RANDOM_SEED=13)

# plot statistics:


# plot solution locations on x-y plane:
plt.figure(1)
globalMinima = [[3.0, 2.0], [-2.805118, 3.131312], [-3.779310, -3.283186], [3.584458, -1.848126]]
plt.scatter(*zip(*globalMinima), marker='X', color='red', zorder=1)
plt.scatter(*zip(*population_42), marker='.', color='blue', zorder=0)
plt.scatter(*zip(*population_13), marker='.', color='green', zorder=0)

# Legends and labels.
plt.legend(['Global Minima', '42', '13'])


plt.figure(2)
sns.set_style("whitegrid")
plt.plot(minFitnessValues_42, color='red')
plt.plot(meanFitnessValues_42, color='green')
plt.plot(minFitnessValues_13, color='blue')

plt.xlabel('Generation')
plt.ylabel('Min / Average Fitness')
plt.title('Min and Average fitness over Generations')

# Legends.
plt.legend(['42', '42 Mean', '13'])

plt.show()


