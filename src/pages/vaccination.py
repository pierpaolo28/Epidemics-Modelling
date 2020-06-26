import pandas as pd
import numpy as np
import torch
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import pages.home
import support.vacc_base as vacc


def write():
    with st.spinner("Loading Vaccination Modelling ..."):
        st.title('Time Limited Immunity and Vaccination Modelling')
        st.markdown('## Time Limited Immunity SIR')
        st.markdown(
            '''
            Updating our SIR model, we can be able to take into account the possibily that individuals might 
            not gain lifetime immunity from a desease when recovering from it, but that might instead be re-infected 
            again in the future after some time. The amount of time an individual might be immune from a desease can
            be represented by just adding a new variable to our model ($v$).
            '''
        )
        st.latex(
            r'''\frac{\partial S}{\partial t} = -\beta \times I \times \frac{S}{N} + v \times R''')
        st.latex(
            r'''\frac{\partial I}{\partial t} = \beta \times I \times \frac{S}{N} -\gamma \times I''')
        st.latex(
            r'''\frac{\partial R}{\partial t} = \gamma \times I - v \times R''')

        N = st.slider("Population Size: ", min_value=2, max_value=5000,
                      value=1000, step=10)

        sim_days = st.slider("Number of days: ",
                             min_value=2, max_value=1000,
                             value=100, step=10)

        orig_infected = st.slider("Number of individuals originally infected: ",
                                  min_value=1, max_value=N//2,
                                  value=3, step=1)

        contact_with_people = st.slider("Number of individuals at close contact in a day: ",
                                        min_value=0, max_value=N//2,
                                        value=5, step=1)

        prob_infect = st.slider("Probability of infection if in contact with an infected: ",
                                min_value=0.0, max_value=1.0,
                                value=0.05, step=0.1)

        days = st.selectbox("Number of days the desease can last", [
                            14, 7, 10, 21, 28])

        immu_days = st.number_input(
            "Number of days desease immunity can last", 0, 1000, 25)

        S, I, R, R0 = vacc.timed_SIR_sim(N, sim_days, orig_infected,
                                         prob_infect, contact_with_people, days, immu_days)
        vacc.timed_SIR_plot(S, I, R, R0)

        st.markdown('## Time Limited Immunity and Vaccination SIR')
        st.markdown(
            '''
            Extending our set of equations (adding an extra stage $\\frac{\partial V}{\partial t}$), we can be able to take into account how an epidemic will evolve once a vaccine is available. 
            In order to apply these modifications, we just need to apdate $\\frac{\partial S}{\partial t}$ and add the vaccination stage before just after it.
            To make the simulation more realistic, we can then also specify from when in time a vaccine could start being distributed and how fast it can produced and shipped ($p$). 
            Finally, a stage used to record the possible amount of deths is included (using the same notation for the SEIR and Advanced SEIR models).
            '''
        )
        st.latex(
            r'''\frac{\partial S}{\partial t} = -\beta \times I \times \frac{S}{N} + v \times R - p \times S''')
        st.latex(
            r'''\frac{\partial V}{\partial t} = p \times S''')
        st.latex(
            r'''\frac{\partial I}{\partial t} = -\beta \times I \times \frac{S}{N}  -(1-\alpha) \times \gamma \times I -\alpha \times \rho \times I''')
        st.latex(
            r'''\frac{\partial R}{\partial t} = (1-\alpha) \times \gamma \times I - v \times R ''')
        st.latex(
            r'''\frac{\partial D}{\partial t} = \alpha \times \rho \times I ''')

        death_days = st.number_input(
            "Number of days the desease can take to become lethal:", 1, days, 5)

        alpha = st.slider("Death rate: ",
                          min_value=0.01, max_value=1.0,
                          value=0.2, step=0.1)

        start_vacc = st.number_input(
            "Number of Days to start Vaccine Distribution:", 1, sim_days, 30)

        vacc_cap = st.slider("Vaccine Distribution rate: ",
                             min_value=0.01, max_value=1.0,
                             value=0.1, step=0.1)

        S, V, I, R, D, R0 = vacc.vacc_SIR_sim(N, sim_days, orig_infected, prob_infect,
                                              contact_with_people, days, immu_days, start_vacc, vacc_cap, alpha, death_days)
        vacc.vacc_SIR_plot(S, V, I, R, D, R0)
