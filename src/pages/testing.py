import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import pages.home
import csv
import scipy.stats as scs


def write():
    with st.spinner("Loading Modelling ..."):
        st.title('A/B Testing')
        st.markdown('## Live Feedback A/B Testing')
        st.markdown(
            '''
            In this research study two different type of models have been examined: Agent Based Modelling and Compartmental Modelling. Compartmental Modelling
            represents the most traditional way (and gold standard) to model epidemical developments (Control Group), while Agent Based Modelling offers an alternative view to how to approach this
            type of problem (Treatment Group).
            - **Compartmental Modelling:** SIR and SEIR Modelling, Advanced SEIR Modelling, Vaccination Modelling, Coronavirus Modelling.
            - **Agent Based Modelling:** Population Modelling, Track and Trace, Central Hubs, Finance Simulation.

            Which of the two approaches do you think would make you feel most confortable to make a decision about possible interventions to apply (aiding your decision making)?

            You can express just a single vote, subsequent ones will be automatically discarded.
            '''
        )

        data = pd.read_csv('src/pages/record.csv')
        last_record = list(data.sum(axis=0))
        ba = st.button('Compartmental Modelling')
        if ba:
            f = open("src/pages/vote.txt", "r")
            status = int(f.read())
            f.close()
            if status == 0:
                with open('src/pages/record.csv', 'a') as fd:
                    writer = csv.writer(fd)
                    writer.writerow([])
                    writer.writerow(['1', '0'])
                data = pd.read_csv('src/pages/record.csv')
                last_record = list(data.sum(axis=0))
                f = open("src/pages/vote.txt", "w")
                f.write("1")
                f.close()
            st.write(last_record[0])
        bb = st.button('Agent Based Modelling')
        if bb:
            f = open("src/pages/vote.txt", "r")
            status = int(f.read())
            f.close()
            if status == 0:
                with open('src/pages/record.csv', 'a') as fd:
                    writer = csv.writer(fd)
                    writer.writerow([])
                    writer.writerow(['0', '1'])
                data = pd.read_csv('src/pages/record.csv')
                last_record = list(data.sum(axis=0))
                f = open("src/pages/vote.txt", "w")
                f.write("1")
                f.close()
            st.write(last_record[1])
        st.write("Sample Size (logged responses): ",
                 round(sum(last_record), 3))
        if ba == False and bb == False:
            pass
        else:
            c_a = last_record[0]/sum(last_record)
            c_b = last_record[1]/sum(last_record)

            cr_uplift = (c_b - c_a) / c_a
            se_a, se_b = np.sqrt((c_a * (1 - c_a)) / sum(last_record)
                                 ), np.sqrt((c_b * (1 - c_b)) / sum(last_record))
            se_diff = np.sqrt(se_a**2 + se_b**2)
            z_score = (c_b - c_a) / se_diff
            p_value = 1 - scs.norm(0, 1).cdf(z_score)

            sides = st.radio("Type of Hypotesys", ('One Sided', 'Two Sided'))
            if sides == 'One Sided':
                sided = 0
            else:
                sided = 1

            interval = st.slider("Required Confidence: ",
                                 min_value=0.0, max_value=1.0,
                                 value=0.9, step=0.01)

            x_a = np.linspace(last_record[0]-49, last_record[0]+50, 100)
            y_a = scs.binom(sum(last_record), c_a).pmf(x_a)
            x_b = np.linspace(last_record[1]-49, last_record[1]+50, 100)
            y_b = scs.binom(sum(last_record), c_b).pmf(x_b)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_a, y=y_a,
                                     mode='lines',
                                     name='Control Group'))
            fig.add_trace(go.Scatter(x=x_b, y=y_b,
                                     mode='lines',
                                     name='Treatment Group'))
            fig.update_layout(
                title_text="Binomial Distribution Representation of Control and Treatment Groups")
            fig.update_xaxes(title="Count of Possible Outcomes")
            fig.update_yaxes(title="Probability")
            fig.update_layout(
                autosize=False,
                width=700,
                height=500,
            )
            st.plotly_chart(fig)

            st.write("Conversion Rate for Compartmental Modelling: ",
                     round(c_a*100, 3),  "%")
            st.write("Conversion Rate for Agent Based Modelling: ",
                     round(c_b*100, 3),  "%")

            st.write("Relative Uplift: ", round(cr_uplift*100, 3),  "%")
            st.write("Z Score: ", round(z_score, 3))
            st.write("P Value: ", round(p_value, 3))

            if ((p_value < (1 - interval) and sided == 0) or ((p_value > (interval + (1 - interval)/2) or p_value < (1 - interval - (1 - interval)/2)) and sided == 1)):
                st.write("Statistically significant: ", True)
            else:
                st.write("Statistically significant: ", False)
