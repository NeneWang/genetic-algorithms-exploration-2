from deap import tools
from deap import algorithms
import pprint
import random

AGGRESIVE = "AGGRESIVE"
COOPERATIVE = "COOPERATIVE"



def determineStrategyWithMajority(individual):
    """
    The strategy is determined by the majority of the genes.
    - if majorty(gen) == 0 => COOPERATE
    - else DEFECT
    """
    count1 = sum([1 for i in individual if i == 1])
    count0 = sum([1 for i in individual if i == 0])
    if count1 > count0:
        return AGGRESIVE
    else:
        return COOPERATIVE

def determineStrategyWithDominantRecessive(individual, limit=2):
    """
    The strategy is determine as:
    
    G | 1 | 0
    --|---|---
    1 | A | C
    0 | C | C
    
    """
    
    count1 = sum([1 for i in individual[:limit] if i == 1])
    if count1 <= 0:
        return AGGRESIVE
    else:
        return COOPERATIVE

    

def gambiteval(ind1strategy, ind2strategy, both_coop=2, both_defect_winner=1, mixed_coop=0, mixed_defect=3):
    """
    Fitness is evaluated in this case when two individuals face each other.
    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoZTbudsbpcG_COpZ-JYNcwpFwVOXz8OyawhO6Vw-7&s
    """
    
    
    if ind1strategy == COOPERATIVE and ind2strategy == AGGRESIVE:
        return (mixed_coop, mixed_defect)
    elif ind1strategy == AGGRESIVE and ind2strategy == COOPERATIVE:
        return (mixed_defect, mixed_coop)
    elif ind1strategy == COOPERATIVE and ind2strategy == COOPERATIVE:
        return (both_coop, both_coop)
    elif ind1strategy == AGGRESIVE and ind2strategy == AGGRESIVE:
        # return (0, 0)
        # 50% chance of winning or losing.
        return (random.choice([(both_defect_winner, 0), (0, both_defect_winner), (0, 0)]))
    else:
        raise ValueError("Invalid Strategy")
    
def prisonDilemmaEval(ind1strategy, ind2strategy, both_coop=2, both_defect_winner=1, mixed_coop=0, mixed_defect=3):
    """
    Fitness is evaluated in this case when two individuals face each other.
    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoZTbudsbpcG_COpZ-JYNcwpFwVOXz8OyawhO6Vw-7&s
    """
    if ind1strategy == COOPERATIVE and ind2strategy == AGGRESIVE:
        return (mixed_coop, mixed_defect)
    elif ind1strategy == AGGRESIVE and ind2strategy == COOPERATIVE:
        return (mixed_defect, mixed_coop)
    elif ind1strategy == COOPERATIVE and ind2strategy == COOPERATIVE:
        return (both_coop, both_coop)
    elif ind1strategy == AGGRESIVE and ind2strategy == AGGRESIVE:
        return (both_defect_winner, both_defect_winner)
    else:
        raise ValueError("Invalid Strategy")


def evalTournamentGambit(individuals, toolbox, defaultEncounterEval=gambiteval):
    """

    - Make it so that they ALL have to face at least once someone (so it has to be a pair of individuals. if they cant find food, they are not selected (no cases could be random))

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :returns: A list of offspirngs NOT the selected individuals.

    """
    
    if (hasattr(toolbox, "encounterEval")):
        encounterEval = toolbox.encounterEval
    else:
        encounterEval = defaultEncounterEval
    chosen = []
    # randomize individuals
    random.shuffle(individuals)
    # print(f"Individuals at start : {len(individuals)}")

    for i in range(0, len(individuals), 2):
        if i + 1 >= len(individuals):
            break
        
        individual1 = individuals[i]
        individual2 = individuals[i+1]
        
        strategyInd1 = toolbox.determine_strategy(individual1)
        strategyInd2 = toolbox.determine_strategy(individual2)

        # fitnessInd1Inc, fitnessInd2Inc = gambiteval(strategyInd1, strategyInd2)
        fitnessInd1Inc, fitnessInd2Inc = encounterEval(strategyInd1, strategyInd2)
        # print(f"Individual1: {individual1}: {strategyInd1} - Individual2: {individual2}: {strategyInd2} - Fitness1: {fitnessInd1Inc} - Fitness2: {fitnessInd2Inc}")

        # Increase the fitness of the individuals.
        individual1.fitness.values = (fitnessInd1Inc,)
        individual2.fitness.values = (fitnessInd2Inc,)

        
        # Add all the individuals evaluated to the population to have offspring.
        chosen.extend([individual1, individual2])

    return chosen


