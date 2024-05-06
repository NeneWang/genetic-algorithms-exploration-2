from deap import base
from deap import creator
from deap import tools
import random
import matplotlib.pyplot as plt
import seaborn as sns

from deap_expansion import eaGambit, gambiteval, prisonDilemmaEval, evalTournamentGambit, evalAccumulatedTournmanetGambit, selRankedPaired, selLiteralToFitness, selWithRankedPopulationCurved

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

supported_reproduction_algorithm = [
    {
        "name": "FITNESS_PROPORTIONAL",
        "inspiration": "A simple exmaple to introduce the idea of mating and mutation.",
        "description": "The count of offspring of an individual is proportional to its fitness resulting from the evaluation function.",
        "algorithm": eaGambit
    },
    {
        "name": "FITNESS_ROULETTE",
        "inspiration": "In human nature, when a hunter goes to 'hunt' depending on the cooperation with who else is also hunting, might be more successful, when coming back to the tribe, if succesfull, increasing the chances of mating.",
        "description": "After multiple encounters, the fitness is aggregated from each encounter. A roulette wheel is used to select the parent, where those with larger fitness are more likely to be chosen."
    },
    {
        "name": "ASEXUAL_STRUCTURE",
        "inspiration": "Inspired from plants that decide to collaborate or not with other plants. Since plants cant move, they only have one interaction with it's environment. Depending on the interaction they might have more resources to reproduce.",
        "description": "The offspring is a clone of the parent with x chance of some mutation times. The parent is selected by a tournament selection."
    },
    {
        "name": "MONOGOID_STRUCTURE",
        "inspiration": "Some humans societies attempt to have something like this. most commonly seen in birds and other animals",
        "description": "Assigns half of the population as female, and make male indiividuals compete repetitevely at tournaments to earn resources. the more resources the the more offspring.",
    },
    {
        "name": "POLYGOID_STRUCTURE",
        "inspiration": "Inspired from the animal kingdom, where a male is more attractive if it has more resources.",
        "description": "Assigns half of the population as female, rank male indiividuals by resources, gathered, and make them compete repetitevely at tournaments to earn resources. the more resources the the more offspring.",
    }
]


