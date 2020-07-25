import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from datetime import timedelta, datetime
import matplotlib.dates as mdates


def world_map(resources, df2):
    datasets = []
    for link in resources:
        df = pd.read_csv(link)
        df = df[df["Country/Region"] != "Diamond Princess"]
        df = df[df["Country/Region"] != "MS Zaandam"]
        df = df.drop(["Province/State"], axis=1)
        df = df.reset_index(drop=True)
        df = df.groupby("Country/Region").sum()
        df = df.reset_index()
        df.loc[
            df.loc[df["Country/Region"] == "US"].index, "Country/Region"
        ] = "United States of America"
        df.loc[
            df.loc[df["Country/Region"] == "United Kingdom"].index, "Country/Region"
        ] = "United Kingdom of Great Britain and Northern Ireland"
        df.loc[
            df.loc[df["Country/Region"] == "Russia"].index, "Country/Region"
        ] = "Russian Federation"
        df.loc[
            df.loc[df["Country/Region"] == "Venezuela"].index, "Country/Region"
        ] = "Venezuela (Bolivarian Republic of)"
        df.loc[
            df.loc[df["Country/Region"] == "Bolivia"].index, "Country/Region"
        ] = "Bolivia (Plurinational State of)"
        df.loc[
            df.loc[df["Country/Region"] == "Taiwan*"].index, "Country/Region"
        ] = "Taiwan, Province of China"
        df.loc[
            df.loc[df["Country/Region"] == "Syria"].index, "Country/Region"
        ] = "Syrian Arab Republic"
        df.loc[
            df.loc[df["Country/Region"] == "Korea, South"].index, "Country/Region"
        ] = "Korea, Republic of"
        df.loc[
            df.loc[df["Country/Region"] == "Iran"].index, "Country/Region"
        ] = "Iran (Islamic Republic of)"
        df.loc[
            df.loc[df["Country/Region"] == "Cote d'Ivoire"].index, "Country/Region"
        ] = "Côte d'Ivoire"
        df.loc[
            df.loc[df["Country/Region"] == "Congo (Kinshasa)"].index, "Country/Region"
        ] = "Congo, Democratic Republic of the"
        df.loc[
            df.loc[df["Country/Region"] == "Congo (Brazzaville)"].index,
            "Country/Region",
        ] = "Congo"
        df.loc[
            df.loc[df["Country/Region"] == "Moldova"].index, "Country/Region"
        ] = "Moldova, Republic of"
        df.loc[
            df.loc[df["Country/Region"] == "Tanzania"].index, "Country/Region"
        ] = "Tanzania, United Republic of"
        df.loc[
            df.loc[df["Country/Region"] == "Brunei"].index, "Country/Region"
        ] = "Brunei Darussalam"
        code2 = []
        for i in df["Country/Region"]:
            try:
                code2.append(df2[df2["name"] == i]["alpha-3"].values[0])
            except:
                code2.append("NA")

        df["code"] = code2
        df.loc[
            df.loc[
                df["Country/Region"]
                == "United Kingdom of Great Britain and Northern Ireland"
            ].index,
            "Country/Region",
        ] = "United Kingdom"
        datasets.append(df)

    for i in range(len(datasets)):
        datasets[i] = datasets[i].drop(["Lat", "Long"], axis=1)
        datasets[i] = datasets[i].melt(
            id_vars=["Country/Region", "code"], var_name="Dates", value_name="Cases"
        )

    return datasets


def SIR(t, y, beta, gamma):
    S, I, R = y
    dsdt = -beta * I * S
    didt = beta * I * S - gamma * I
    drdt = gamma * I
    return dsdt, didt, drdt


def time_extend_index(index, new_size):
    values = index.values
    current = datetime.strptime(index[-1], "%m/%d/%y")
    while len(values) < new_size:
        current = current + timedelta(days=1)
        values = np.append(values, datetime.strftime(current, "%m/%d/%y"))
    return values


def predict(beta, gamma, cases, recovered, place, days, s0, i0, r0):
    new_index = time_extend_index(cases.index, days)
    extended = []
    for i in [cases, recovered]:
        extended.append(
            np.concatenate((i.values, [None] * (len(new_index) - len(i.values))))
        )
    step = solve_ivp(
        SIR,
        [0, len(new_index)],
        [s0, i0, r0],
        args=(beta, gamma),
        t_eval=np.arange(0, len(new_index), 1),
    )
    return new_index, extended, step


def loss(point, cases, recovered, s0, i0, r0):
    beta, gamma = point
    alpha = 0.1
    solution = solve_ivp(
        SIR,
        [0, len(cases)],
        [s0, i0, r0],
        args=(beta, gamma),
        t_eval=np.arange(0, len(cases), 1),
        vectorized=True,
    )
    l1 = np.sqrt(np.mean((solution.y[1] - cases) ** 2))
    l2 = np.sqrt(np.mean((solution.y[2] - recovered) ** 2))
    return alpha * l1 + (1 - alpha) * l2


def SIR_series(data_list, place, days, s0, i0):
    r0 = 0
    cases = (
        data_list[0][data_list[0]["Country/Region"] == place]["Cases"]
        - data_list[1][data_list[1]["Country/Region"] == place]["Cases"]
    )
    recovered = data_list[1][data_list[1]["Country/Region"] == place]["Cases"]
    days = len(cases.index) + days
    optimal = minimize(
        loss,
        [0.001, 0.001],
        args=(cases, recovered, s0, i0, r0),
        method="L-BFGS-B",
        bounds=[(0.00000001, 0.4), (0.00000001, 0.4)],
    )
    print(optimal)
    beta, gamma = optimal.x
    print(
        f"country={place}, beta={beta:.8f}, gamma={gamma:.8f}, r_0:{(beta/gamma):.8f}"
    )
    new_index, extended, prediction = predict(
        beta, gamma, cases, recovered, place, days, s0, i0, r0
    )
    df = pd.DataFrame(
        {
            "Infected": prediction.y[1],
            "Infected (Data)": extended[0],
            "Recovered": prediction.y[2],
            "Recovered (Data)": extended[1],
        },
        index=new_index,
    )
    return df


def sir_pred_plot(df, place):
    plt.figure(num=None, figsize=(10, 6), dpi=80, facecolor="w", edgecolor="k")
    new_x = mdates.datestr2num(df.index)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
    plt.plot(new_x, df["Infected"].values, label="Infected")
    plt.plot(new_x, df["Infected (Data)"].values, label="Infected (Data)")
    plt.plot(new_x, df["Recovered"].values, label="Recovered")
    plt.plot(new_x, df["Recovered (Data)"].values, label="Recovered (Data)")
    plt.gcf().autofmt_xdate()
    plt.legend(fontsize=14)
    plt.title("SIR " + str(place) + " Forecasting", fontsize=20)
    plt.xlabel("Days", fontsize=18)
    plt.ylabel("Number of cases", fontsize=18)
    plt.savefig(place + "_preds.svg", format="svg", bbox_inches="tight")
    plt.show()
