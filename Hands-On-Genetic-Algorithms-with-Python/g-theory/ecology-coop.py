import matplotlib.pyplot as plt
import seaborn as sns

from gambit_algorithm import gambitGeneticSimulation
from deap_expansion import OPTIONS

INITIAL_COOPERATIE_RATE = .8
START_WITH_PURE_STRATEGIES = True

# Genetic Algorithm constants:
POPULATION_SIZE = 100
P_CROSSOVER = 0.2  # probability for crossover
P_MUTATION = 0.01   # probability for mutating an offspring individual
MAX_GENERATIONS = 50
POPULATION_LIMIT = 50000 # Simulation will stop if the population exceeds this limit.
GEN_SIZE = 5
FLIPBIT_MUTATION_PROB = 1.0/GEN_SIZE

# set the random seed:
RANDOM_SEED = 42

REPRODUCTION_LOGIC = "FITNESS_PROPORTIONAL_TORUNAMENT"



precurated_cases = {
    "be1.tribal_hunters": {
        "lore": "BE1 Base Case Tribal Hunters",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL
    },
     "be1b.tribal_hunters": {
        "lore": "BE1 Base Case Tribal Hunters",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .9,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL
    },
     "be1c.tribal_hunters": {
        "lore": "BE1 variant. Whit a more rewarding setting for coolaboration.",
        "both_coop": 4,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL
    },
     "be2.nuclear_hunters": {
        "lore": "BE2 Making aggressiveness nuclear",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 0,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL
    },
     "be2b.nuclear_hunters": {
        "lore": "BE2 variant | Where being cooperative is many times more rewarding.",
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 0,
        "POPULATION_SIZE": 6,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 800000,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness
    },
     "be3.limiting_population": {
        "lore": "BE2 variant | Where we create an limit to the max amount of individuals in the population.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 150,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness
    },
     "be3b.limiting_population": {
        "lore": "BE3 variant. cooperating now is rewarded by 4 offsprings each instead.",
        "both_coop": 6,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 150,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness
    },
     "be3c.limiting_population": {
        "lore": "BE3 variant. Limiting using a curved survivval. Where as the population grows, the chances of survival decreases. Using the POPULATION_LIMIT as an asymptote.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 150,
        "P_CROSSOVER": 0.0,
        "P_MUTATION": 0.0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY
    },
     "be4.mutation_crossover": {
        "lore": "BE3 variant. With Mutation and Crossover enabled.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 500000,
        "P_CROSSOVER": 0,
        "P_MUTATION": 0,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
    },
     "be4b.mutation_crossover": {
        "lore": "BE4 variant. With a Increasing Difficulty Limit Strategy.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 500000,
        "P_CROSSOVER": 0,
        "P_MUTATION": 0.1,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY
    },
     "be4c.mutation_crossover": {
        "lore": "BE4 variant. With Nuclear disagreements.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 0,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 500000,
        "P_CROSSOVER": 0,
        "P_MUTATION": 0.1,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY
    },
     "be4d.mutation_crossover": {
        "lore": "BE4 variant. With Nuclear disagreements.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 0,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 500000,
        "P_CROSSOVER": 0.5,
        "P_MUTATION": 0.1,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY
    },
     "be5a.recessive_dominant": {
        "lore": "BE4 variant. With Mutation and Crossover enabled.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 500000,
        "P_CROSSOVER": 0.5,
        "P_MUTATION": 0.1,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY,
        "determine_strategy": OPTIONS.determineStrategyWithMajority
    },
     "be5acontrol.recessive_dominant": {
        "lore": "BE4 variant. With Mutation and Crossover enabled.",
        "both_coop": 2,
        "mixed_coop": 0,
        "mixed_defect": 3,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 500000,
        "P_CROSSOVER": 0.5,
        "P_MUTATION": 0.1,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "select": OPTIONS.selLiteralToFitness,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY
    },
     
     
     
     
     "be5b.control_limited": {
        "lore": "BE4 variant. With Mutation and Crossover enabled.",
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 10,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 300000,
        "P_CROSSOVER": 0.1,
        "P_MUTATION": 0.05,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "limit_strategy": OPTIONS.LIMIT_TOP,
        "select": OPTIONS.selLiteralToFitness,
        "determine_strategy": OPTIONS.determineStrategyWithMajority
    },
     "be5b.recessive_dominant_limited": {
        "lore": "BE4 variant. With Mutation and Crossover enabled.",
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 10,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 300000,
        "P_CROSSOVER": 0.1,
        "P_MUTATION": 0.05,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "limit_strategy": OPTIONS.LIMIT_TOP,
        "select": OPTIONS.selLiteralToFitness,
        "determine_strategy": OPTIONS.determineStrategyWithDominantRecessive
    },
     
     "be5b.control_limited_increasing": {
        "lore": "BE4 variant. With Mutation and Crossover enabled.",
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 10,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 300000,
        "P_CROSSOVER": 0.1,
        "P_MUTATION": 0.05,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY,
        "select": OPTIONS.selLiteralToFitness,
        "determine_strategy": OPTIONS.determineStrategyWithMajority
    },
     "be5b.recessive_dominant_increasing": {
        "lore": "BE4 variant. With Mutation and Crossover enabled.",
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 10,
        "both_defect_winner": 1,
        "POPULATION_SIZE": 100,
        "INITIAL_COOPERATIE_RATE": .5,
        "POPULATION_LIMIT": 300000,
        "P_CROSSOVER": 0.1,
        "P_MUTATION": 0.05,
        "RANDOMIZE_SEED": False,
        "encounterEval": OPTIONS.PRISON_DILEMA_EVAL,
        "limit_strategy": OPTIONS.INCREASING_DIFFICULTY,
        "select": OPTIONS.selLiteralToFitness,
        "determine_strategy": OPTIONS.determineStrategyWithDominantRecessive
    },
}



# population, coop_pop, defect_pop = gambitGeneticSimulation(POPULATION_SIZE=POPULATION_SIZE, P_CROSSOVER=P_CROSSOVER, P_MUTATION=P_MUTATION, FLIPBIT_MUTATION_PROB=FLIPBIT_MUTATION_PROB, MAX_GENERATIONS=MAX_GENERATIONS, POPULATION_LIMIT=POPULATION_LIMIT, GEN_SIZE=GEN_SIZE, RANDOM_SEED=RANDOM_SEED)

case = "be5b.recessive_dominant_limited"
case = "be5b.control_limited_increasing"

population, coop_pop, defect_pop = gambitGeneticSimulation(**precurated_cases[case])

# plot statistics:
sns.set_style("whitegrid")
plt.plot(population, color='blue')
plt.plot(coop_pop, color='green')
plt.plot(defect_pop, color='red')
plt.xlabel('Generation')
plt.ylabel('Population')
plt.legend(['Total', 'Cooperative', 'Aggressive'])

title = f"Population over Generations | {case}"
plt.title(title)
plt.show()

