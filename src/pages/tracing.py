import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def write():
    with st.spinner("Loading Track and Tracing ..."):
        st.title("Track and Tracing")
        st.write(
            """
                Track and Tracing can be considered to be the most effective approach in order to take under control a pandemic.
                Although, one of the main limitations of this approach, is that in less lethal deseases it might be difficult to correctly identify in time all the individuals infected (some might be asyntomatic).
            """
        )
