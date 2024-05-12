import streamlit as st
from deap import base, creator, tools
import matplotlib.pyplot as plt
import seaborn as sns

from modules.gambit_algorithm import gambitGeneticSimulation
from modules.deap_expansion import OPTIONS
# Predefined cases
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
        "encounterEval": OPTIONS.INCREASING_DIFFICULTY,
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
    }
}

# Streamlit app interface
st.title("Gambit Genetic Simulation")

# Dropdown for selecting a precurated case
case = st.selectbox("Select a precurated case", list(precurated_cases.keys()))

# Retrieve selected case settings
case_settings = precurated_cases[case]

# Display sliders for case parameters that can be adjusted
both_coop = st.slider("Both Cooperative Score", min_value=0, max_value=10, value=case_settings["both_coop"])
mixed_coop = st.slider("Mixed Cooperative Score", min_value=0, max_value=10, value=case_settings["mixed_coop"])
mixed_defect = st.slider("Mixed Defective Score", min_value=0, max_value=10, value=case_settings["mixed_defect"])
both_defect_winner = st.slider("Both Defective Winner Score", min_value=0, max_value=10, value=case_settings["both_defect_winner"])
population_size = st.slider("Population Size", min_value=10, max_value=5000, value=case_settings["POPULATION_SIZE"])
initial_cooperation_rate = st.slider("Initial Cooperation Rate", min_value=0.0, max_value=1.0, value=case_settings["INITIAL_COOPERATIE_RATE"])
p_crossover = st.slider("Crossover Probability", min_value=0.0, max_value=1.0, value=case_settings["P_CROSSOVER"])
p_mutation = st.slider("Mutation Probability", min_value=0.0, max_value=1.0, value=case_settings["P_MUTATION"])

# Update the selected case settings with user inputs
case_settings.update({
    "both_coop": both_coop,
    "mixed_coop": mixed_coop,
    "mixed_defect": mixed_defect,
    "both_defect_winner": both_defect_winner,
    "POPULATION_SIZE": population_size,
    "INITIAL_COOPERATIE_RATE": initial_cooperation_rate,
    "P_CROSSOVER": p_crossover,
    "P_MUTATION": p_mutation
})

# Function to run the simulation
def run_simulation():
    return gambitGeneticSimulation(**case_settings)

# Run simulation button
if st.button("Run Simulation"):
    population, coop_pop, defect_pop = run_simulation()
    
    # Plot results
    fig, ax = plt.subplots()
    sns.set_style("whitegrid")
    ax.plot(population, color='blue')
    ax.plot(coop_pop, color='green')
    ax.plot(defect_pop, color='red')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Population')
    ax.legend(['Total', 'Cooperative', 'Aggressive'])
    ax.set_title(f"Population over Generations | {case}")
    st.pyplot(fig)
