import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from support.tracing_base import make_df
from support.central_hub import pop_simulation, replay_plot


def write():
    with st.spinner("Loading Central Hubs ..."):
        st.title("Central Hubs")
        st.write(
            """
                Imposing travel restrictions can greatly help in lowering the rate at which a desease can spread. 
                Individuals, although still have at times to visit centrals hubs such as supermarkets during lockdowns. 
                What would be the affect of allowing a central hub on the velocity at which a desease can spread? In this simulation,
                we can easily observe how having even just a single central hub, can lead to a fast spreading of the desease across different communities.
            """
        )
        probs_positives = 0.02
        grid_max = [[0, 5], [0, 5]]
        iterations = 50
        grids_types = {
            '4 Isolated Communities': [[[0, 1], [0, 1]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]]],
            '4 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]]],
            '8 Isolated Communities': [[[0, 1], [0, 1]], [[2, 3], [4, 5]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]], [[0, 1], [2, 3]], [[2, 3], [2, 3]], [[4, 5], [2, 3]]],
            '8 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[2, 3], [4, 5]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]], [[0, 1], [2, 3]], [[2, 3], [2, 3]], [[4, 5], [2, 3]]],
        }

        size = st.slider("Population size: ",
                         min_value=1, max_value=500,
                         value=200, step=10)

        d_p = st.slider("Death Probability: ",
                        min_value=0.0, max_value=0.5,
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

        hub_locations = {
            '4 Isolated Communities': [[2, 3], [2, 3]],
            '4 Communities with shared central point': [[2, 3], [2, 3]],
            '8 Isolated Communities': [[2, 3], [0, 1]],
            '8 Communities with shared central point': [[2, 3], [0, 1]]
        }

        central_location_grid = hub_locations[grid_selection]
        prob_to_visit_location = st.slider("Probability of visiting the central hub: ",
                                           min_value=0.0, max_value=1.0,
                                           value=0.3, step=0.01)

        negatives, positives, survivors, deaths, x_res, y_res, state, index = pop_simulation(size, iterations,
                                                                                             probs_positives,
                                                                                             grid_limits,
                                                                                             min_contact_radious,
                                                                                             unlikelyness_of_spread,
                                                                                             static, d_p, avg_age,
                                                                                             central_location_grid,
                                                                                             prob_to_visit_location)

        df = make_df(x_res, y_res, state, index, grid_max)

        replay_plot(negatives, positives, survivors, deaths, df,
                    grid_max=grid_max, loc_grid=central_location_grid)
