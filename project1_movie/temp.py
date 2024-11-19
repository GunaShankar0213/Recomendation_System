import pandas as pd
import pickle
from time import sleep
import requests
import streamlit as st


def fetch_trending(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

recommended_movie_names = []
recommended_movie_posters = []

def post(id,names):
    for i in range(0,10):
     recommended_movie_posters.append(fetch_trending(id[i]))
     recommended_movie_names.append(names[i])
    return recommended_movie_posters,recommended_movie_names

def trending():
    data = pd.read_csv("C:\\Users\\Admin01\\Downloads\\MISC\Machine Learnin Project\\project1\\tmdb_5000_movies.csv")
    trending = data.sort_values(["popularity"], ascending=False)

    movie_id = trending['id']
    movie_name = trending['original_title']
    # id = movie_id[:10]
    id=[]
    names = movie_name[0:10:1]
    names = names.values
    for i in range(0, 4803):
        for j in names:
            if data['original_title'][i] == j:
                 id.append(data['id'][i])
    st.title("TOP 10 POPULAR MOVIES:")

    recommended_movie_posters,recommended_movie_names = post(id,names)
    col1, col2, col3, col4, col5 = st.columns(5, gap='medium')
    with col1:
        st.image(recommended_movie_posters[0], width=200)
        st.text(recommended_movie_names[5])

    with col2:
        st.image(recommended_movie_posters[1], width=200)
        st.text(recommended_movie_names[7])

    with col3:
        st.image(recommended_movie_posters[2], width=200)
        st.text(recommended_movie_names[9])

    with col4:
        st.image(recommended_movie_posters[3], width=200)
        st.text(recommended_movie_names[3])

    with col5:
        st.image(recommended_movie_posters[4], width=200)
        st.text(recommended_movie_names[1])

    col6, col7, col8, col9, col10 = st.columns(5, gap='medium')

    with col6:
        st.image(recommended_movie_posters[5], width=200)
        st.text(recommended_movie_names[4])

    with col7:
        st.image(recommended_movie_posters[6], width=200)
        st.text(recommended_movie_names[6])

    with col8:
        st.image(recommended_movie_posters[7], width=200)
        st.text(recommended_movie_names[8])

    with col9:
        st.image(recommended_movie_posters[8], width=200)
        st.text(recommended_movie_names[0])

    with col10:
        st.image(recommended_movie_posters[9], width=200)
        st.text(recommended_movie_names[2])

