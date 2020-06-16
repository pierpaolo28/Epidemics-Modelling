import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from support.modelling_pop import pop_simulation, replay_plot


def write():
    with st.spinner("Loading Population Modelling ..."):
        st.title("Population Modelling")
        probs_positives = 0.04
        grid_limits = [2, 2]
        iterations = 100

        size = st.slider("Population size: ",
                         min_value=1, max_value=500,
                         value=100, step=10)

        d_p = st.slider("Death Probability: ",
                        min_value=0.0, max_value=1.0,
                        value=0.02, step=0.01)

        min_contact_radious = st.slider("Contact radius: ",
                                        min_value=0.0, max_value=1.0,
                                        value=0.3, step=0.01)

        unlikelyness_of_spread = st.slider("Probability of how unlikely it is to spread the virus if within the contact radius: ",
                                           min_value=0.0, max_value=1.0,
                                           value=0.9, step=0.01)

        static = st.selectbox("Chaotic Population", [False, True])

        negatives, positives, survivors, deaths, x_res, y_res, state, index = pop_simulation(size, iterations,
                                                                                             probs_positives,
                                                                                             grid_limits,
                                                                                             min_contact_radious,
                                                                                             unlikelyness_of_spread,
                                                                                             static, d_p)
        d = {'x_pos': x_res, 'y_pos': y_res, 'state': state, 'index': index}
        df = pd.DataFrame(data=d)
        for i in list(df['index'].unique()):
            for j in list(df['state'].unique()):
                if len(df[(df['index'] == i) & (df['state'] == j)]) == 0:
                    df = df.append(pd.DataFrame([[grid_limits[0]+5, grid_limits[1]+5, j, i]],
                                                columns=df.columns))

        replay_plot(negatives, positives, survivors, deaths, df, grid_limits)
        st.markdown("## Simulation Report")
        st.markdown("### Final population distribution")
        st.write("Number of Susceptible Individuals: ",
                 negatives[len(negatives)-1])
        st.write("Number of Infected Individuals: ",
                 positives[len(negatives)-1])
        st.write("Number of Recovered Individuals: ",
                 survivors[len(negatives)-1])
        st.write("Number of Deaths: ", deaths[len(negatives)-1])
        st.markdown("### Key highlight")
        st.write("Peak number of infected: ", max(positives))
