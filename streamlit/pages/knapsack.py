import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from deap import base, creator, tools, algorithms
import pandas as pd

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
                st.write("New Best Solution: ", self.best_value, "Weight: ", totalWeight)
                st.write("Best Solution: ", str(zeroOneList))
                self.printItems(self.best_solution)
                
        # print("Total Weight: ", totalWeight, "Total Value: ", totalValue)
        return totalValue if totalWeight <= self.maxCapacity else 0

    def printItems(self, zeroOneList):
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
        st.table(df_solution)
        
def apply_torunament(toolbox, tournsize=3):
    toolbox.register("select", tools.selTournament, tournsize=tournsize)
    return toolbox
        
        
def run_knapsack_tournament(population_size, crossover_prob, mutation_prob, max_generations, items=ITEMS_KNAPSACK, max_capacity=MAX_CAPACITY, apply_selection=apply_torunament):
    # Move the creation of Knapsack problem instance inside the function
    knapsack = KnapsackProblem(items=items, maxCapacity=max_capacity)

    # Genetic Algorithm constants:
    P_CROSSOVER = crossover_prob
    P_MUTATION = mutation_prob
    MAX_GENERATIONS = max_generations
    HALL_OF_FAME_SIZE = 1

    toolbox = base.Toolbox()
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
    # best = hof.items[-1]
    
    best = knapsack.best_solution
    st.write(" == Best Ever Individual == ", str(best))
    st.write(" === Best Ever Fitness === ", best.fitness.values[0])
    st.write(" === Last Generation Mean Fitness === ", logbook.select("avg")[-1])

    st.write(" ============== Knapsack Items ============== ")
    knapsack.printItems(best)

    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red', label='Max Fitness')
    plt.plot(meanFitnessValues, color='green', label='Average Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Max and Average fitness over Generations')
    plt.legend()  # Add legend to the plot

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


st.title('Knapsack Problem')

with st.container():
    st.write("The knapsack problem is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.")
    # https://rosettacode.org/wiki/Knapsack_problem/0-1#
    st.write("You can read more about the knapsack problem here: | [Wiki](https://en.wikipedia.org/wiki/Knapsack_problem) | [Rosetta](https://rosettacode.org/wiki/Knapsack_problem/0-1#) |")
    st.write("This is a simple implementation of the knapsack problem using a genetic algorithm.")
st.subheader('Knapsack Settings')

if st.button('Reset Items'):
    for i in range(len(ITEMS_KNAPSACK)):
        ITEMS_KNAPSACK[i] = (ITEMS_KNAPSACK[i][0], ITEMS_KNAPSACK[i][1], ITEMS_KNAPSACK[i][2])
    st.write("Items reset")

# Randomize
if st.button('Randomize Items'):
    for i in range(len(ITEMS_KNAPSACK)):
        ITEMS_KNAPSACK[i] = (ITEMS_KNAPSACK[i][0], np.random.randint(1, 100), np.random.randint(1, 100))
    st.write("Items randomized")
    

# Edit items settings   
st.write(" == Items Settings == ")
df_items = pd.DataFrame(ITEMS_KNAPSACK, columns=["Name", "Weight", "Utility"])
edited_values = st.data_editor(df_items)
try:
    print(list(edited_values.itertuples(index=False, name=None)))
    ITEMS_KNAPSACK = list(edited_values.itertuples(index=False, name=None))
except:
    st.write("Error updating items")
    
# Max Size of the bag
MAX_CAPACITY = st.number_input('Max Capacity', min_value=1, value=400)

    
st.subheader('Genetic Algorithm Settings')
population_size = st.slider('Population Size', min_value=10, max_value=200, value=50, step=10)
crossover_prob = st.slider('Crossover Probability', min_value=0.1, max_value=1.0, value=0.9, step=0.1)
mutation_prob = st.slider('Mutation Probability', min_value=0.01, max_value=0.5, value=0.1, step=0.01)
max_generations = st.slider('Max Generations', min_value=10, max_value=200, value=50, step=10)


st.subheader("Selection Method")
# Radio selection for selection method
selection_method = st.radio("Selection Method", ["Tournament", "Roulette", "Best K", "Stochastic Universal Sampling"])
if selection_method == "Tournament":
    tour_size = st.number_input('Tournament Size', min_value=2, value=3)
    def selection_method(toolbox, tour_size=tour_size):
        toolbox.register("select", tools.selTournament, tournsize=tour_size)
        
        return toolbox
    def selection_method(toolbox, tournsize=3):
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        return toolbox
elif selection_method == "Roulette":
    def selection_method(toolbox):
        toolbox.register("select", tools.selRoulette)
        return toolbox
elif selection_method == "Best K":
    k = st.number_input('K', min_value=1, value=5)
    if k:
        def selection_method(toolbox, k=k):
            toolbox.register("select", tools.selBest, k=k)
            return toolbox
elif selection_method == "Stochastic Universal Sampling":
    k = st.number_input('K', min_value=1, value=5)
    def selection_method(toolbox):
        toolbox.register("select", tools.selStochasticUniversalSampling, k=k)
        return toolbox
    

if st.button('Run Knapsack Solution'):
    print("Running Knapsack", MAX_CAPACITY)
    run_knapsack_tournament(population_size, crossover_prob, mutation_prob, max_generations, ITEMS_KNAPSACK, MAX_CAPACITY)
