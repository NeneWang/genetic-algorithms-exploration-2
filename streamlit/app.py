import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from deap import base, creator, tools, algorithms
import pandas as pd
from streamlit_extras.row import row



st.write('Hi, in this application, we have two pages: `Knapsack Problem` and `Genetic Algorithms Problem`')

# https://hackmd.io/@n_1IfOpxQPSjyRrn5yedJw/r1fbS-RZC#Genetic-Exploration-Report
st.write("This Simulator is intended to be used while being guided by the following report: [Genetic Exploration Report](https://hackmd.io/@n_1IfOpxQPSjyRrn5yedJw/r1fbS-RZC#Genetic-Exploration-Report)")


from streamlit_card import card


import streamlit as st

import pkgutil
from importlib import import_module

import streamlit as st
import streamlit_extras
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row

col1, col2 = st.columns(2)


@st.cache_resource
def show_extras():
    extra_names = [
        extra.name for extra in pkgutil.iter_modules(streamlit_extras.__path__)
    ]

    icon_row = row(10)

    for extra_name in extra_names:
        mod = import_module(f"streamlit_extras.{extra_name}")
        print(mod.__title__, mod.__icon__)
        icon = mod.__icon__
        icon_row.link_button(
            icon,
            f"https://arnaudmiribel.github.io/streamlit-extras/extras/{extra_name}/",
            help=mod.__title__,
            use_container_width=True,
        )

    icon_row.markdown("### ...")


# st.markdown(
#     "streamlit-extras is a Python library putting together useful Streamlit bits of code. It"
#     " includes > 40 (count emojis below!) functional or visual additions to Streamlit that will"
#     " make your life easier or your apps nicer. We call them *extras* and anyone's welcome to add"
#     " their owns!"
# )


# show_extras()

with col1:
    hasClicked = card(
    title="Knapsack Problem",
    text="Combinatorial Optimization Problem, find optimal selection of items.",
    image="https://hackmd.io/_uploads/Hk15JFB4R.png",
    url="")

with col2:

    hasClicked = card(
    title="Genetic Simulation",
    text="Analyze how strategic interactions influence the evolution of traits and behaviors within populations",
    image="https://hackmd.io/_uploads/BJZSmAINA.png",
    url="/genetic_population_sim"
    )