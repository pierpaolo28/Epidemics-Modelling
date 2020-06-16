import pandas as pd
import numpy as np
import torch
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt


def write():
    with st.spinner("Loading Modelling ..."):
        st.title("Population Modelling")