import streamlit as st
from deap import base, creator, tools
import matplotlib.pyplot as plt
import seaborn as sns

from modules.gambit_algorithm import gambitGeneticSimulation
# Predefined cases
precurated_cases = {
    "be1.tribal_hunters": {...},  # Replace with the actual precurated cases you provided
    # Add other cases here
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
