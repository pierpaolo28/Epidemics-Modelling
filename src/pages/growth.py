import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from support.utilities import world_map
from support.log_plots import process_data, exponential_view, log_view, log, exp, fit_curve, fit_plot


def write():
    with st.spinner("Loading Disease Growth ..."):

        st.title('COVID-19 Disease Growth')

        df2 = pd.read_csv('data/all.csv')
        resources = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                     'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
                     ]

        data_list, fig, fig2 = world_map(resources, df2)

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

        top_trends, topten_weekly_results = process_data(
            data_list, today_top)

        st.markdown("## Keeping track of how fast a disease spreads")

        st.write("Examining how the number of cases increases over time using a linear plot"
                 " can be difficult since different countries have different population sizes"
                 ", using instead a logarithmic plot, everything becomes clear. Using the"
                 " logarithmic verison of the plot below, we can in fact clearly see that all the different"
                 " countries followed approximately the same path in the evolution of the number of cases."
                 " The growth is at first exponential until it reaches an inflection point and then becomes a logistic"
                 " (this can happen either thanks to disease spreading prevention techniques such as improved hygiene, social distancing"
                 ", etc.. or because the disease already spread across the majority of the population in interest and therefore is left with not"
                 "not many people to infect).")

        exponential_view(top_trends, topten_weekly_results)

        df_log_plot = pd.DataFrame(topten_weekly_results, columns=list(
            top_trends['Week_Number'].unique()))
        df_log_plot2 = df_log_plot.iloc[:, 1:]
        df_log_plot2[str(df_log_plot2.columns[-1]+1)
                     ] = [0 for i in range(len(df_log_plot2))]
        df_log_plot2.columns = df_log_plot.columns
        df_log_plot = df_log_plot.iloc[:, :-1]
        df_log_plot2 = df_log_plot2.iloc[:, :-1]
        cases_change = df_log_plot2.sub(df_log_plot)
        list_cases_change = cases_change.values.tolist()
        list_weekly_cases = df_log_plot.values.tolist()

        st.markdown(
            "## Understanding how close we are to the end of the exponential phase")

        st.write("While going through an exponential growth, it can be difficult to understand "
                 "how long will it last (if the growth is going to still keep being exponential or is going to start decaying). "
                 "One possible way to approach this problem, is to focus our attention on the rate of change in new cases from a week to another. "
                 "Plotting this on a both axis logarithmic scale, we would then clearly see that all the different countries have a same linear growth in cases. "
                 "Although, using some form of containement, some of these countries are succesfully able to escape from this linear growth in cases."
                 "Using this type of approach, we can successfully emphasize the deviation in the growth of an exponential curve. ")

        log_view(top_trends, list_weekly_cases, list_cases_change)

        st.write(
            "The change in the number of cases from a day to another, can be defined by the following equation:")
        st.latex(r'''\Delta N_{d} = E \times p \times N_{d}''')
        st.markdown("Where $E$ represents the average number of people we are exposed to every day "
                    ", $p$ represents the probability that an exposure might lead to an infection and $N_{d}$ is the number of cases as today.")
        st.markdown("Using the logarithmic linear graphs, we could then perform a linear regression to find the line of best fit and find out how many days does it take for our cases to increase by a fixed constant. "
                    "Finally, using metrics such as the $R^{2}$ score, we could then quantitatively measure how far are our curves from an exponential curve.")

        st.markdown(
            "Another way to examine if we are reaching the end of an exponential curve, is by examining the slope (Growth Factor).")

        st.latex(
            r'''Growth \; Factor = \dfrac{\Delta N_{d}}{\Delta N_{d-1}}''')
        st.markdown("A growth factor of more than one, will shows as that we are still going through an exponential growth, while a growth factor equal to 1 can tell us we might now be approaching our inflection point.")

        # Daily
        topten_weekly_results = []
        for i in list(top_trends['Country/Region'].unique()):
            single_weekly_results = []
            for j in list(top_trends['Dates'].unique()):
                week_cases = top_trends[(top_trends['Dates'] == j) & (
                    top_trends['Country/Region'] == i)]['Cases'].values
                if len(week_cases) == 0:
                    single_weekly_results.append(0.0)
                else:
                    single_weekly_results.append(np.sum(week_cases))
            topten_weekly_results.append(single_weekly_results)

        orig, log_res, exp_res = [], [], []
        top_three = list(today_top['Country/Region'][:3].values)
        matches = dict(
            zip(list(top_trends['Country/Region'].unique()), topten_weekly_results))
        for name in top_three:
            x = np.arange(len(matches[name]))
            y = matches[name]
            orig.append(y)
            log_res.append(fit_curve(func_type=log, x=x,
                                     y=y, bounds=([-np.inf, np.inf])))
            exp_res.append(fit_curve(func_type=exp, x=x, y=y,
                                     bounds=([0, 0, -100], [100, 0.99, 100])))

        st.markdown("For a logistic curve at the turning point: ")
        st.latex(
            r'''Slope = Growth Factor/2 \Rightarrow\quad Doubling Time (DT) = \dfrac{ln(2)}{Growth Factor/2}''')
        st.markdown("Instead, for an exponential curve: ")
        st.latex(
            r'''Slope = Growth Factor \Rightarrow\quad Doubling Time (DT) = \dfrac{ln(2)}{Growth Factor}''')
        st.markdown("A worked out example, with the results from the top three countries with the most number of Coronavirus Cases right now, is available below.")
        fit_plot(orig, log_res, exp_res, top_three)
