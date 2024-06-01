import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from deap import base, creator, tools, algorithms
import pandas as pd
from modules.knapsack_tools import ITEMS_KNAPSACK, MAX_CAPACITY, apply_torunament, KnapsackProblem, run_knapsack_tournament


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

# Add link https://hackmd.io/@n_1IfOpxQPSjyRrn5yedJw/r1fbS-RZC#Definitions
st.write("Definitions can be found at [HackMD](https://hackmd.io/@n_1IfOpxQPSjyRrn5yedJw/r1fbS-RZC#Definitions)")

population_size = st.slider('Initial Population', min_value=10, max_value=200, value=50, step=10)
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

df_solution = pd.DataFrame()
show_solution = st.toggle("Show Best Solution")

if st.button('Run Knapsack Solution'):
    print("Running Knapsack", MAX_CAPACITY)
    results = run_knapsack_tournament(population_size, crossover_prob, mutation_prob, max_generations, ITEMS_KNAPSACK, MAX_CAPACITY)
    best_solution = results['best_solution']
    best_value = results['best_value']
    logbook = results['logbook']
    knapsack: KnapsackProblem = results['knapsack']
    
    
    
    st.write("Best Solution: ", str(best_solution))
    st.write("Best Value: ", best_value)
    df_solution = knapsack.get_solution_table(best_solution)
    
  
    if show_solution:
        if not df_solution.empty:
            st.dataframe(df_solution)
    