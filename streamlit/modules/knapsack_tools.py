
import matplotlib.pyplot as plt
import seaborn as sns
from deap import base, creator, tools, algorithms
import pandas as pd
import numpy as np


ITEMS_KNAPSACK = [
    ("map", 9, 150), ("compass", 13, 35), ("water", 153, 200), ("sandwich", 50, 160),
    ("glucose", 15, 60), ("tin", 68, 45), ("banana", 27, 60), ("apple", 39, 40),
    ("cheese", 23, 30), ("beer", 52, 10), ("suntan cream", 11, 70), ("camera", 32, 30),
    ("t-shirt", 24, 15), ("trousers", 48, 10), ("umbrella", 73, 40),
    ("waterproof trousers", 42, 70), ("waterproof overclothes", 43, 75),
    ("note-case", 22, 80), ("sunglasses", 7, 20), ("towel", 18, 12), ("socks", 4, 50),
    ("book", 30, 10)
]


    

MAX_CAPACITY = 400

class KnapsackProblem:
    def __init__(self, items=ITEMS_KNAPSACK, maxCapacity=MAX_CAPACITY):
        self.items = items
        self.maxCapacity = maxCapacity
        print("Initalized with capacity: ", maxCapacity)
        self.best_solution = []
        self.best_value = 0

    def __len__(self):
        return len(self.items)

    def getValue(self, zeroOneList, verbose=False):
        totalWeight = totalValue = 0
        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                totalWeight += zeroOneList[i] * weight
                totalValue += zeroOneList[i] * value
        
        if totalValue > self.best_value and totalWeight <= self.maxCapacity:
            self.best_value = totalValue
            self.best_solution = zeroOneList
            if verbose:
                print("New Best Solution: ", self.best_value, "Weight: ", totalWeight)
                self.get_solution_table(self.best_solution)
                
        # print("Total Weight: ", totalWeight, "Total Value: ", totalValue)
        return totalValue if totalWeight <= self.maxCapacity else 0

    def get_solution_table(self, zeroOneList) -> pd.DataFrame:
        """
        Print using st.write the selected items in the list, while ignoring items that will cause the accumulating weight to exceed the maximum weight
        """
        solution_items = []
        total_weight = total_value = 0
        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if total_weight + weight <= self.maxCapacity:
                if zeroOneList[i] > 0:
                    total_weight += weight
                    total_value += value
                    solution_items.append((item, weight, value))
        solution_items.append(("Total", total_weight, total_value))
        df_solution = pd.DataFrame(solution_items, columns=["Name", "Weight", "Utility"])
        return df_solution
        

def apply_tournament(toolbox, tournsize=3):
    toolbox.register("select", tools.selTournament, tournsize=tournsize)
    return toolbox

def run_knapsack_tournament(toolbox, population_size, crossover_prob, mutation_prob, max_generations, items=ITEMS_KNAPSACK, max_capacity=MAX_CAPACITY, apply_selection=apply_tournament):
    # Move the creation of Knapsack problem instance inside the function
    knapsack = KnapsackProblem(items=items, maxCapacity=max_capacity)

    # Genetic Algorithm constants:
    P_CROSSOVER = crossover_prob
    P_MUTATION = mutation_prob
    MAX_GENERATIONS = max_generations
    HALL_OF_FAME_SIZE = 1
    
    toolbox.register("zeroOrOne", np.random.randint, 0, 2)
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, len(knapsack))
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)
    def knapsackValue(individual):
        return knapsack.getValue(individual),  
    toolbox.register("evaluate", knapsackValue)
    apply_selection(toolbox)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/len(knapsack))

    population = toolbox.populationCreator(n=population_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)
    hof.clear()

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                                ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=False)
    
    # For some reason this is not working
    return {
        "best_solution": knapsack.best_solution,
        "best_value": knapsack.best_value,
        "logbook": logbook,
        "hof": hof,
        "knapsack": knapsack
    }
