import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pprint
from deap import base, creator, tools, algorithms
import pandas as pd
from modules.gambit_algorithm import gambitGeneticSimulation
from modules.deap_expansion import OPTIONS
from modules.knapsack_tools import ITEMS_KNAPSACK, MAX_CAPACITY, apply_tournament, KnapsackProblem, run_knapsack_tournament


reward_tables = [
    {
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 10,
        "both_defect_winner": 0
    },
    {
        "both_coop": 5,
        "mixed_coop": 0,
        "mixed_defect": 10,
        "both_defect_winner": 1
    },
    {
        'both_coop': 2,
        'mixed_coop': 0,
        'mixed_defect': 3,
        "both_defect_winner": 0
    },
    {
        'both_coop': 2,
        'mixed_coop': 0,
        'mixed_defect': 3,
        "both_defect_winner": 1
    },
    {
        'both_coop': 5,
        'mixed_coop': 0,
        'mixed_defect': 3,
        "both_defect_winner": 1
    },
    {
        'both_coop': 5,
        'mixed_coop': 0,
        'mixed_defect': 3,
        "both_defect_winner": 0
    }         
]


population_limits = [5000, 3000]
initial_population_sizes = [100, 200, 500, 1000, 2000, 5000]
crossovers_rates = [0.0, 0.1, 0.2, 0.5]
mutation_rates = [0.0, 0.1, 0.2, 0.5]
SEEDS = [42, 43, 44, 45, 46]
supperted_selection_methods = {"proportional_to_fitness": OPTIONS.selLiteralToFitness, 
                               "ranked_population_curved": OPTIONS.selWithRankedPopulationCurved}
supported_determine_strategies = {
        "determineStrategyWithDominantRecessive": OPTIONS.determineStrategyWithDominantRecessive, 
        "determineStrategyWithMajority": OPTIONS.determineStrategyWithMajority
    }
encounter_evaluations = ["prisonDilemmaEval", "gambiteval"]
initial_cooperative_rates = [0.0, 0.1, 0.2, 0.5, 0.7, 1.0]







# Random sample experiemtns.

experiments_arr = []

def brute_force_sample_experiment():
    """
    
    def gambitGeneticSimulation(both_coop=2, both_defect_winner=1, mixed_coop=0, mixed_defect=3, INITIAL_COOPERATIE_RATE=INITIAL_COOPERATIE_RATE,
    START_WITH_PURE_STRATEGIES=START_WITH_PURE_STRATEGIES, RANDOMIZE_SEED=True, POPULATION_SIZE=POPULATION_SIZE, P_CROSSOVER=P_CROSSOVER, P_MUTATION=P_MUTATION, FLIPBIT_MUTATION_PROB=FLIPBIT_MUTATION_PROB, MAX_GENERATIONS=MAX_GENERATIONS, POPULATION_LIMIT=POPULATION_LIMIT, 
    GEN_SIZE=GEN_SIZE, RANDOM_SEED=RANDOM_SEED, lore="", encounterEval="prisonDilemmaEval", evaluate=evalTournamentGambit, select=selLiteralToFitness, curvePopulation=True, limit_strategy="LIMIT_TOP", determine_strategy=determineStrategyWithMajority) -> tuple:
    """
    total_computations = len(reward_tables) * len(initial_population_sizes) * len(initial_cooperative_rates) * len(crossovers_rates) * len(mutation_rates) * len(SEEDS) * len(supperted_selection_methods) * len(supported_determine_strategies) * len(encounter_evaluations)
    for reward_table in reward_tables:
        for initial_population_size in initial_population_sizes:
            for initial_cooperative_rate in initial_cooperative_rates:
                for crossover_rate in crossovers_rates:
                    for mutation_rate in mutation_rates:
                        for seed in SEEDS:
                            for selection_method in supperted_selection_methods.keys():
                                for determine_strategy in supported_determine_strategies.keys():
                                    for encounter_evaluation in encounter_evaluations:
                                        experiments_settings = {
                                            "POPULATION_SIZE": initial_population_size,        
                                            "both_coop": reward_table["both_coop"],
                                            "mixed_coop": reward_table["mixed_coop"],
                                            "mixed_defect": reward_table["mixed_defect"],
                                            "both_defect_winner": reward_table["both_defect_winner"],
                                            "INITIAL_COOPERATIE_RATE": initial_cooperative_rate,
                                            "POPULATION_LIMIT": 5000,
                                            "P_CROSSOVER": crossover_rate,
                                            "P_MUTATION": mutation_rate,
                                            "RANDOM_SEED": seed,
                                            "select": supperted_selection_methods[selection_method],
                                            "determine_strategy": supported_determine_strategies[determine_strategy],
                                            "encounterEval": encounter_evaluation,            
                                        }
                                        
                                        
                                        pprint.pprint(experiments_settings)
                                        
                                        population, coop_pop, defect_pop, logbook = gambitGeneticSimulation(**experiments_settings)
                                        end_coop_populations = coop_pop[-1]
                                        end_defect_populations = defect_pop[-1]
                                        end_population = population[-1]
                                        dominant_allele_switch = logbook.select("dominant_allele_switch")[-1]
                                        max_reached_at_generation = logbook.select("max_reached_at_generation")[-1]
                                        max_reached_value = logbook.select("max_reached_value")[-1]
                                        
                                        # is stable when 
                                        is_stable_population_size = True
                                        if max_reached_value > 0:
                                            is_stable_population_size = abs(end_population - max_reached_value) / max_reached_value < 0.05
                                        
                                        
                                        experiments_results = {
                                            "POPULATION_SIZE": initial_population_size,        
                                            "both_coop": reward_table["both_coop"],
                                            "mixed_coop": reward_table["mixed_coop"],
                                            "mixed_defect": reward_table["mixed_defect"],
                                            "both_defect_winner": reward_table["both_defect_winner"],
                                            "INITIAL_COOPERATIE_RATE": initial_cooperative_rate,
                                            "POPULATION_LIMIT": 5000,
                                            "P_CROSSOVER": crossover_rate,
                                            "P_MUTATION": mutation_rate,
                                            "RANDOM_SEED": seed,
                                            "select": selection_method,
                                            "determine_strategy": determine_strategy,
                                            "encounterEval": encounter_evaluation,
                                            "end_coop_populations": end_coop_populations,
                                            "end_defect_populations": end_defect_populations,
                                            "end_population": end_population,
                                            "dominant_allele_switch": dominant_allele_switch,
                                            "max_reached_at_generation": max_reached_at_generation,
                                            'max_reached_population': max_reached_value,
                                            "is_stable_population_size": is_stable_population_size,                   
                                        }
                                        pprint.pprint(experiments_results)
                                        experiments_arr.append(experiments_results)
                                    df_experiments = pd.DataFrame(experiments_arr)
                                    print("================= DF Experiments ====================")
                                    print(df_experiments.head(50))
    # store.
    df_experiments.to_csv("reports/behavioural_full_experiments.csv")
    
brute_force_sample_experiment()