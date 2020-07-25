import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from datetime import timedelta, datetime
import matplotlib.dates as mdates
import utils as ut
import argparse

parser = argparse.ArgumentParser(description="SIR Time Series Estimation")
parser.add_argument(
    "--country",
    default="Germany",
    help="Country of choice for fitting and prediction (default: Germany)",
)
parser.add_argument(
    "--days", default=30, help="Number of days to predict (default: 30)"
)
parser.add_argument(
    "--s0",
    default=210000,
    help="Number of individuals initially suceptible (default: 210000)",
)
parser.add_argument(
    "--i0", default=2, help="Number of individuals initially infected (default: 2)"
)
choice = parser.parse_args()

df2 = pd.read_csv("../data/all.csv")
resources = [
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
]

data_list = ut.world_map(resources, df2)

data_list[0].set_index("Dates", inplace=True)
data_list[1].set_index("Dates", inplace=True)
data_list[2].set_index("Dates", inplace=True)

print("Using as Parameters: ")
params = []
for k in choice.__dict__:
    params.append(choice.__dict__[k])
    print(k, ":", choice.__dict__[k])

df = ut.SIR_series(
    data_list=data_list, place=params[0], days=params[1], s0=params[2], i0=params[3]
)

ut.sir_pred_plot(df, choice.country)
