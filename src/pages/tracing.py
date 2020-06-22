import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from support.tracing_base import pop_simulation, make_df, replay_plot


def write():
    with st.spinner("Loading Track and Tracing ..."):
        st.title("Track and Tracing")
        st.write(
            """
                Track and Tracing can be considered to be the most effective approach in order to take under control a pandemic.
                Although, one of the main limitations of this approach, is that in less lethal deseases it might be difficult to correctly identify in time all the individuals infected (some might be asyntomatic).
                Developing contact tracing apps using criptography, could therefore enable us to keep our privacy intact while reducing the risk of spreading the desease.

                In the following model, is presented how an epidemics might evolve is all the infected individual are succesfully identified and then make their way to a quarantene location designed for all the individuals affected by the desease. 
                Individuals are represented with different associated volicities in order to simulate the fact that same might be tracked before than others and might interact with susceptible individuals along the way.
            """
        )
        probs_positives = 0.04
        grid_max = [[0, 5], [0, 5]]
        iterations = 50
        grids_types = {
            'Single Community': [grid_max],
            '2 Isolated Communities': [[[0, 1], [0, 1]], [[4, 5], [4, 5]]],
            '2 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[4, 5], [4, 5]]],
            '4 Isolated Communities': [[[0, 1], [0, 1]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]]],
            '4 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]]],
            '8 Isolated Communities': [[[0, 1], [0, 1]], [[2, 3], [4, 5]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]], [[0, 1], [2, 3]], [[2, 3], [2, 3]], [[4, 5], [2, 3]]],
            '8 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[2, 3], [4, 5]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]], [[0, 1], [2, 3]], [[2, 3], [2, 3]], [[4, 5], [2, 3]]],
            '6 Communities with shared central point and metropoli': [grid_max, [[0, 1], [0, 1]], [[2, 3], [2, 5]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]], [[0, 1], [2, 3]], [[4, 5], [2, 3]]]
        }

        size = st.slider("Population size: ",
                         min_value=1, max_value=500,
                         value=200, step=10)

        d_p = st.slider("Death Probability: ",
                        min_value=0.0, max_value=1.0,
                        value=0.02, step=0.01)

        min_contact_radious = st.slider("Contact radius: ",
                                        min_value=0.0, max_value=1.0,
                                        value=0.2, step=0.01)

        unlikelyness_of_spread = st.slider("Probability of how unlikely it is to spread the virus if within the contact radius: ",
                                           min_value=0.0, max_value=1.0,
                                           value=0.8, step=0.01)

        avg_age = st.slider("Average population age: ",
                            min_value=1, max_value=100,
                            value=55, step=5)
        avg_age = avg_age/100
        static = st.selectbox("Static Population", [False, True])

        grid_selection = st.selectbox(
            "Types of communities", list(grids_types.keys()))
        grid_limits = grids_types[grid_selection]

        quarantine_locations = {
            'Single Community': [[4, 5], [0, 1]],
            '2 Isolated Communities': [[4, 5], [0, 1]],
            '2 Communities with shared central point': [[4, 5], [0, 1]],
            '4 Isolated Communities': [[2, 3], [2, 3]],
            '4 Communities with shared central point': [[2, 3], [2, 3]],
            '8 Isolated Communities': [[2, 3], [0, 1]],
            '8 Communities with shared central point': [[2, 3], [0, 1]],
            '6 Communities with shared central point and metropoli': [[2, 3], [0, 1]]
        }

        quarantene_grid = quarantine_locations[grid_selection]
        prob_to_be_untracked = 0

        negatives, positives, survivors, deaths, x_res, y_res, state, index = pop_simulation(size, iterations,
                                                                                             probs_positives,
                                                                                             grid_limits,
                                                                                             min_contact_radious,
                                                                                             unlikelyness_of_spread,
                                                                                             static, d_p, avg_age,
                                                                                             quarantene_grid,
                                                                                             prob_to_be_untracked)

        df = make_df(x_res, y_res, state, index, grid_max)

        replay_plot(negatives, positives, survivors, deaths, df,
                    grid_max=grid_max, quar_grid=quarantene_grid)

        st.write("The following model, extends instead the first model by adding a probability value that some individuals might not get traced at all and might therefore end up spreading the desease (eg. coronavirus asyntomatic or limited available testing capacity).")

        prob_to_be_untracked = st.slider("Probability individuals might be untracked: ",
                                         min_value=0.0, max_value=1.0,
                                         value=0.5, step=0.1)

        negatives, positives, survivors, deaths, x_res, y_res, state, index = pop_simulation(size, iterations,
                                                                                             probs_positives,
                                                                                             grid_limits,
                                                                                             min_contact_radious,
                                                                                             unlikelyness_of_spread,
                                                                                             static, d_p, avg_age,
                                                                                             quarantene_grid,
                                                                                             prob_to_be_untracked)

        df = make_df(x_res, y_res, state, index, grid_max)

        replay_plot(negatives, positives, survivors, deaths, df,
                    grid_max=grid_max, quar_grid=quarantene_grid)
