import pandas as pd
import numpy as np
import torch
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import pages.home
import support.advanced_models as ad


def write():
    with st.spinner("Loading Advanced SEIR Modelling ..."):
        st.title('Advanced SEIR Modelling')
        st.markdown(
            '''
            In this section, is taken a step further the SEIR model proposed in the "SIR and SEIR Modelling" tab. In this improved version, we now: 
            - Take into account the portion of infected individuals which dies instead of recover.
            - $R_{0}$ is not anymore static but dynamically changes over time. In this example, two functions have been used  in order to simulate $R_{0}$ behaviour over time: a Sigmoid or Sinusoidal. In this way, we are now able to model
            how a government might react in order to control the spread of the disease by exercising social distancing measures. A sigmoid in it's minimum point can in fact represent a lock-down and the smoothness by which it reaches its minimum can 
            easily represent how gradually the restrictions have been applied. An additional parameter is provided in order to decide from what day onward to start applying the restrictions (so that to observe what could be the consequences of a late or early intervention). The sinusoidal landscape, can instead be used in order to model possible sequential waves a disease can lead to.
            -  Also the death rate has been designed to be time and age dependent. To each different age group is assigned a different base death rate (the older, the greater), which increase linearly with the increase in the number of infected at each time-step. Therefore, with higher peaks of individuals infected all at the same time
            increases the likelihood of individuals to die (mimicking strained healthcare system which don't have the potential to cure everyone at the same time). An animation of how the percentage of people dying if positive ($\\alpha$) varies over time, is available in the animated simulation below.
            '''
        )

        N = st.slider("Population Size: ", min_value=2, max_value=5000,
                      value=1000, step=1)

        sim_days = st.slider("Number of days: ",
                             min_value=2, max_value=1000,
                             value=100, step=10)

        orig_infected = st.slider("Number of individuals originally infected/esposed: ",
                                  min_value=1, max_value=N//2,
                                  value=7, step=1)

        days = st.selectbox("Number of days the disease can last", [
                            14, 7, 10, 21, 28])

        inc_days = st.selectbox("Number of incubation days for the disease", [
                                float(i) for i in range(1, days, 3)])

        death_days = st.selectbox("Number of days the disease can take to become lethal", [
            float(i) for i in range(int(inc_days)+2, days, 2)])

        # Age groups = 0-20, 20-50, 50-70, 70-110
        age_props = st.text_input(
            'In bins of: 0-20, 20-50, 50-70, 70-110. What are group range proportions in the population?', '0.15, 0.25, 0.4, 0.2')
        age_props2 = age_props.split(', ')
        if len(age_props2) != 4:
            age_props2 = age_props.split(' ')
        age_props = [float(i) for i in age_props2]
        if (sum(age_props) == 1) or len(age_props) == 4:
            age_based_alpha = [0.05, 0.1, 0.3, 0.5]
            pop_age_prop = [age_props[0], age_props[1],
                            age_props[2], age_props[3]]
            opt_alpha = sum(
                [i*j for i, j in zip(age_based_alpha, pop_age_prop)])

            scaling = st.slider("How much weight should older age have on the death rate?",
                                min_value=0.001, max_value=1.0,
                                value=0.1, step=0.01)

            land = st.radio("What's landscape should R follow?",
                            ('Sigmoid', 'Sinusoidal'))
            if land == 'Sigmoid':
                x = st.slider("From what day social distancing measures have been applied?",
                              min_value=0, max_value=sim_days-1,
                              value=40, step=1)
                dec_factor = st.slider("How drastically rapidly have the restrictions been applied?",
                                       min_value=0.1, max_value=1.0,
                                       value=0.3, step=0.1)
                R0_beg = st.number_input("Maximum possible R value", 1, 14, 6)
                R0_end = st.number_input(
                    "Minimum possible R value", 1, R0_beg, 1)
                S, E, I, R, D, R0_time, alpha_time = ad.ad_SEIR_sim(N, sim_days, orig_infected, days,
                                                                    inc_days, scaling, opt_alpha, death_days, R0_beg, R0_end, dec_factor, x)
            else:
                scale_factor = st.slider("Sinusoid scaling R value: ",
                                         min_value=1, max_value=10,
                                         value=2, step=1)
                S, E, I, R, D, R0_time, alpha_time = ad.ad_SEIR_sim2(N, sim_days, orig_infected, days,
                                                                     inc_days, scaling, opt_alpha, death_days, scale_factor)

            ad.ad_SEIR_plot(S, E, I, R, D, R0_time, alpha_time)
        else:
            st.write(
                "The overall 4 comma separated population proportions should sum up to one, please update your selection. Your selection currently sums up to " + str(sum(age_props)) + " and has a lenght of " + str(len(age_props)) + '.')
