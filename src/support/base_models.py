import streamlit as st
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def sir_step_ahead(y, t, N, beta, gamma):
    S, I, R = y
    dsdt = -beta * I * (S / N)
    didt = beta * I * (S / N) - gamma * I
    drdt = gamma * I
    return dsdt, didt, drdt


def SIR_sim(N, sim_days, orig_infected, prob_infect, contact_with_people, days):
    y0 = N-orig_infected, orig_infected, 0
    beta = prob_infect*contact_with_people
    gamma = 1.0 / days
    R0 = beta/gamma
    t = np.linspace(0, sim_days-1, sim_days)
    sim_res = odeint(sir_step_ahead, y0, t, args=(N, beta, gamma))
    S, I, R = sim_res.T
    return S, I, R, R0


def SIR_plot(negatives, positives, survivors, R0):
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
            title_text="Standard SIR Model (R<sub>0</sub>=" + str(round(R0, 2))+')', hovermode="closest",
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


def seir_step_ahead(y, t, N, beta, gamma, delta):
    S, E, I, R = y
    dsdt = -beta * I * (S / N)
    dedt = beta * I * (S / N) - delta * E
    didt = delta * E - gamma * I
    drdt = gamma * I
    return dsdt, dedt, didt, drdt


def SEIR_sim(N, sim_days, orig_esposed, prob_infect, contact_with_people, days, inc_days):
    y0 = N-orig_esposed, orig_esposed, 0, 0
    beta = prob_infect*contact_with_people
    gamma = 1.0 / days
    delta = 1.0 / inc_days
    R0 = beta/gamma
    t = np.linspace(0, sim_days-1, sim_days)
    sim_res = odeint(seir_step_ahead, y0, t, args=(N, beta, gamma, delta))
    S, E, I, R = sim_res.T
    return S, E, I, R, R0


def SEIR_plot(negatives, esposed, positives, survivors, R0):
    fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(len(negatives))], y=negatives,
                         mode="lines", name='Susceptible',
                         line=dict(width=2, color="blue")),
              go.Scatter(x=[i for i in range(len(negatives))], y=esposed,
                         mode="lines", name='Esposed',
                         line=dict(width=2, color="red")),
              go.Scatter(x=[i for i in range(len(negatives))], y=positives,
                         mode="lines", name='Infected',
                         line=dict(width=2, color="green")),
              go.Scatter(x=[i for i in range(len(negatives))], y=survivors,
                         mode="lines", name='Recovered',
                         line=dict(width=2, color="orange"))],
        layout=go.Layout(
            title_text="Standard SEIR Model (R<sub>0</sub>=" + str(round(R0, 2))+')', hovermode="closest",
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
                y=esposed,
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
                line=dict(width=2, color="orange"))])

                for k in range(len(negatives))],

    )
    fig.update_xaxes(title_text="Number of Days")
    fig.update_yaxes(title_text="Number of Cases")
    st.plotly_chart(fig)
