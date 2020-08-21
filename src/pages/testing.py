import pandas as pd
import numpy as np
import torch
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import pages.home
import csv
from support.utilities import world_map, world_plot, stats
from support.base_models import SIR_sim, SIR_plot, SEIR_sim, SEIR_plot


def write():
    with st.spinner("Loading Modelling ..."):
        st.title('A/B Testing')
        st.markdown('## Live Feedback A/B Testing')
        st.markdown(
            '''
            In this research study two different type of models have been examined: Agent Based Modelling and Compartmental Modelling. Comparmental Modelling 
            represents the most traditional way to model epidemical developments (Control Group), while Agent Based Modelling offers an alternative view to how to approach this 
            type of problem (Treatment Group). Which of the two approaches do you think would make you feel most sure/confortable to make a decision about possible restrictions to apply?
            '''
        )

        data = pd.read_csv('src/pages/record.csv')
        last_record = list(data.sum(axis=0))
        if st.button('Compartmental Modelling'):
            with open('src/pages/record.csv', 'a') as fd:
                writer = csv.writer(fd)
                writer.writerow([])
                writer.writerow(['1', '0', '0'])
            data = pd.read_csv('src/pages/record.csv')
            last_record = list(data.sum(axis=0))
            st.write(last_record[0])
        if st.button('Agent Based Modelling'):
            with open('src/pages/record.csv', 'a') as fd:
                writer = csv.writer(fd)
                writer.writerow([])
                writer.writerow(['0', '1', '0'])
            data = pd.read_csv('src/pages/record.csv')
            last_record = list(data.sum(axis=0))
            st.write(last_record[1])
        if st.button('Neither'):
            with open('src/pages/record.csv', 'a') as fd:
                writer = csv.writer(fd)
                writer.writerow([])
                writer.writerow(['0', '0', '1'])
            data = pd.read_csv('src/pages/record.csv')
            last_record = list(data.sum(axis=0))
            st.write(last_record[2])
        st.write("Sample Size: ", sum(last_record))

        c_a = last_record[0]/sum(last_record)
        c_b = last_record[1]/sum(last_record)

        st.write("Conversion Rate for Compartmental Modelling: ", c_a)
        st.write("Conversion Rate for Agent Based Modelling: ", c_b)
