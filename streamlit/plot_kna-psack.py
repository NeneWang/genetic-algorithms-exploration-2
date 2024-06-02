import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pprint
from deap import base, creator, tools, algorithms
import pandas as pd

# Sample data
x = [1, 2, 3]
y = [1, 2, 3]

# Create the scatter plot
sns.scatterplot(x=x, y=y)

print('Hello, World!')