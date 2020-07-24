import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from support.utilities import world_map

# Automatically clear cashes every 24hrs
@st.cache(ttl=86400)
def set_up():
    data = pd.read_csv('data/all.csv')
    up, low = np.inf, 0
    resources = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
                 ]

    data_list, fig, fig2 = world_map(resources, data)

    new = pd.DataFrame([data_list[0]['Country/Region'], data_list[0]['code'],
                        data_list[0]['Dates'], data_list[0].iloc[:, -
                                                                 1], data_list[1].iloc[:, -1],
                        data_list[2].iloc[:, -1]]).transpose()

    df = pd.read_csv(
        'data/API_SH.MED.BEDS.ZS_DS2_en_csv_v2_1120885.csv', skiprows=[0, 1, 2])
    df = df.drop(
        columns=["Country Name", "Indicator Name", "Indicator Code"])
    df.set_index('Country Code', inplace=True)
    df['Beds'] = df.ffill(axis=1).iloc[:, -1]
    df = df[df['Beds'].notna()]
    #df.isnull().mean() * 100
    df = df['Beds']
    merged_one = pd.merge(left=new, right=df,
                          left_on='code', right_on=df.index)
    df2 = pd.read_excel('data/PopulationAgeSex-20200621022821.xlsx',
                        sheet_name='Data', skiprows=[0, 2, 3, 4])
    df2 = df2.drop(
        columns=["ISO 3166-1 numeric code", "Time", "Sex", "Note"])
    df2.Location = [i.lstrip() for i in list(df2.Location.values)]
    merged_one2 = pd.merge(left=merged_one, right=df2,
                           left_on='Country/Region', right_on=df2.Location)
    return merged_one2


def summary_view(name, cases, estimated_cases, recovered, deths):
    fig = make_subplots(rows=1, cols=4,
                        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]])

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=cases,
            title="Cases",
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=estimated_cases,
            title="Estimated Cases",
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=recovered,
            title="Recovered",
        ),
        row=1, col=3
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=deths,
            title="Deaths",
        ),
        row=1, col=4
    )

    fig.update_layout(height=200, width=750, title_text=name+" Summary")
    st.plotly_chart(fig)


