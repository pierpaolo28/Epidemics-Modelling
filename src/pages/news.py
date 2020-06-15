import streamlit as st
from newsapi import NewsApiClient
from PIL import Image
import requests
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import config

newsapi = NewsApiClient(api_key=config.news_key)

pick = {'United Kingdom': 'gb',
        'Argentina': 'ar',
        'Australia': 'au',
        'Austria': 'at',
        'Belgium': 'be',
        'Brazil': 'br',
        'Bulgaria': 'bg',
        'Canada': 'ca',
        'China': 'cn',
        'Colombia': 'co',
        'Cuba': 'cu',
        'Czech Republic': 'cz',
        'Egypt': 'eg',
        'France': 'fr',
        'Germany': 'de',
        'Greece': 'gr',
        'Hong Kong': 'hk',
        'Hungary': 'hu',
        'India': 'in',
        'Indonesia': 'id',
        'Ireland': 'ie',
        'Israel': 'il',
        'Italy': 'it',
        'Japan': 'jp',
        'Latvia': 'lv',
        'Lithuania': 'lt',
        'Malaysia': 'my',
        'Mexico': 'mx',
        'Morocco': 'ma',
        'Netherlands': 'nl',
        'New Zealand': 'nz',
        'Nigeria': 'ng',
        'Norway': 'no',
        'Philippines': 'ph',
        'Poland': 'pl',
        'Portugal': 'pt',
        'Romania': 'ro',
        'Russia': 'ru',
        'Saudi Arabia': 'sa',
        'Serbia': 'rs',
        'Singapore': 'sg',
        'Slovakia': 'sk',
        'Slovenia': 'si',
        'South Africa': 'za',
        'South Korea': 'kr',
        'Sweden': 'se',
        'Switzerland': 'ch',
        'Taiwan': 'tw',
        'Thailand': 'th',
        'Turkey': 'tr',
        'UAE': 'ae',
        'Ukraine': 'ua',
        'United States': 'us',
        'Venezuela': 've'}


def write():
    with st.spinner("Loading World View ..."):
        st.title('COVID-19 World News')
        country = st.selectbox("Select you preferite country",
                               options=list(pick.keys()))
        top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                                  language='en',
                                                  country=pick[country])

        if len(top_headlines['articles']) > 5:
            max_articles = 5
        else:
            max_articles = len(top_headlines['articles'])
        sent = []
        st.markdown("## Latest Articles")
        c = 'https://'
        for i in range(max_articles):
            tit = top_headlines['articles'][i]['title']
            st.markdown("### {}".format(tit))
            desc = top_headlines['articles'][i]['description']
            if desc == None:
                desc = ''
            st.write(desc)
            url = top_headlines['articles'][i]['urlToImage']
            src = top_headlines['articles'][i]['source']['name']
            auth = top_headlines['articles'][i]['author']
            link = top_headlines['articles'][i]['url']
            st.write("Source: " + str(src) + ", Authors: " + str(auth))
            st.markdown("[Read more here]({})".format(link))
            fail = 0
            try:
                if url[:4] != c[:4]:
                    url = c[0:8] + url[2:]
            except:
                fail = 1
            if fail == 0:
                response = requests.get(url, stream=True)
                img = Image.open(response.raw)
                plt.imshow(img)
                plt.axis('off')
                st.pyplot()
            sent.append(desc)
        if max_articles == 0:
            st.write("No news available at the moement for this country.")

        word_list = [item for sublist in [i.split() for i in sent]
                     for item in sublist]
        filtered_words = [
            word for word in word_list if word not in stopwords.words('english')]

        st.markdown("## Sentiment Analysis")
        d = {}
        for x, a in zip(list(dict(Counter(filtered_words)).values()),
                        list(dict(Counter(filtered_words)).keys())):
            d[a] = x

        try:
            wordcloud = WordCloud()
            wordcloud.generate_from_frequencies(frequencies=d)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title("Word Cloud", fontsize=20)
            st.pyplot()
        except:
            st.write("Not enough news available for this country at the moment")

        analyzer = SentimentIntensityAnalyzer()
        sent_list = ' '.join(sent)

        vs = analyzer.polarity_scores(sent_list)
        st.markdown("### Today overall sentiment is {}".format(
            str(vs['compound'])))
