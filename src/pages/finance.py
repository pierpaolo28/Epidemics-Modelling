import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from support.finance_base import pop_simulation, replay_plot


def write():
    with st.spinner("Loading Finance Simulation ..."):
        st.title("Finance Simulation")
        st.write(
            """
                Applying different types of social distancing and limited movement restrictions, could potentially lead to a good cointainement of the
                spreading of a desease, but also to a major shrink of the whole economy. In the following simulation, two main types of responses are simulated:
                no containement at all or imposing an hard lockdown. In order to keep track of the economic consequences of these two different approaches, the created population has been 
                divided into 3 different classes: Working Class, Middle Class and Upper Class. Which have assigned different types of incomes and expenses which they have to pay on daily bases depending on their income.
                The government offers the opportunity to give financial support on daily basis in case any of the citizen is struggling to pay its expenses. In a fully functioning society, most of the citizen are able to pay their 
                expenses without having to use their savings or ask for help. As restrictions are imposed and freedom of movement is limited, citizen can only continue to earning and be self-sufficient if they are able to work from home.
                Otherwise, the will have to make use of their savings and of the government support provided. Because of the neture of their work, middle and higher class workers, are more likely be able to work remotely.
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
        static = st.selectbox("Population in Lockdown", [True, False])

        grid_selection = st.selectbox(
            "Types of communities", list(grids_types.keys()))
        grid_limits = grids_types[grid_selection]

        top_remote_working = st.slider("Upper and Middle class probability of doing remote working: ",
                                       min_value=0.0, max_value=1.0,
                                       value=0.7, step=0.1)
        low_remote_working = st.slider("Working class probability of doing remote working: ",
                                       min_value=0.0, max_value=1.0,
                                       value=0.4, step=0.1)

        negatives, positives, survivors, deaths, x_res, y_res, state, index, soc_class, savings, soc_help = pop_simulation(size,
                                                                                                                           iterations,
                                                                                                                           probs_positives,
                                                                                                                           grid_limits,
                                                                                                                           min_contact_radious,
                                                                                                                           unlikelyness_of_spread,
                                                                                                                           static, d_p, avg_age,
                                                                                                                           top_remote_working,
                                                                                                                           low_remote_working)

        d = {'x_pos': x_res, 'y_pos': y_res, 'state': state, 'index': index}
        df = pd.DataFrame(data=d)
        for i in list(df['index'].unique()):
            for j in list(df['state'].unique()):
                if len(df[(df['index'] == i) & (df['state'] == j)]) == 0:
                    df = df.append(pd.DataFrame([[grid_max[0][1]+5, grid_max[1][1]+5, j, i]],
                                                columns=df.columns))
        d2 = {'Savings': savings, 'Social Class': soc_class,
              'Social Help': soc_help, 'index': index}
        df2 = pd.DataFrame(data=d2)

        daily_average_savings = []
        daily_support_requests = []
        for j in [0, 1, 2]:
            day_savings, day_help = [], []
            for i in list(df2['index'].unique()):
                day_savings.append(np.mean(df2[(df2['index'] == i) & (
                    df2['Social Class'] == j)]['Savings'].values))
                day_help.append(np.sum(df2[(df2['index'] == i) & (
                    df2['Social Class'] == j)]['Social Help'].values))
            daily_average_savings.append(day_savings)
            daily_support_requests.append(day_help)

        replay_plot(negatives, positives, survivors, deaths, df,
                    grid_max, daily_average_savings, daily_support_requests)

        st.markdown("## Simulation Report")
        st.write('Total number of financial support requests received from working class: ' +
                 str(sum(daily_support_requests[0])))
        st.write('Total number of financial support requests received from middle class: ' +
                 str(sum(daily_support_requests[1])))
        st.write('Total number of financial support requests received from upper class: ' +
                 str(sum(daily_support_requests[2])))

        tot_savings = daily_average_savings[0][len(daily_average_savings[0])-1]+daily_average_savings[1][len(
            daily_average_savings[0])-1]+daily_average_savings[2][len(daily_average_savings[0])-1]

        st.write('Averaged Total amount of savings accumulated: ' +
                 str(round(tot_savings, 3)))
