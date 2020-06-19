import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
import pages.world_view
import pages.home


def summary_view(data_list):
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]])

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=sum(data_list[0].iloc[:, -2]),
            title="Cases",
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=sum(data_list[1].iloc[:, -2]),
            title="Recovered",
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=sum(data_list[2].iloc[:, -2]),
            title="Deaths",
        ),
        row=1, col=3
    )

    fig.update_layout(height=200, width=600, title_text="Today Summary")
    # st.plotly_chart(fig)
    return fig


def header_view(data_list):
    message = data_list[0]["Country/Region"] + "<br>"
    message += "Confirmed: " + data_list[0].iloc[:, -2].astype(str)

    fig2 = go.Figure(data=go.Scattergeo(
        locationmode="country names",
        lon=data_list[0]["Long"],
        lat=data_list[0]["Lat"],
        hovertext=message,
        showlegend=False,
        marker=dict(
            size=7,
            opacity=0.9,
            reversescale=True,
            autocolorscale=True,
            line=dict(
                width=1,
            ),
            cmin=0,
            color=data_list[0].iloc[:, -3],
            cmax=max(data_list[0].iloc[:, -3]),
            colorbar_title="Live Confirmed Cases",
        )),
    )

    fig2.update_layout(
        title="COVID-19 Worldwide Cases",
        showlegend=True,
        legend=dict(x=0.65, y=0.8),
        geo=dict(
            projection_type="orthographic",
            showcoastlines=True,
            showland=True,
            showocean=True,
            lakecolor="LightBlue"
        ),
    )

    # st.plotly_chart(fig)
    return fig2

# Automatically clear cashes every 24hrs
@st.cache(ttl=86400)
def world_map(resources, df2):
    datasets = []
    for link in resources:
        df = pd.read_csv(link)
        df = df[df['Country/Region'] != 'Diamond Princess']
        df = df[df['Country/Region'] != 'MS Zaandam']
        if len(datasets) == 0:
            fig2 = header_view([df])
        df = df.drop(['Province/State'], axis=1)
        df = df.reset_index(drop=True)
        df = df.groupby('Country/Region').sum()
        df = df.reset_index()
        df.loc[df.loc[df['Country/Region'] == 'US'].index,
               'Country/Region'] = 'United States of America'
        df.loc[df.loc[df['Country/Region'] == 'United Kingdom'].index,
               'Country/Region'] = 'United Kingdom of Great Britain and Northern Ireland'
        df.loc[df.loc[df['Country/Region'] == 'Russia'].index,
               'Country/Region'] = 'Russian Federation'
        df.loc[df.loc[df['Country/Region'] == 'Venezuela'].index,
               'Country/Region'] = 'Venezuela (Bolivarian Republic of)'
        df.loc[df.loc[df['Country/Region'] == 'Bolivia'].index,
               'Country/Region'] = 'Bolivia (Plurinational State of)'
        df.loc[df.loc[df['Country/Region'] == 'Taiwan*'].index,
               'Country/Region'] = 'Taiwan, Province of China'
        df.loc[df.loc[df['Country/Region'] == 'Syria'].index,
               'Country/Region'] = 'Syrian Arab Republic'
        df.loc[df.loc[df['Country/Region'] == 'Korea, South'].index,
               'Country/Region'] = 'Korea, Republic of'
        df.loc[df.loc[df['Country/Region'] == 'Iran'].index,
               'Country/Region'] = 'Iran (Islamic Republic of)'
        df.loc[df.loc[df['Country/Region'] == 'Cote d\'Ivoire'].index,
               'Country/Region'] = 'Côte d\'Ivoire'
        df.loc[df.loc[df['Country/Region'] ==
                      'Congo (Kinshasa)'].index, 'Country/Region'] = 'Congo, Democratic Republic of the'
        df.loc[df.loc[df['Country/Region'] ==
                      'Congo (Brazzaville)'].index, 'Country/Region'] = 'Congo'
        df.loc[df.loc[df['Country/Region'] == 'Moldova'].index,
               'Country/Region'] = 'Moldova, Republic of'
        df.loc[df.loc[df['Country/Region'] == 'Tanzania'].index,
               'Country/Region'] = 'Tanzania, United Republic of'
        df.loc[df.loc[df['Country/Region'] == 'Brunei'].index,
               'Country/Region'] = 'Brunei Darussalam'
        code2 = []
        for i in df['Country/Region']:
            try:
                code2.append(df2[df2['name'] == i]['alpha-3'].values[0])
            except:
                code2.append('NA')

        df['code'] = code2
        df.loc[df.loc[df['Country/Region'] == 'United Kingdom of Great Britain and Northern Ireland'].index,
               'Country/Region'] = 'United Kingdom'
        datasets.append(df)

    fig = summary_view(datasets)

    for i in range(len(datasets)):
        datasets[i] = datasets[i].drop(
            ['Lat', 'Long'], axis=1)
        datasets[i] = datasets[i].melt(
            id_vars=["Country/Region", "code"],
            var_name="Dates",
            value_name="Cases")

    return datasets, fig, fig2


def world_plot(df, up, low, name):
    fig = px.choropleth(df, locations="code", hover_name="Country/Region",
                        animation_frame="Dates",
                        color_continuous_scale=px.colors.sequential.Viridis[::-1],
                        color="Cases",
                        title="Covid-19 World "+str(name),
                        range_color=[low, up])
    st.plotly_chart(fig)


def stats(countries, infected, died, title):
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.set_size_inches(18.5, 10.5)

    x = list(countries.values)

    n_cases = list(infected.values)
    ax[0].barh(x, n_cases, color='green')
    ax[0].set_xlabel("Number of Cases", fontsize=25)

    n_deths = list(died.values)
    ax[1].barh(x, n_deths, color='green')
    ax[1].set_xlabel("Number of Deths", fontsize=25)

    ax[1].set_yticks(x, [])
    ax[1].invert_yaxis()
    ax[0].set_yticklabels(x, fontsize=22)

    ax[0].tick_params(axis="x", labelsize=20, rotation=30)
    ax[1].tick_params(axis="x", labelsize=20, rotation=30)
    ax[0].get_xaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax[1].get_xaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    fig.suptitle(title, fontsize=30)
    fig.tight_layout()
    fig.subplots_adjust(top=0.92)
    st.pyplot()
