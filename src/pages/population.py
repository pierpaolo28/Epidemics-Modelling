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
        st.markdown(
            "As described in the Desease Growth tab, the number of new cases can vary according to the following formula: ")
        st.latex(r'''\Delta N_{d} = E \times p \times N_{d}''')
        st.markdown(
            """
            Therefore, the only way we can be able to decrease the number of cases, is by decresing the values of $E$ and $p$.
            This can happen for example:
            - $E$ can decrease if travelling and meetings of people are reduced as much as possible.
            - $p$ can be reduced instead for example by making less likely to catch the desease by taking precotions such as washing hands, wearing masks, avoid touching our faces, etc...
            
            This trend can be observed in the following proposed model by the **Contact Radius** ($E$) and **Probability of how unlikely it is to spread the virus if within the contact radius** (complementary of $p$) variables.
            In this way, causal effects of social distancing and improved hygiene can be easily inspected. Furthermore, the role of dividing individuals in different communities is additionally studied.
        """)
        probs_positives = 0.05
        grid_max = [[0, 5], [0, 5]]
        iterations = 100
        grids_types = {
            'Single Community': [grid_max],
            '2 Isolated Communities': [[[0, 1], [0, 1]], [[4, 5], [4, 5]]],
            '2 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[4, 5], [4, 5]]],
            '4 Isolated Communities': [[[0, 1], [0, 1]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]]],
            '4 Communities with shared central point': [grid_max, [[0, 1], [0, 1]], [[4, 5], [4, 5]], [[0, 1], [4, 5]], [[4, 5], [0, 1]]]
        }

        size = st.slider("Population size: ",
                         min_value=1, max_value=500,
                         value=60, step=10)

        d_p = st.slider("Death Probability: ",
                        min_value=0.0, max_value=1.0,
                        value=0.02, step=0.01)

        min_contact_radious = st.slider("Contact radius: ",
                                        min_value=0.0, max_value=1.0,
                                        value=0.4, step=0.01)

        unlikelyness_of_spread = st.slider("Probability of how unlikely it is to spread the virus if within the contact radius: ",
                                           min_value=0.0, max_value=1.0,
                                           value=0.5, step=0.01)

        avg_age = st.slider("Average population age: ",
                            min_value=1, max_value=100,
                            value=65, step=5)
        avg_age = avg_age/100
        static = st.selectbox("Static Population", [False, True])

        grid_selection = st.selectbox(
            "Types of communities", list(grids_types.keys()))
        grid_limits = grids_types[grid_selection]

        negatives, positives, survivors, deaths, x_res, y_res, state, index = pop_simulation(size, iterations,
                                                                                             probs_positives,
                                                                                             grid_limits,
                                                                                             min_contact_radious,
                                                                                             unlikelyness_of_spread,
                                                                                             static, d_p, avg_age)
        d = {'x_pos': x_res, 'y_pos': y_res, 'state': state, 'index': index}
        df = pd.DataFrame(data=d)
        for i in list(df['index'].unique()):
            for j in list(df['state'].unique()):
                if len(df[(df['index'] == i) & (df['state'] == j)]) == 0:
                    df = df.append(pd.DataFrame([[grid_max[0][1]+5, grid_max[1][1]+5, j, i]],
                                                columns=df.columns))

        replay_plot(negatives, positives, survivors,
                    deaths, df, grid_max=grid_max)
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
