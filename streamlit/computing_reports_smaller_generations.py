import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pprint
from deap import base, creator, tools, algorithms
import pandas as pd
from modules.knapsack_tools import ITEMS_KNAPSACK, MAX_CAPACITY, apply_tournament, KnapsackProblem, run_knapsack_tournament




populations = [50]
generations = [x for x in range(10, 40, 1)]
crossover_probabilities = [x/10 for x in range(1, 5, 2)]
mutation_probabilities = [x/10 for x in range(1, 5, 2)]

selection_methods = [
    tools.selTournament, 
    tools.selRoulette, 
    tools.selBest
]
k = [x for x in range(1, 3)]
experiments_arr = []


for selection_method in selection_methods:
    for population in populations:
        for generation in generations:
            for crossover_probability in crossover_probabilities:
                for mutation_probability in mutation_probabilities:
                    for k_value in k:
                        toolbox = base.Toolbox()
                        selection_strategy_name = ""
                        if selection_method == tools.selTournament:
                            toolbox.register("select", selection_method, tournsize=k_value)    
                            strategy_name = "Tournament"
                        if selection_method == tools.selBest:
                            toolbox.register("select", tools.selBest)
                            strategy_name = "Best"
                        if selection_method == tools.selRoulette:
                            toolbox.register("select", tools.selRoulette, k=k_value)
                            strategy_name = "Roulette"
    
                        resuls = run_knapsack_tournament(toolbox, population, crossover_probability, mutation_probability, generation)
                        logbook = resuls['logbook']
                        max_found_at = logbook.select('max_found_at')[-1]
                        end_mean_fitness_population = logbook.select('avg')[-1]
                        end_max_fitness = logbook.select('max')[-1]
                        
                        
                        experiments = {
                            'max_found_at_generation': max_found_at, 
                            'end_mean_fitness_population': end_mean_fitness_population, 
                            'end_max_fitness': end_max_fitness,
                            "initial_population": population,
                            "max_generation": generation,
                            "crossover_probability": crossover_probability,
                            "mutation_probability": mutation_probability,
                            "selection_method": selection_method,
                            "selection_strategy_name": strategy_name,
                            "k_value": k_value
                            
                        }
                        pprint.pprint(experiments)
                        experiments_arr.append(experiments)
df_experiments = pd.DataFrame(experiments_arr)
df_experiments.to_csv('reports/knapsack__smallerexperiments.csv')
df_experiments.head(40)  
    
    
    