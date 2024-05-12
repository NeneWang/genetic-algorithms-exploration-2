from deap import base
from deap import creator
from deap import tools
import random
import matplotlib.pyplot as plt
import seaborn as sns
from deap_expansion import eaGambit, gambiteval, prisonDilemmaEval, evalTournamentGambit, evalAccumulatedTournmanetGambit, selRankedPaired, selLiteralToFitness, selWithRankedPopulationCurved, determineStrategyWithDominantRecessive, determineStrategyWithMajority
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


def gambitGeneticSimulation(both_coop=2, both_defect_winner=1, mixed_coop=0, mixed_defect=3, INITIAL_COOPERATIE_RATE=INITIAL_COOPERATIE_RATE,
                            START_WITH_PURE_STRATEGIES=START_WITH_PURE_STRATEGIES, RANDOMIZE_SEED=True, POPULATION_SIZE=POPULATION_SIZE, P_CROSSOVER=P_CROSSOVER, P_MUTATION=P_MUTATION, FLIPBIT_MUTATION_PROB=FLIPBIT_MUTATION_PROB, MAX_GENERATIONS=MAX_GENERATIONS, POPULATION_LIMIT=POPULATION_LIMIT, 
                            GEN_SIZE=GEN_SIZE, RANDOM_SEED=RANDOM_SEED, lore="", encounterEval=OPTIONS.INCREASING_DIFFICULTY, evaluate=evalTournamentGambit, select=selLiteralToFitness, curvePopulation=True, limit_strategy="LIMIT_TOP", determine_strategy=determineStrategyWithMajority) -> tuple:
    """
    Runs the Gambit Simulation, here the possible tools supported 
    limit_strategy: 'LIMIT_TOP' | 'INCREASING_DIFFICULTY`
    determine_strategy: determineStrategyWithDominantRecessive | determineStrategyWithMajority
    """
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
    toolbox.register("determine_strategy", determine_strategy)

    # Single-point crossover:
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=FLIPBIT_MUTATION_PROB)
    evalMap = {
        OPTIONS.INCREASING_DIFFICULTY: prisonDilemmaEval,
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

