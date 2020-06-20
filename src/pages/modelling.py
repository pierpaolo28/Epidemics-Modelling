import pandas as pd
import numpy as np
import torch
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import pages.home
from support.utilities import world_map, world_plot, stats
from support.base_models import SIR_sim, SIR_plot, SEIR_sim, SEIR_plot


def write():
    with st.spinner("Loading Modelling ..."):
        st.title('SIR and SEIR Modelling')
        st.markdown('## SIR (Susceptible-Infected-Recovered)')
        st.markdown(
            '''
            The SIR model can be described by the following three formulas, where 
            $N$ is the total number of elements in the population,
            $\\beta$ represents average amount of people an infected element can be able to infect in a day and
            $\gamma$ the percentage of how many individuals recover from the desease each day.
            '''
        )
        st.latex(
            r'''\frac{\partial S}{\partial t} = -\beta \times I \times \frac{S}{N}''')
        st.latex(
            r'''\frac{\partial I}{\partial t} = \beta \times I \times \frac{S}{N} -\gamma \times I''')
        st.latex(
            r'''\frac{\partial R}{\partial t} = \gamma \times I''')

        N = st.slider("Population Size: ", min_value=2, max_value=5000,
                      value=100, step=10)

        sim_days = st.slider("Number of days: ",
                             min_value=2, max_value=1000,
                             value=100, step=10)

        orig_infected = st.slider("Number of individuals originally infected/esposed: ",
                                  min_value=1, max_value=N//2,
                                  value=3, step=1)

        contact_with_people = st.slider("Number of individuals at close contact in a day: ",
                                        min_value=0, max_value=N//2,
                                        value=5, step=1)

        prob_infect = st.slider("Probability of infection if in contact with an infected: ",
                                min_value=0.0, max_value=1.0,
                                value=0.2, step=0.1)

        days = st.selectbox("Number of days the desease can last", [
                            14, 1, 3, 7, 10, 21, 28])

        S, I, R, R0 = SIR_sim(N, sim_days, orig_infected,
                              prob_infect, contact_with_people, days)
        SIR_plot(S, I, R, R0)

        st.markdown('## SEIR (Susceptible-Esposed-Infected-Recovered)')
        st.markdown(
            '''
            In order to make our more more realistic, we can then add an additional state E representing all the population 
            elements which are still in the incubation stage before becoming infected. In order to apply these modifications, we
            just need to apdate $\\frac{\partial I}{\partial t}$ and add this extra stage before just before it. The only variable which needs to
            be added compared to the SIR model is $\delta$ (the percentage of how many individuals move from the incubaation period to being infected).
            '''
        )
        st.latex(
            r'''\frac{\partial E}{\partial t} = \beta \times I \times \frac{S}{N} -\delta \times E''')
        st.latex(
            r'''\frac{\partial I}{\partial t} = \delta \times E \times -\gamma \times I''')

        inc_days = st.selectbox("Number of incubation days for the desease", [
                                float(i) for i in range(1, days, 3)])

        S, E, I, R, R0 = SEIR_sim(
            N, sim_days, orig_infected, prob_infect, contact_with_people, days, inc_days)
        SEIR_plot(S, E, I, R, R0)
