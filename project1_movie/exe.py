import pickle
import pandas as pd
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import streamlit.components.v1 as components
import temp
from streamlit_option_menu import option_menu
import constant_value as const
from Project3.recommendation_app.application.features import extract
from Project3.recommendation_app.application.model import recommend_from_playlist
from element_action import initialize_movie_widget, show_recommended_movie_info
from descriptions import score_based_cfg, content_based_cfg, content_extra_based_cfg
import recommendation as reco
from time import sleep

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


# get movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    sleep(4)
    data = requests.get(url, verify=False)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# collect the recomended movies and poster in order list
def recommend(movie):
    movie_list = pd.DataFrame(movies)
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        # fetch the movie poster
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie_list.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# stylesheet
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# sidebar of website
st.sidebar.markdown('<p style="font-family:sans-serif; color:#fad6a5; font-size: 20px;">'
                    'Welcome you to this movie recommendation system search for a movie, content, different '
                    'genres,<b> Kindly Provide Feedback At last</b>. </p><br></br> '
                    , unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(menu_title=None, options=['Weightage', 'Content-Based', 'Music Genre', 'About'],
                           icons=["cloud", "cast", "list-task", "gear"], default_index=1, styles={
            "container": {"padding": "0!important", "background-color": "#303030"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "crimson"},
        })

if selected == 'Weightage':

    st.title('Movie Recommender System')
    # loading trained data
    movies = pickle.load(open("movie_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))

    movie_list = pd.DataFrame(movies)
    option = st.selectbox("Type or select a movie from the dropdown", movie_list['title'])


    # visual graph
    def atlast():
        with st.container():
            new_title = '<p style="font-family:Roboto,sans-serif; color:#00FFFF; font-size: 42px; text-align: ' \
                        'center">This Chart Shows The Popularity Of The Recommended Movies😉 </p> '
            st.markdown(new_title, unsafe_allow_html=True)
            my_val = recommend(option)
            var = my_val[0]
            data = pd.read_csv(
                "C:\\Users\\Admin01\\Downloads\\MISC\Machine Learnin Project\\project1\\tmdb_5000_movies.csv")
            votes = []
            for i in range(0, 4803):
                for j in var:
                    if data['original_title'][i] == j:
                        votes.append(data['vote_count'][i])

        chart_data = pd.DataFrame(
            [votes],
            columns=var)
        st.bar_chart(chart_data)


    # web elements
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(option)
        with st.spinner('Wait for it...'):
            sleep(2)
        st.success('Done!')

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap='medium')
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0], width=200)
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1], width=200)

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2], width=200)
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3], width=200)
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4], width=200)
        with col6:
            st.text(recommended_movie_names[5])
            st.image(recommended_movie_posters[5], width=200)
        with col7:
            st.text(recommended_movie_names[6])
            st.image(recommended_movie_posters[6], width=200)
        st.markdown('#####')
        atlast()
    sleep(4)
    temp.trending()
if selected == 'Content-Based':

    with open('movie_df.pickle', 'rb') as handle:
        movie = pickle.load(handle)
    st.markdown('# Movie Recommender system')

    # adding search panel and search button
    main_layout, search_layout = st.columns([10, 1])
    options = main_layout.multiselect('Which movies do you like?', movie["title"].unique())
    show_recommended_movies_btn = search_layout.button("search")

    recommended_movie_num = st.slider("Recommended movie number", min_value=5, max_value=10)
    if recommended_movie_num:
        # user recommended movies
        const.MOVIE_NUMBER = recommended_movie_num
    # score box
    show_score = st.checkbox("Show score")
    col_for_content_based = initialize_movie_widget(content_based_cfg)
    if show_recommended_movies_btn:
        sleep(2)
        contend_based_recommended_movies = reco.contend_based_recommendations(movie, options)
        show_recommended_movie_info(contend_based_recommended_movies, col_for_content_based, show_score)

if selected == 'Music Genre':
    # st.title("Upcoming Feature")
    user_input = st.text_input("Paste The Requested Link From Spotify:")
    new_val = st.slider("Recommended movie number", min_value=10, max_value=30)

    songDF = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\project1\\Project3\\data\\allsong_data.csv")
    complete_feature_set = pd.read_csv(
        "C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\project1\\Project3\\data\\complete_feature.csv")
    playlistDF_test = pd.read_csv(
        "C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\project1\\Project3\\data\\test_playlist.csv")


    def recommend_music(link):
        # requesting the URL form the HTML form
        # URL = request.form['URL']
        URL = link
        # using the extract function to get a features dataframe

        df = extract(URL)
        # retrieve the results and get as many recommendations as the user requested
        edm_top40 = recommend_from_playlist(songDF, complete_feature_set, df)
        number_of_recs = int(new_val)

        my_songs = []
        for i in range(number_of_recs):
            my_songs.append([str(edm_top40.iloc[i, 1]) + ' - ' + '"' + str(edm_top40.iloc[i, 4]) + '"',
                             "https://open.spotify.com/track/" + str(edm_top40.iloc[i, 1]).split("/")[-1]])
            # return render_template('results.html', songs=my_songs)
        return my_songs


    def recommend_music_top40(link):
        # requesting the URL form the HTML form
        # URL = request.form['URL']
        URL = link
        # using the extract function to get a features dataframe

        df = extract(URL)
        # retrieve the results and get as many recommendations as the user requested
        edm_top40 = recommend_from_playlist(songDF, complete_feature_set, df)
        return edm_top40


    if user_input:
        songs = recommend_music(user_input)
        val = recommend_music_top40(user_input)
        val_df = pd.DataFrame(val)
        colm = list(val_df['track_name'])
        for i in range(0, len(songs)):
            h_m = '<p style="font-family:Roboto,sans-serif; color:white; font-size: 38px;"> {} </p>'.format(colm[i])
            # st.title(colm[i])
            st.markdown(h_m, unsafe_allow_html=True)
            st.write(songs[i][1])

if selected == 'About':
    about_us = '<p style="font-family:Roboto,sans-serif; color:yellow; font-size: 38px;">Team 4: </p>'
    st.markdown(about_us, unsafe_allow_html=True)
    st.image('download.jpg')

    st.markdown('<img src="download.jpg">', unsafe_allow_html=True)

    htitle = '<h2 style="font-family:Roboto,sans-serif; color:orange; font-size: 42px; text-align: ' \
             'center"><u>The Project is Developed By</u> </h2> '
    st.markdown(htitle, unsafe_allow_html=True)
    st.markdown('<p style="font-family:sans-serif; color:yellow; font-weight:bold; font-size: 38px;">20MIA1162   '
                'Guna Shankar S </p>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:sans-serif; color:yellow; font-weight:bold; font-size: 38px;">20MIA1162   '
                'Guna Shankar S </p>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:sans-serif; color:yellow; font-weight:bold; font-size: 38px;">20MIA1162   '
                'Guna Shankar S </p>', unsafe_allow_html=True)
