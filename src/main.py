import streamlit as st
import pages.home
import pages.world_view
import pages.news
import pages.credits
import pages.modelling
import pages.population
import pages.growth
import pages.tracing
import pages.seir
import pages.virus_model
import pages.hubs
import pages.finance
from support.utilities import world_map, world_plot, stats

PAGES = {
    "Home": pages.home,
    "World View": pages.world_view,
    "World News": pages.news,
    "Desease growth": pages.growth,
    "Population Modelling": pages.population,
    "Track and Trace": pages.tracing,
    "Central Hubs": pages.hubs,
    "Finance Simulation": pages.finance,
    "SIR and SEIR Modelling": pages.modelling,
    "Advanced SEIR Modelling": pages.seir,
    "Coronavirus Modelling": pages.virus_model,
    "Credits": pages.credits,
}


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    st.sidebar.title("Contribute")
    st.sidebar.info(
        "This an open source research project, therefore any **suggestion** is welcome. "
        "The source code used to create this Web App, is available at "
        "[this link](https://github.com/pierpaolo28/Epidemics-Modelling). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Pier Paolo Ippolito. You can learn more about me at
        [pierpaolo28.github.io](https://pierpaolo28.github.io/).
        """
    )

    if selection == "Home":
        pages.home.write()
    elif selection == "World View":
        pages.world_view.write()
    elif selection == "World News":
        pages.news.write()
    elif selection == "Desease growth":
        pages.growth.write()
    elif selection == "Track and Trace":
        pages.tracing.write()
    elif selection == "Central Hubs":
        pages.hubs.write()
    elif selection == "Finance Simulation":
        pages.finance.write()
    elif selection == "Credits":
        pages.credits.write()
    elif selection == "Population Modelling":
        pages.population.write()
    elif selection == "SIR and SEIR Modelling":
        pages.modelling.write()
    elif selection == "Advanced SEIR Modelling":
        pages.seir.write()
    elif selection == "Coronavirus Modelling":
        pages.virus_model.write()


if __name__ == "__main__":
    main()
