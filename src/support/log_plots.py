import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
pd.options.mode.chained_assignment = None
colorscale = px.colors.cyclical.HSV


def process_data(data_list, today_top):
    top_trends = data_list[0][data_list[0]
                              ['Country/Region'].isin(list(today_top['Country/Region'].unique()))]
    top_trends['Dates'] = pd.to_datetime(top_trends['Dates'])
    top_trends['Week_Number'] = top_trends['Dates'].dt.week
    topten_weekly_results = []
    for i in list(top_trends['Country/Region'].unique()):
        single_weekly_results = []
        for j in list(top_trends['Week_Number'].unique()):
            week_cases = top_trends[(top_trends['Week_Number'] == j) & (
                top_trends['Country/Region'] == i)]['Cases'].values
            if len(week_cases) == 0:
                single_weekly_results.append(0.0)
            else:
                single_weekly_results.append(np.mean(week_cases))
        topten_weekly_results.append(single_weekly_results)
    return top_trends, topten_weekly_results


def exponential_view(top_trends, topten_weekly_results):
    plot_data = []
    for i, j in zip(range(len(topten_weekly_results)), list(top_trends['Country/Region'].unique())):
        plot_data.append(go.Scatter(x=[i for i in range(len(topten_weekly_results[i]))],
                                    y=topten_weekly_results[i],
                                    mode="lines",
                                    name=j,
                                    line=dict(color=colorscale[i], width=2)))

    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title_text="Averaged Weekly Cases over time", hovermode="closest",
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 200, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 100,
                                                           "easing": "quadratic-in-out"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        dict(label="Linear",
                             method="relayout",
                             args=[{"yaxis.type": "linear"}]),
                        dict(label="Log",
                             method="relayout",
                             args=[{"yaxis.type": "log"}]),
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.27,
                    "xanchor": "right",
                    "y": 1.5,
                    "yanchor": "top"
                }
            ]),

        frames=[go.Frame(
            data=[
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[0],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[1],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[2],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[3],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[4],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[5],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[6],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[7],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[8],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in range(k)],
                    y=topten_weekly_results[9],
                    mode="lines")
            ]) for k in range(len(topten_weekly_results[9]))],

    )

    fig.update_layout(height=500, width=800, yaxis_type="log")
    fig.update_xaxes(title_text="Year Week Number")
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)


def log_view(top_trends, list_weekly_cases, list_cases_change):
    plot_data = []
    for i, j in zip(range(len(list_weekly_cases)), list(top_trends['Country/Region'].unique())):
        plot_data.append(go.Scatter(x=list_weekly_cases[i],
                                    y=list_cases_change[i],
                                    mode="lines",
                                    name=j,
                                    line=dict(color=colorscale[i], width=2)))

    # Create figure
    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title_text="World Cases Trajectory over time", hovermode="closest",
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 200, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 100,
                                                           "easing": "quadratic-in-out"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        dict(label="Linear",
                             method="relayout",
                             args=[{"yaxis.type": "linear"}]),
                        dict(label="Log",
                             method="relayout",
                             args=[{"yaxis.type": "log"}]),
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.27,
                    "xanchor": "right",
                    "y": 1.5,
                    "yanchor": "top"
                }
            ]),

        frames=[go.Frame(
            data=[
                go.Scatter(
                    x=[i for i in list_weekly_cases[0][:k]],
                    y=list_cases_change[0],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[1][:k]],
                    y=list_cases_change[1],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[2][:k]],
                    y=list_cases_change[2],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[3][:k]],
                    y=list_cases_change[3],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[4][:k]],
                    y=list_cases_change[4],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[5][:k]],
                    y=list_cases_change[5],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[6][:k]],
                    y=list_cases_change[6],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[7][:k]],
                    y=list_cases_change[7],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[8][:k]],
                    y=list_cases_change[8],
                    mode="lines"),
                go.Scatter(
                    x=[i for i in list_weekly_cases[9][:k]],
                    y=list_cases_change[9],
                    mode="lines")
            ]) for k in range(len(list_cases_change[9]))],

    )

    fig.update_layout(height=500, width=800,
                      yaxis_type="log", xaxis_type="log")
    fig.update_xaxes(
        title_text="Average confirmed cases from week To week")
    fig.update_yaxes(title_text="Average number of total cases")
    st.plotly_chart(fig)


