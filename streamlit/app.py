import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from deap import base, creator, tools, algorithms
import pandas as pd


st.write('Hi, in this application, we have two pages: `Knapsack Problem` and `Genetic Algorithms Problem`')

# https://hackmd.io/@n_1IfOpxQPSjyRrn5yedJw/r1fbS-RZC#Genetic-Exploration-Report
st.write("This Simulator is intended to be used while being guided by the following report: [Genetic Exploration Report](https://hackmd.io/@n_1IfOpxQPSjyRrn5yedJw/r1fbS-RZC#Genetic-Exploration-Report)")