def evalAccumulatedTournmanetGambit(individuals, toolbox, k=100, defaultEncounterEval=gambiteval):
    """
    Creates k * len(individuals) tournaments (an individual will have k encounters each)
    - Returns the count of indiividuals, with their corrected fitness values.
    - Will prioritize the `encounterEval` strategy defined in the toolbox.
    """
    
    
    if hasattr(toolbox, "settings"):
        settingsDict = toolbox.settings()
        k = settingsDict["encounters_per_lifetime"]
    
    # Increase or reduce the fitness of the individuals, depending on the strategy.
    for tournament_round in range(k):
        random.shuffle(individuals)
        
        # Ensrue that they have fair encounters.
        for i in range(0, len(individuals), 2):
            if i + 1 >= len(individuals):
                break
            
            individual1 = individuals[i]
            individual2 = individuals[i+1]
            
            strategyInd1 = toolbox.determine_strategy(individual1)
            strategyInd2 = toolbox.determine_strategy(individual2)

            fitnessInd1Inc, fitnessInd2Inc = toolbox.encounterEval(strategyInd1, strategyInd2)
            originalFitnessInd1 = individual1.fitness.values[0]
            originalFitnessInd2 = individual2.fitness.values[0]
            
            
            individual1.fitness.values = (originalFitnessInd1 + fitnessInd1Inc,)
            individual2.fitness.values = (originalFitnessInd2 + fitnessInd2Inc,)
    
    return individuals
    
    
def selLiteralToFitness(individuals):
    """
    Selects parents mating cases proprtional to the fitnesses value literally
    """
    chosen = []
    for i in range(len(individuals)):
        individual = individuals[i]
        for fitnessIdx in range(int(individual.fitness.values[0])):
            chosen.append(individual)
            
    random.shuffle(chosen)
    return chosen
    
def selRankedPaired(individuals, k=5, toolbox=None):
    """
    Use fitness to rank half of the individuals as female (no requirement to select.)
    Allows more resources to the top members k, is the times an gambit torunament is played. to balance.
    
    scores are added as a pair.
    
    resources allows as follows:
    
    a score of 3*k+ will allow 3 repetitions of the individual.
    a score of 2*k  will allow 2 repetitions of the individual.
    a score of 1*k  will allow 1 repetitions of the individual.
    no score will  not allow any repetitions of the individual.
    
    """
    chosen = []
    if hasattr(toolbox, "settings"):
        settingsDict = toolbox.settings()
        k = settingsDict["encounters_per_lifetime"]
    
    # Sort the individuals by fitness.
    individuals = sorted(individuals, key=lambda x: x.fitness.values[0], reverse=True)
    
        
    # Allow more repetitions for the top ranked individuals.
    for i in range(0, len(individuals), 2):
        if i + 1 >= len(individuals):
            break
        individual1 = individuals[i]
        individual2 = individuals[i+1]
        pair_score = individual1.fitness.values[0] + individual2.fitness.values[0]
        
        repeat = 0
        if pair_score > 3*k:
            repeat = 5
        else:
            repeat = int(pair_score//k)
        
        for _ in range(repeat):
            chosen.append(individual1)
            chosen.append(individual2)
    return chosen

def selWithRankedPopulationCurved(individuals,toolbox=None, k=5):
    """
    Prioritizes reproduction of the top individuals.
    As population approaches the limit, the skipping of individuals is more likely.
    They have higher change
    """
    # Sort the individuals by fitness.
    chosen = []
    population_limit=10000
    
    if hasattr(toolbox, "settings"):
        settingsDict = toolbox.settings()
        population_limit = settingsDict["population_limit"]
        k = settingsDict["encounters_per_lifetime"]
    
    individuals = sorted(individuals, key=lambda x: x.fitness.values[0], reverse=True)
    # print(f"Individuals: {len(individuals)}")
    # print("Example", individuals[0].fitness.values[0])
    
    for i in range(0, len(individuals), 2):
        if i + 1 >= len(individuals):
            break
        
        
        individual1 = individuals[i]
        individual2 = individuals[i+1]
        pair_score = individual1.fitness.values[0] + individual2.fitness.values[0]
        
        repeat = 0
        if pair_score > 3*k:
            repeat = 5
        else:
            repeat = int(pair_score//k)
        
        for _ in range(repeat):
            chosen.append(individual1)
            chosen.append(individual2)
    # print(f"Chosen: {len(chosen)}")
    return chosen

def simpleVarAnd(population, toolbox, cxpb, mutpb):
    """
    Then applies the crossover in pairs with random members of the population.
    The order of the population is important, 0, 1 will be a pair, 2, 3 will be a pair, etc.

    """
    # Randomize population order to select random parents.
    offspring = population
    
    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):# 1, 3, 5, ... (Always has one before.)
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i]) # Run the assigned mate operation. And since it returns a pair, it should be assigned to a pair.
            del offspring[i - 1].fitness.values, offspring[i].fitness.values # Delete the fitness values of the offspring. (To be recalculated later)
        
    for i in range(len(offspring)): # 0, 1, 2, 3, ...
        if random.random() < mutpb: # If the random number is less than the mutation probability.
            offspring[i], = toolbox.mutate(offspring[i]) # Run the assigned mutate operation.
            del offspring[i].fitness.values # Delete the fitness values of the offspring. (To be recalculated later)

    return offspring