# Following: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
# and: https://www.youtube.com/watch?v=54XLXg4fYsc
def log(x, a, b, c, d):
    num = (d - c)
    dem = (1 + a*np.exp(-b*x))
    return c + num/dem


def exp(x, a, b, c):
    return a*np.exp(b*x)+c


def fit_curve(func_type, x, y, bounds):
    popt, pcov = curve_fit(func_type, x, y, bounds=bounds)
    if bounds[0] == -np.inf:
        # For a logistic curve at the turning point, Slope = Growth rate/2 -> doubling time = ln(2) / (Growth rate/2)
        doubling_time = np.log(2)/(popt[1]/2)
    else:
        # For an exponential curve, Slope = Growth rate -> doubling time = ln(2)/Growth rate
        doubling_time = np.log(2)/popt[1]
    # Using R^2 as our metric for goodness of fit
    y_pred = func_type(x, *popt)
    r2_res = r2_score(y, y_pred)
    if r2_res > 0.85:
        return y_pred, r2_res, doubling_time
    else:
        return [None], [None], [None]


def fit_plot(orig, log_res, exp_res, top_three):
    fig, ax = plt.subplots(nrows=1, ncols=3)
    fig.set_size_inches(27.5, 10.5)

    ax[0].plot(orig[0], color='black', label='Original Data', linewidth=3.0)
    if len(log_res[0][0]) != 1:
        ax[0].plot(log_res[0][0], '--', color='red',  label='Logistic ($R^2$=' + str(
            round(log_res[0][1], 2)) + ', \n DT=' + str(round(log_res[0][2], 1)) + ' days)')
    if len(exp_res[0][0]) != 1:
        ax[0].plot(exp_res[0][0], '--', label='Exponential ($R^2$=' + str(
            round(exp_res[0][1], 2)) + ', \n DT=' + str(round(exp_res[0][2], 1)) + ' days)')
    ax[0].set_ylabel("Number of Cases", fontsize=34)
    ax[0].set_title(top_three[0], fontsize=34)
    ax[0].legend(fontsize=27)

    ax[1].plot(orig[1], color='black', label='Original Data', linewidth=3.0)
    if len(log_res[1][0]) != 1:
        ax[1].plot(log_res[1][0], '--', color='red', label='Logistic ($R^2$=' + str(
            round(log_res[1][1], 2)) + ', \n DT=' + str(round(log_res[1][2], 1)) + ' days)')
    if len(exp_res[1][0]) != 1:
        ax[1].plot(exp_res[1][0], '--', label='Exponential ($R^2$=' + str(
            round(exp_res[1][1], 2)) + ', \n DT=' + str(round(exp_res[1][2], 1)) + ' days)')
    ax[1].set_xlabel("Days", fontsize=34)
    ax[1].set_title(top_three[1], fontsize=34)
    ax[1].legend(fontsize=27)

    ax[2].plot(orig[2], color='black', label='Original Data', linewidth=3.0)
    if len(log_res[2][0]) != 1:
        ax[2].plot(log_res[2][0], '--', color='red', label='Logistic ($R^2$=' + str(
            round(log_res[2][1], 2)) + ', \n DT=' + str(round(log_res[2][2], 1)) + ' days)')
    if len(exp_res[2][0]) != 1:
        ax[2].plot(exp_res[2][0], '--', label='Exponential ($R^2$=' + str(
            round(exp_res[2][1], 2)) + ', \n DT=' + str(round(exp_res[2][2], 1)) + ' days)')
    ax[2].set_title(top_three[2], fontsize=34)
    ax[2].legend(fontsize=27)

    ax[0].tick_params(axis="x", labelsize=20)
    ax[1].tick_params(axis="x", labelsize=20)
    ax[2].tick_params(axis="x", labelsize=20)
    ax[0].tick_params(axis="y", labelsize=20)
    ax[1].tick_params(axis="y", labelsize=20)
    ax[2].tick_params(axis="y", labelsize=20)

    fig.suptitle('Logistic/Exponential Curve Fitting', fontsize=34)
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)
    st.pyplot()
