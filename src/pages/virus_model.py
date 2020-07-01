import pandas as pd
import numpy as np
import torch
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
from scipy import integrate, optimize
from sklearn.metrics import r2_score
import pages.home
import support.virus_utilities as vir
import support.advanced_models as ad
import math

millnames = ['', ' thousands', ' millions', ' billions', ' trillions']
# https://stackoverflow.com/questions/3154460/python-human-readable-large-numbers


def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames)-1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def write():
    with st.spinner("Loading Coronavirus Modelling ..."):
        st.title('Coronavirus Modelling')

        merged_one2 = vir.set_up()

        country_name = st.selectbox("Choose the country to analyse",
                                    list(merged_one2['Country/Region'].unique()))

        dates_range = list(
            merged_one2[merged_one2['Country/Region'] == country_name]['Dates'])
        cases = merged_one2[merged_one2['Country/Region']
                            == country_name].iloc[:, 3].values
        recovered = merged_one2[merged_one2['Country/Region']
                                == country_name].iloc[:, 4].values
        deths = merged_one2[merged_one2['Country/Region']
                            == country_name].iloc[:, 5].values
        population = int(sum(
            merged_one2[merged_one2['Country/Region'] == country_name].values[0][8:])*1000)
        country_latest = list(merged_one2[(merged_one2['Country/Region'] == country_name) & (
            merged_one2['Dates'] == list(merged_one2['Dates'].unique())[::-1][0])].values[0])
        cum_cases = country_latest[3]
        cum_recovered = country_latest[4]
        cum_deths = country_latest[5]
        beds = int(country_latest[6]*population/1000)
        age_dist = dict(zip(list(merged_one2.columns[8:]),
                            [int(i) for i in list(merged_one2[merged_one2['Country/Region'] == country_name].values[0][8:]*1000)]))
        age_props = dict(zip(list(merged_one2.columns[8:]), np.array(
            list(age_dist.values()))/population))
        # https://science.sciencemag.org/content/368/6490/489
        true_cum_cases = cum_cases/0.14
        likelihood_to_get_it = (true_cum_cases/population)*100

        vir.summary_view(country_name, cum_cases, true_cum_cases,
                         cum_recovered, cum_deths)

        st.write(str(country_name) + " has currently a population of " +
                 str(millify(population)) + " of abitants and " + str(millify(beds)) + ' hospital beds. ' +
                 "According the total estimated cases and overall population, the likelihood that an abitant might become positive to Coronavirus is currently equal to " + str(round(likelihood_to_get_it, 2)) + "%." +
                 " In the figure below is available " + str(country_name) + " response record since the beginning of the outbreak.")

        vir.comulative_plot(cases,  recovered,  deths, dates_range)

        st.write(str(country_name) + " population age distribution is available below. This population distribution will then be used in order to design the SEIR model.")

        vir.age_population(country_name, age_dist)

        st.write("Using the informations specifically provided for " + str(country_name) + " we are now going to use the 'Advanced SEIR Modelling' model introduced in the previous section in order to identify the best possible response to Coronavirus for this country. Given the information provided by the number of hospital beds available in this country, we can also keep track of when during the simulation the number of deths can be directly caused by the lack of health assistance (eg. at the curve peak the health system might get overwhelmed). In this model, has additionally been taken into account that a portion of the available beds might be already taken by other patients for non-coronavirus related causes.")

        sim_days = st.slider("Number of days: ",
                             min_value=2, max_value=500,
                             value=150, step=10)
        orig_infected = population/100
        days = st.selectbox("Number of days the disease can last", [
                            14, 7, 10, 21, 28])

        inc_days = st.selectbox("Number of incubation days for the disease", [
                                float(i) for i in range(1, days, 3)])

        death_days = st.selectbox("Number of days the disease can take to become lethal", [
            float(i) for i in range(int(inc_days)+2, days, 2)])

        age_based_alpha = [0.003, 0.002, 0.001, 0.005, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02, 0.03, 0.03,
                           0.04, 0.05, 0.07, 0.07, 0.08, 0.1, 0.1, 0.12, 0.199]
        pop_age_prop = list(age_props.values())
        opt_alpha = sum([i*j for i, j in zip(age_based_alpha, pop_age_prop)])

        scaling = st.slider("How much weight should older age have on the death rate?",
                            min_value=0.001, max_value=1.0,
                            value=0.5, step=0.01)

        beds_already_taken = st.slider("Percentage of beds already taken for non-coronavirus related disease",
                                       min_value=0.1, max_value=1.0,
                                       value=0.3, step=0.01)

        land = st.radio("What's landscape should R follow?",
                        ('Sigmoid', 'Sinusoidal'))
        if land == 'Sigmoid':
            x = st.slider("From what day social distancing measures have been applied?",
                          min_value=0, max_value=sim_days-1,
                          value=25, step=1)
            dec_factor = st.slider("How drasticly rapidly have the restrictions been applied?",
                                   min_value=0.1, max_value=1.0,
                                   value=0.5, step=0.1)
            R0_beg = st.number_input("Maxium possible R value", 1, 14, 4)
            R0_end = st.number_input(
                "Minimum possible R value", 1, R0_beg, 1)
            S, E, I, R, D, R0_time, alpha_time = ad.ad_SEIR_sim(population, sim_days, orig_infected, days,
                                                                inc_days, scaling, opt_alpha, death_days, R0_beg, R0_end, dec_factor, x)
        else:
            scale_factor = st.slider("Sinusoid scaling R value: ",
                                     min_value=0.0, max_value=10.0,
                                     value=0.8, step=0.1)
            S, E, I, R, D, R0_time, alpha_time = ad.ad_SEIR_sim2(population, sim_days, orig_infected, days,
                                                                 inc_days, scaling, opt_alpha, death_days, scale_factor)

        actual_beds = int(beds*(1-beds_already_taken))
        daily_deths = [0]+[D[i]-D[i-1] for i in range(1, len(D))]
        avoidable_deths = []
        for i in daily_deths:
            if i > actual_beds:
                avoidable_deths.append(i-actual_beds)
            else:
                avoidable_deths.append(0)

        vir.virus_SEIR_plot(S, E, I, R, D, R0_time,
                            alpha_time, daily_deths, avoidable_deths)

        st.write("Comparing our current availability of beds against the actual number of beds needed during the peak of the outbreak, we can finally obtain the summary plot available below.")

        vir.beds_plot(actual_beds, daily_deths)

        st.markdown("## Advanced SEIR Parameters Estimation")

        sim_days2 = len(dates_range)
        d = [i for i in range(len(dates_range))]
        null = 0
        for i in range(len(cases)):
            if cases[i] <= 0:
                null += 1
            else:
                break

        def sir_step_ahead(y, d, beta, gamma):
            S, I, R = y
            N = S + I + R
            dsdt = -beta * I * (S / N)
            didt = beta * I * (S / N) - gamma * I
            drdt = gamma * I
            return dsdt, didt, drdt

        def r_time(t, R0_beg, R0_end, dec_factor, x0):
            adaptive_r = ((R0_beg-R0_end) /
                          (1+np.exp(-dec_factor*(-t+x0)))) + R0_end
            return adaptive_r

        def alpha2(scaling, I, N, opt_alpha):
            return scaling * (I/N) + opt_alpha

        def ad_seir_step_ahead(y, t, gamma, delta, scaling, rho, R0_beg, R0_end, dec_factor, x):
            S, E, I, R, D = y
            N = S + E + I + R + D
            r_t = r_time(t, R0_beg, R0_end, dec_factor, x)
            alpha_t = alpha2(scaling, I, N, opt_alpha)
            beta_t = r_t * (1/(alpha_t*(1/rho)+(1-alpha_t)*(1/gamma)))
            dsdt = -beta_t * I * (S / N)
            dedt = beta_t * I * (S / N) - delta * E
            didt = delta * E - (1 - alpha_t) * gamma * I - alpha_t * rho * I
            drdt = (1 - alpha_t) * gamma * I
            dddt = alpha_t * rho * I
            return dsdt, dedt, didt, drdt, dddt

        def r_time2(t, sim_days2, scale_factor):
            return scale_factor*np.sin(t/(sim_days2/10))+scale_factor + 1

        def ad_seir_step_ahead2(y, t, gamma, delta, scaling, rho, scale_factor):
            S, E, I, R, D = y
            N = S + E + I + R + D
            r_t = r_time2(t, sim_days2, scale_factor)
            alpha_t = alpha2(scaling, I, N, opt_alpha)
            beta_t = r_t * (1/(alpha_t*(1/rho)+(1-alpha_t)*(1/gamma)))
            dsdt = -beta_t * I * (S / N)
            dedt = beta_t * I * (S / N) - delta * E
            didt = delta * E - (1 - alpha_t) * gamma * I - alpha_t * rho * I
            drdt = (1 - alpha_t) * gamma * I
            dddt = alpha_t * rho * I
            return dsdt, dedt, didt, drdt, dddt

        def fit_odeint(t, gamma, delta, scaling, rho, R0_beg, R0_end, dec_factor, x):
            return integrate.odeint(ad_seir_step_ahead, y0, t, args=(gamma, delta, scaling, rho, R0_beg, R0_end, dec_factor, x))[:, 1]

        def fit_odeint2(t, gamma, delta, scaling, rho, scale_factor):
            return integrate.odeint(ad_seir_step_ahead2, y0, t, args=(gamma, delta, scaling, rho, scale_factor))[:, 1]

        I0 = cases[null]
        S0 = population - I0
        R0 = 0.0
        E0 = 0.0
        D0 = 0.0
        y0 = S0, E0, I0, R0, D0

        land2 = st.selectbox("What's landscape did R approximately follow?",
                             ['Sigmoid', 'Sinusoidal'])
        if land2 == "Sigmoid":
            popt, pcov = optimize.curve_fit(fit_odeint, d[:len(
                d)-null], cases[null:], bounds=(0.000, [1., 1., 1., 1., 10, 10, 1., 50.]))
            cols = ['γ', '𝛿', 'Age Weight', 'ρ',
                    'Max R0', 'Min R0', 'Decay Factor', 'X0']
            dataframe = pd.DataFrame(
                [popt],
                columns=(cols))
            st.dataframe(dataframe.style.format("{:.3}").hide_index())
            fitted = fit_odeint(d, *popt)
        else:
            popt, pcov = optimize.curve_fit(fit_odeint2, d[:len(
                d)-null], cases[null:], bounds=(0.000, [1., 1., 1., 1., 10]))
            cols = ['γ', '𝛿', 'Age Weight', 'ρ', 'R0 Scaling']
            dataframe = pd.DataFrame(
                [popt],
                columns=(cols))
            st.dataframe(dataframe.style.format("{:.3}").hide_index())
            fitted = fit_odeint2(d, *popt)

        r2_res = r2_score(cases, fitted)
        vir.comulative_plot2(cases, fitted, dates_range, r2_res)
