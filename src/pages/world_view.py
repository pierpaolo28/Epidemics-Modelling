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


def write():
    with st.spinner("Loading World View ..."):

        st.title('COVID-19 World View')

        df2 = pd.read_csv('data/all.csv')
        resources = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
                     ]

        data_list = world_map(resources, df2)

        totay_cases = data_list[0][data_list[0]['Dates']
                                   == data_list[0]['Dates'].unique()[::-1][0]]
        today_deths = data_list[2][data_list[2]['Dates']
                                   == data_list[2]['Dates'].unique()[::-1][0]]
        today = pd.merge(totay_cases, today_deths, left_on='Country/Region',
                         right_on='Country/Region', how='inner')
        today.loc[today.loc[today['Country/Region'] ==
                            'United Kingdom of Great Britain and Northern Ireland'].index, 'Country/Region'] = 'United Kingdom'
        today_top = today.sort_values(by='Cases_y', ascending=False)[:10]
        yest_cases = data_list[0][data_list[0]['Dates']
                                  == data_list[0]['Dates'].unique()[::-1][1]]
        yest_deths = data_list[2][data_list[2]['Dates']
                                  == data_list[2]['Dates'].unique()[::-1][1]]
        yest = pd.merge(yest_cases, yest_deths, left_on='Country/Region',
                        right_on='Country/Region', how='inner')
        yest.loc[yest.loc[yest['Country/Region'] ==
                          'United Kingdom of Great Britain and Northern Ireland'].index, 'Country/Region'] = 'United Kingdom'
        yest_top = yest.sort_values(by='Cases_y', ascending=False)[:10]
        res = pd.merge(today_top, yest_top, left_on='Country/Region',
                       right_on='Country/Region', how='inner')
        last_cases = res['Cases_x_x'] - res['Cases_x_y']
        last_deths = res['Cases_y_x'] - res['Cases_y_y']

        stats(today_top['Country/Region'], today_top['Cases_x'],
              today_top['Cases_y'], "Highest estimated cumulative cases/deths")

        stats(res['Country/Region'], last_cases,
              last_deths, "Change in cases/deths in the last 24 hours")

        low = 0
        up = st.text_input('How many cases maximum to consider?', str(np.inf))
        world_plot(data_list[0], float(up), low, name='Cases')
        world_plot(data_list[1], float(up), low, name='Recovered')
        world_plot(data_list[2], float(up), low, name='Deths')
