import streamlit as st


def write():
    with st.spinner("Loading Credits ..."):
        st.write(
            """
                    # Credits

                    This project was possible thanks to the data provided by the 
                    [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) 
                    and the [Python News API.](https://newsapi.org/docs/client-libraries/python)

                    Additionally, part of the proposed analysis have been inspired by following part of the videos/lectures from [minutephysics](https://www.youtube.com/user/minutephysics), [3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw) and [The Julia Programming Language](https://www.youtube.com/user/JuliaLanguage).

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