def gambitGeneticSimulation(both_coop=2, both_defect_winner=1, mixed_coop=0, mixed_defect=3, INITIAL_COOPERATIE_RATE=INITIAL_COOPERATIE_RATE,
                            START_WITH_PURE_STRATEGIES=START_WITH_PURE_STRATEGIES, RANDOMIZE_SEED=True, POPULATION_SIZE=POPULATION_SIZE, P_CROSSOVER=P_CROSSOVER, P_MUTATION=P_MUTATION, FLIPBIT_MUTATION_PROB=FLIPBIT_MUTATION_PROB, MAX_GENERATIONS=MAX_GENERATIONS, POPULATION_LIMIT=POPULATION_LIMIT, 
                            GEN_SIZE=GEN_SIZE, RANDOM_SEED=RANDOM_SEED, lore="", encounterEval="prisonDilemmaEval", evaluate=evalTournamentGambit, select=selLiteralToFitness, curvePopulation=True, limit_strategy="LIMIT_TOP") -> tuple:
    
    if RANDOMIZE_SEED:
        RANDOM_SEED = random.randint(0, 10000)
    else:
        random.seed(RANDOM_SEED)
    print(f"Random Seed {RANDOM_SEED}")

    if INITIAL_COOPERATIE_RATE > 1 or INITIAL_COOPERATIE_RATE < 0:
        raise ValueError("Initial Cooperation Rate should be between 0 and 1.")
    

    toolbox = base.Toolbox()
    # create an operator that randomly returns 0 or 1:
    toolbox.register("zeroOrOne", random.randint, 0, 1)
    # define a single objective, maximizing fitness strategy:
    creator.create("FitnessMax", base.Fitness, weights=(1.0,)) # You dont really need it, cause there is no fitness calculation.
    # create the Individual class based on list:
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # create the individual operator to fill up an Individual instance:

    # Single-point crossover:
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=FLIPBIT_MUTATION_PROB)
    evalMap = {
        "prisonDilemmaEval": prisonDilemmaEval,
        "gambiteval": gambiteval
    }
    toolbox.register("encounterEval", evalMap[encounterEval], both_coop=both_coop, both_defect_winner=both_defect_winner, mixed_coop=mixed_coop, mixed_defect=mixed_defect)
    toolbox.register("evaluate", evaluate )
    
    
    def returnSharedSettings():
        return {
            "population_limit": POPULATION_LIMIT,
            "encounters_per_lifetime": 5
        }
    
    toolbox.register("settings", returnSharedSettings)

    population = []
    if START_WITH_PURE_STRATEGIES:
        
        def returnOnes():
            return 1

        def returnZeros():
            return 0
        
        toolbox.register("pure_ones", returnOnes)
        toolbox.register("pure_zeros", returnZeros)
        toolbox.register("cooperatorCreator", tools.initRepeat, creator.Individual, toolbox.pure_zeros, GEN_SIZE)
        
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.cooperatorCreator)
        population.extend(toolbox.populationCreator(n=int(POPULATION_SIZE * INITIAL_COOPERATIE_RATE)))
        
        
        # Create the population of defectors:
        toolbox.register("defectorCooperator", tools.initRepeat, creator.Individual, toolbox.pure_ones, GEN_SIZE)
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.defectorCooperator)
        population.extend(toolbox.populationCreator(n=int(POPULATION_SIZE * (1-INITIAL_COOPERATIE_RATE))))
                          
        toolbox.register("select", select)
        
        print(f"Created population with {len(population)} individuals. ")
    else:      
        toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, GEN_SIZE)
        # create the population operator to generate a list of individuals:
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)
        population = toolbox.populationCreator(n=POPULATION_SIZE)



    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook =  eaGambit(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                            ngen=MAX_GENERATIONS, verbose=True, population_limit=POPULATION_LIMIT, curvePopulation=curvePopulation,
                                            limit_strategy=limit_strategy)


    # extract statistics:
    # logbook.header = ['gen', 'population', 'coop_pop', 'defect_pop'] 
    population, coop_pop, defect_pop = logbook.select("population", "coop_pop", "defect_pop")
    return population, coop_pop, defect_pop




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
        "encounterEval": "prisonDilemmaEval"
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
        "encounterEval": "prisonDilemmaEval"
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
        "encounterEval": "prisonDilemmaEval"
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
        "encounterEval": "prisonDilemmaEval"
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness,
        "limit_strategy": "INCREASING_DIFFICULTY"
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness,
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness,
        "limit_strategy": "INCREASING_DIFFICULTY"
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
        "encounterEval": "prisonDilemmaEval",
        "select": selLiteralToFitness,
        "limit_strategy": "INCREASING_DIFFICULTY"
    },
}



# population, coop_pop, defect_pop = gambitGeneticSimulation(POPULATION_SIZE=POPULATION_SIZE, P_CROSSOVER=P_CROSSOVER, P_MUTATION=P_MUTATION, FLIPBIT_MUTATION_PROB=FLIPBIT_MUTATION_PROB, MAX_GENERATIONS=MAX_GENERATIONS, POPULATION_LIMIT=POPULATION_LIMIT, GEN_SIZE=GEN_SIZE, RANDOM_SEED=RANDOM_SEED)

case = "be4c.mutation_crossover"
population, coop_pop, defect_pop = gambitGeneticSimulation(**precurated_cases[case])

# plot statistics:
sns.set_style("whitegrid")
plt.plot(population, color='blue')
plt.plot(coop_pop, color='green')
plt.plot(defect_pop, color='red')
plt.xlabel('Generation')
plt.ylabel('Population')
plt.legend(['Total', 'Cooperative', 'Aggressive'])
plt.title('Population over Generations')
plt.show()