def comulative_plot(negatives, positives, survivors, dates_range):
    fig = go.Figure(
        data=[go.Scatter(x=dates_range, y=negatives,
                         mode="lines", name='Cases',
                         line=dict(width=2, color="blue")),
              go.Scatter(x=dates_range, y=positives,
                         mode="lines", name='Recovered',
                         line=dict(width=2, color="green")),
              go.Scatter(x=dates_range, y=survivors,
                         mode="lines", name='Deaths',
                         line=dict(width=2, color="orange"))],
        layout=go.Layout(
            title_text="Comulative Results Over Time", hovermode="closest",
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
    fig.update_yaxes(title_text="Number")
    st.plotly_chart(fig)


def age_population(name, age_dist):
    fig = plt.figure(num=None, figsize=(10, 5), dpi=80,
                     facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)
    ax.bar(range(len(age_dist)), list(age_dist.values()), align='center')
    ax.set_xticks(range(len(age_dist)))
    ax.set_xticklabels(list(age_dist.keys()))
    ax.tick_params(axis="x", labelsize=12, rotation=30)
    ax.tick_params(axis="y", labelsize=12)
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_ylabel("Number of individuals", fontsize=15)
    ax.set_title(name+" Population Age", fontsize=15)
    st.pyplot()


def virus_SEIR_plot(negatives, esposed, positives, survivors, deths, R0, alpha, daily_deths, avoidable_deths):
    fig = make_subplots(rows=3, cols=2,
                        specs=[[{"colspan": 2}, None], [{}, {}], [{"colspan": 2}, None]], horizontal_spacing=0.2,
                        vertical_spacing=0.1)

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=negatives,
                   mode="lines", name='Susceptible',
                   line=dict(width=2, color="blue")),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=esposed,
                   mode="lines", name='Esposed',
                   line=dict(width=2, color="red")),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=positives,
                   mode="lines", name='Infected',
                   line=dict(width=2, color="green")),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=deths,
                   mode="lines", name='Deaths',
                   line=dict(width=2, color="black")),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=survivors,
                   mode="lines", name='Recovered',
                   line=dict(width=2, color="orange")),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=R0,
                   mode="lines", name='R0 Landscape',
                   line=dict(width=2)),
        row=2, col=1)

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=alpha,
                   mode="lines", name='α Landscape',
                   line=dict(width=2)),
        row=2, col=2)

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=daily_deths,
                   mode="lines", name='Daily Deaths',
                   line=dict(width=2)),
        row=3, col=1)

    fig.add_trace(
        go.Scatter(x=[i for i in range(len(negatives))], y=avoidable_deths,
                   mode="lines", name='Avoidable Deaths',
                   line=dict(width=2)),
        row=3, col=1)

    frames = [go.Frame(
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
            y=deths,
            mode="lines",
            line=dict(width=2, color="black")),
            go.Scatter(
            x=[i for i in range(k)],
            y=survivors,
            mode="lines",
            line=dict(width=2, color="orange")),
            go.Scatter(
            x=[i for i in range(k)],
            y=R0,
            mode="lines",
            line=dict(width=2)),
            go.Scatter(
            x=[i for i in range(k)],
            y=alpha,
            mode="lines",
            line=dict(width=2)),
            go.Scatter(
            x=[i for i in range(k)],
            y=daily_deths,
            mode="lines",
            line=dict(width=2)),
            go.Scatter(
            x=[i for i in range(k)],
            y=avoidable_deths,
            mode="lines",
            line=dict(width=2))],
        layout=go.Layout(
            annotations=[dict(
                text="                    R<sub>0</sub>=" +
                str(round(R0[k], 2)),
                showarrow=False,
                arrowhead=0,
                font=dict(
                    color="black",
                    size=18
                ),
                xshift=282,
                yshift=-116
            ),
                dict(
                text="                    α<sub>0</sub>=" +
                    str(round(alpha[k], 3)),
                showarrow=False,
                arrowhead=0,
                font=dict(
                    color="black",
                    size=18
                    ),
                xshift=284,
                yshift=-140)
            ]),

        traces=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        for k in range(len(negatives))]

    fig.frames = frames

    fig.update_layout(updatemenus=[
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
                    "y": 1.25,
                    "yanchor": "top"
        }
    ],)

    fig.update_layout(height=800, width=800,
                      title_text="Coronavirus SEIR Model (Avg R<sub>0</sub>=" + str(round(np.mean(R0), 2)) + ', α=' + str(round(np.mean(alpha), 3)) + ')')
    fig.update_xaxes(title_text="Days", row=1, col=1)
    fig.update_yaxes(title_text="Number of Cases", row=1, col=1)
    fig.update_yaxes(title_text="R<sub>0</sub>", row=2, col=1)
    fig.update_xaxes(title_text="Days",  row=2, col=1)
    fig.update_yaxes(title_text="α", row=2, col=2)
    fig.update_xaxes(title_text="Days",  row=2, col=2)
    fig.update_yaxes(title_text="Number of Deaths", row=3, col=1)
    fig.update_xaxes(title_text="Days",  row=3, col=1)
    st.plotly_chart(fig)


def beds_plot(actual_beds, daily_deths):
    fig = plt.figure(num=None, figsize=(20, 10), dpi=80,
                     facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)
    ax.barh(['Available Beds', 'Needed Beds'], [
            actual_beds, int(max(daily_deths))], align='center')
    ax.tick_params(axis="x", labelsize=22, rotation=30)
    ax.tick_params(axis="y", labelsize=22)
    ax.get_xaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_title("Available vs Needed Beds", fontsize=35)
    st.pyplot()


def comulative_plot2(negatives, survivors, dates_range, r2_res):
    fig = go.Figure(
        data=[go.Scatter(x=dates_range, y=negatives,
                         mode="lines", name='Real Cases Trend',
                         line=dict(width=2, color="blue")),
              go.Scatter(x=dates_range, y=survivors,
                         mode="lines", name='Inferred Trend',
                         line=dict(width=2, color="orange"))],
        layout=go.Layout(
            title_text="Advanced SEIR Parameters Estimation (R2 Score="+str(round(r2_res, 3))+")", hovermode="closest",
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
                y=survivors,
                mode="lines",
                line=dict(width=2, color="orange"))])

                for k in range(len(negatives))],

    )
    fig.update_xaxes(title_text="Number of Days")
    fig.update_yaxes(title_text="Comulative Cases")
    st.plotly_chart(fig)
