import pandas as pd
import numpy as np
from scipy.integrate import odeint
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st


def timed_sir_step_ahead(y, t, N, beta, gamma, v):
    S, I, R = y
    dsdt = -beta * I * (S / N) + v*R
    didt = beta * I * (S / N) - gamma * I
    drdt = gamma * I - v*R
    return dsdt, didt, drdt


def timed_SIR_sim(N, sim_days, orig_infected, prob_infect, contact_with_people, days, immu_days):
    y0 = N-orig_infected, orig_infected, 0
    beta = prob_infect*contact_with_people
    gamma = 1.0 / days
    v = 1.0/immu_days
    R0 = beta/gamma
    t = np.linspace(0, sim_days-1, sim_days)
    sim_res = odeint(timed_sir_step_ahead, y0, t, args=(N, beta, gamma, v))
    S, I, R = sim_res.T
    return S, I, R, R0


def timed_SIR_plot(negatives, positives, survivors, R0):
    fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(len(negatives))], y=negatives,
                         mode="lines", name='Susceptible',
                         line=dict(width=2, color="blue")),
              go.Scatter(x=[i for i in range(len(negatives))], y=positives,
                         mode="lines", name='Infected',
                         line=dict(width=2, color="green")),
              go.Scatter(x=[i for i in range(len(negatives))], y=survivors,
                         mode="lines", name='Recovered',
                         line=dict(width=2, color="orange"))],
        layout=go.Layout(
            title_text="Time Limited Immunity SIR Model (R<sub>0</sub>=" + str(round(R0, 2))+')', hovermode="closest",
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 100, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 10,
                                                           "easing": "quadratic-in-out"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.14,
                    "xanchor": "right",
                    "y": 1.65,
                    "yanchor": "top"
                }
            ]),

        frames=[go.Frame(
            data=[go.Scatter(
                x=[i for i in range(k)],
                y=negatives,
                mode="lines",
                line=dict(width=2, color="blue")),
                go.Scatter(
                x=[i for i in range(k)],
                y=positives,
                mode="lines",
                line=dict(width=2, color="green")),
                go.Scatter(
                x=[i for i in range(k)],
                y=survivors,
                mode="lines",
                line=dict(width=2, color="orange"))])

                for k in range(len(negatives))],

    )
    fig.update_xaxes(title_text="Number of Days")
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)


def vacc_start(t, start, p, S):
    if t >= start:
        res = p*S
    else:
        res = 0
    return res


def vacc_sir_step_ahead(y, t, N, beta, gamma, v, start_date, p, alpha, rho):
    S, V, I, R, D = y
    vacc = vacc_start(t, start_date, p, S)
    dsdt = -beta * I * (S / N) + v*R - vacc
    dvdt = vacc
    didt = beta * I * (S / N) - (1-alpha)*gamma*I - alpha*rho*I
    drdt = (1-alpha)*gamma*I - v*R
    dddt = alpha * rho * I
    return dsdt, dvdt, didt, drdt, dddt


def vacc_SIR_sim(N, sim_days, orig_infected, prob_infect, contact_with_people, days, immu_days, start_date, p, alpha, death_days):
    y0 = N-orig_infected, 0, orig_infected, 0, 0
    beta = prob_infect*contact_with_people
    gamma = 1.0 / days
    v = 1.0/immu_days
    rho = 1.0/death_days
    R0 = beta/gamma
    t = np.linspace(0, sim_days-1, sim_days)
    sim_res = odeint(vacc_sir_step_ahead, y0, t, args=(
        N, beta, gamma, v, start_date, p, alpha, rho))
    S, V, I, R, D = sim_res.T
    return S, V, I, R, D, R0


def vacc_SIR_plot(negatives, vaccinated, positives, survivors, deths, R0):
    fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(len(negatives))], y=negatives,
                         mode="lines", name='Susceptible',
                         line=dict(width=2, color="blue")),
              go.Scatter(x=[i for i in range(len(negatives))], y=vaccinated,
                         mode="lines", name='Vaccinated',
                         line=dict(width=2, color="red")),
              go.Scatter(x=[i for i in range(len(negatives))], y=positives,
                         mode="lines", name='Infected',
                         line=dict(width=2, color="green")),
              go.Scatter(x=[i for i in range(len(negatives))], y=survivors,
                         mode="lines", name='Recovered',
                         line=dict(width=2, color="orange")),
              go.Scatter(x=[i for i in range(len(negatives))], y=deths,
                         mode="lines", name='Deaths',
                         line=dict(width=2, color="black")), ],
        layout=go.Layout(
            title_text="Vaccination and Time Limited Immunity SIR Model (R<sub>0</sub>=" + str(round(R0, 2))+')', hovermode="closest",
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 100, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 10,
                                                           "easing": "quadratic-in-out"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.14,
                    "xanchor": "right",
                    "y": 1.65,
                    "yanchor": "top"
                }
            ]),

        frames=[go.Frame(
            data=[go.Scatter(
                x=[i for i in range(k)],
                y=negatives,
                mode="lines",
                line=dict(width=2, color="blue")),
                go.Scatter(
                x=[i for i in range(k)],
                y=vaccinated,
                mode="lines",
                line=dict(width=2, color="red")),
                go.Scatter(
                x=[i for i in range(k)],
                y=positives,
                mode="lines",
                line=dict(width=2, color="green")),
                go.Scatter(
                x=[i for i in range(k)],
                y=survivors,
                mode="lines",
                line=dict(width=2, color="orange")),
                go.Scatter(
                x=[i for i in range(k)],
                y=deths,
                mode="lines",
                line=dict(width=2, color="black"))])

                for k in range(len(negatives))],

    )
    fig.update_xaxes(title_text="Number of Days")
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)
