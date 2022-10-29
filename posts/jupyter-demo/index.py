# ---
# title: "Jupyter Demo"
# author: "Matthieu"
# date: "2022-10-29"
# categories: [news, code, analysis]
# image: "miaou.png"
# format:
#   html:
#     code-fold: true
#     code-tools: true
# jupyter: python3
# toc: true
# execute:
#   echo: true
# ---

# # Intro
#
# This is a first attempt of a demo with interactive output. We use a basic plotly chart for this
#
# * And so on ..

# +
# # %load /home/matthieu/.jupyter/default_imports.py
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

# Set seed for reproducibility
np.random.seed(10)
# Turn off warnings
warnings.filterwarnings("ignore")

# + [markdown] tags=[]
# ## Scatter plot
#
# In this example, we will see a simple scatter plot 

# + tags=["remove-cell"]
import matplotlib_inline.backend_inline

# Plot settings
plt.style.use("https://github.com/aeturrell/coding-for-economists/raw/main/plot_style.txt")
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")

# Set max rows displayed for readability
pd.set_option("display.max_rows", 6)


# from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
# from plotly.graph_objs import *
# init_notebook_mode(connected=True)

import plotly.express as px

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")
fig.show()

