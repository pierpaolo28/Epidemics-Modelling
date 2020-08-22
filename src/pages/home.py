import streamlit as st
import pages.world_view
from support.utilities import world_map, world_plot, stats


def write():
    f = open("src/pages/vote.txt", "w")
    f.write("0")
    f.close()
    with st.spinner("Loading Home ..."):
        st.write(
            """
                    # Epidemic Modelling Case Study
                    Examination of the different technqiues which can 
                    be used in order to study and control the development of an epidemic.
                    Throughout this web app, COVID-19 is going to be used as case study. 
                    Although, tweking the different modelling parameters, this same dashboard 
                    could potentially be used in order to make estimates about future different 
                    epidemics.

                    Some examples of resources currently available on this webapp are:
                    - A world view record of how the COVID-19 pandemic progressed over 
                      time and what are the latest results.
                    - A modelling interface which can be used in order to simulate different 
                      scenarios of disease spreading.
                    - Simulations of how protective measures can reduce the spread of the disease 
                      and what would be the potential economical impacts.
                    - Prediction of necessary ICU beds and analysis of how time-limited immunity and
                      vaccination would affect the development of a pandemic.

                    ## Contacts

                    If you want to keep updated with my latest articles and projects [follow me on Medium](https://medium.com/@pierpaoloippolito28?source=post_page---------------------------) and subscribe to my [mailing list](http://eepurl.com/gwO-Dr?source=post_page---------------------------). These are some of my contacts details:

                    * [Linkedin](https://uk.linkedin.com/in/pier-paolo-ippolito-202917146?source=post_page---------------------------)

                    * [Personal Blog](https://pierpaolo28.github.io/blog/?source=post_page---------------------------)

                    * [Personal Website](https://pierpaolo28.github.io/?source=post_page---------------------------)

                    * [Patreon](https://www.patreon.com/user?u=32155890)

                    * [Medium Profile](https://towardsdatascience.com/@pierpaoloippolito28?source=post_page---------------------------)

                    * [GitHub](https://github.com/pierpaolo28?source=post_page---------------------------)

                    * [Kaggle](https://www.kaggle.com/pierpaolo28?source=post_page---------------------------)
            """
        )