def eaGambit(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__,  population_limit = 1000, curvePopulation=True, limit_strategy="LIMIT_TOP"):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that:
    
    - Supports faceoff (gambit) between the population different strategies.
    - No initial evaluation of the population is done. (as they are calculated at the faceoff)
    
    Stats Support:
    - User can add stats to the algorithm to monitor the evolution of the population.
    - The stats are updated in each generation. (and recorded in the logbook)
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'population', 'coop_pop', 'defect_pop', 'sample_coop_genes', 'sample_defect_genes'] 


    
    coop_pop = 0
    defect_pop = 0
    
    for ind in population:
        if toolbox.determine_strategy(ind) == COOPERATIVE:
            coop_pop += 1
        else:
            defect_pop += 1
    logbook.record(gen=0, population=len(population), coop_pop=coop_pop, defect_pop=defect_pop)
    
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        if len(population) >= population_limit and not curvePopulation:
            break
        for ind in population:
            ind.fitness.values = (0,)
            
        
        # Select the next generation individuals
        # print('Population before tournamentSelection: ', len(population))
        toolbox.evaluate(population, toolbox=toolbox)
        
        # print(f"Offspring after tournamentSelection: {len(offspring)}")
        population = toolbox.select(population)
        
        if(curvePopulation):
            if limit_strategy=="LIMIT_TOP":
                population = population[:population_limit]
            elif limit_strategy=="INCREASING_DIFFICULTY":
                chosen = []
                for i in range(0, len(population)):
                        
                    if len(chosen) >= population_limit:
                        # print(f" Broken population limit: {len(chosen)}")
                        break
                    skip_chance = 1 - (len(chosen) / population_limit)
                    # Skip chance increases as the population approaches the limit.
                    if random.random() > skip_chance:
                        # print(f"Skipped at skip chance: {skip_chance} f{random.random()}")
                        continue
                    chosen.append(population[i])
                population = chosen
        # Vary the pool of individuals
        offspring = simpleVarAnd(population, toolbox, cxpb, mutpb)
        
        # print(f"Offspring after fitreproduceVarAnd: {len(offspring)}")

        # Replace the current population by the offspring
        population[:] = offspring
        
        coop_pop = 0
        defect_pop = 0
        
        sample_coop_genes = ""
        sample_defect_genes = ""
        
        for ind in population:
            if toolbox.determine_strategy(ind) == COOPERATIVE:
                coop_pop += 1
                # join list into string
                sample_coop_genes = ''.join([str(i) for i in ind])
            else:
                defect_pop += 1
                sample_defect_genes =  ''.join([str(i) for i in ind])

        # Append the current generation statistics to the logbook
        logbook.record(gen=gen, population=len(population), coop_pop=coop_pop, defect_pop=defect_pop, sample_coop_genes=sample_coop_genes, sample_defect_genes=sample_defect_genes)
        if verbose:
            print(logbook.stream)

    return population, logbook




class OPTIONS:
    AGGRESIVE = "AGGRESIVE"
    COOPERATIVE = "COOPERATIVE"
    
    INCREASING_DIFFICULTY = "INCREASING_DIFFICULTY"
    LIMIT_TOP = "LIMIT_TOP"
    PRISON_DILEMA_EVAL = "prisonDilemmaEval"
    GAMBIT_EVAL = "gambiteval"
    
    determineStrategyWithDominantRecessive = determineStrategyWithDominantRecessive
    determineStrategyWithMajority = determineStrategyWithMajority
    
    gambiteval = gambiteval
    prisonDilemmaEval = prisonDilemmaEval
    evalTournamentGambit = evalTournamentGambit
    evalAccumulatedTournmanetGambit = evalAccumulatedTournmanetGambit
    
    selRankedPaired = selRankedPaired
    selWithRankedPopulationCurved = selWithRankedPopulationCurved
    selLiteralToFitness = selLiteralToFitness
    selWithRankedPopulationCurved = selWithRankedPopulationCurved
    
    determineStrategyWithDominantRecessive = determineStrategyWithDominantRecessive
    determineStrategyWithMajority = determineStrategyWithMajority
    

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
