import time

import pandas as pd
import numpy as np
import json
import re
import sys
import itertools
from skimage import io
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

import warnings
warnings.filterwarnings("ignore")

spotify_df = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\Project2\\clean_spotify_df_spotify.csv")

'''
Feature engineering
1.normalize float var
2.OHE year and popularity
3.Create TF-DIF feature of artist genres
'''
spotify_df['year'] = spotify_df['release_date'].apply(lambda x:x.split('-')[0])
float_cols = spotify_df.dtypes[spotify_df.dtypes == 'float64'].index.values
ohe_cols = 'popularity'
print(spotify_df['popularity'].describe())

#bucket of 5 points
spotify_df['popularity_red'] = spotify_df['popularity'].apply(lambda x: int(x/5))
# spotify_df['consolidates_genre_lists'] = spotify_df['consolidates_genre_lists'].fillna(np.nan)
spotify_df['consolidates_genre_lists'] = spotify_df['consolidates_genre_lists'].fillna(np.nan,inplace=True)

# #fill nulls
spotify_df['consolidates_genre_lists'] = spotify_df['consolidates_genre_lists'].apply(lambda d: d if isinstance(d, list) else [])
print(spotify_df.tail(5))
#
# print('Re-modelled CSV')
# print(spotify_df.tail(5))
#
# #hot encoding
# def ohe_prep(df,coloumn,new_name):
#     tf_df = pd.get_dummies(df[coloumn])
#     feature_name = tf_df.columns
#     tf_df.columns = [new_name + '|' + str(i) for i in feature_name]
#     tf_df.reset_index(drop=True,inplace=True)
#     return tf_df
#
#
# # function to build entire feature set
# def create_feature_set(df, float_cols):
#     """
#     Process spotify df to create a final set of features that will be used to generate recommendations
#
#     Parameters:
#         df (pandas dataframe): Spotify Dataframe
#         float_cols (list(str)): List of float columns that will be scaled
#
#     Returns:
#         final: final set of features
#     """
#
#     # tfidf genre lists
#     tfidf = TfidfVectorizer()
#     tfidf_matrix = tfidf.fit_transform(df['consolidates_genre_lists'].apply(lambda x: " ".join(x)))
#     genre_df = pd.DataFrame(tfidf_matrix.toarray())
#     genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
#     genre_df.reset_index(drop=True, inplace=True)
#
#     # explicity_ohe = ohe_prep(df, 'explicit','exp')
#     year_ohe = ohe_prep(df, 'year', 'year') * 0.5
#     popularity_ohe = ohe_prep(df, 'popularity_red', 'pop') * 0.15
#
#     # scale float columns
#     floats = df[float_cols].reset_index(drop=True)
#     scaler = MinMaxScaler()
#     floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns=floats.columns) * 0.2
#
#     # concanenate all features
#     final = pd.concat([genre_df, floats_scaled, popularity_ohe, year_ohe], axis=1)
#
#     # add song id
#     final['id'] = df['id'].values
#
#     return final
#
# complete_feature_set = create_feature_set(spotify_df, float_cols=float_cols)#.mean(axis = 0)
# complete_feature_set.head()
#
# #client id and secret for my application
# client_id = 'ebb347ce48b140129aaebd06b626f2c6'
# client_secret= 'ce61f6a09b3840c5a6a1e0bfe8aca300'
# scope = 'user-library-read'
#
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()
#
# auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(auth_manager=auth_manager)
# token = util.prompt_for_user_token(scope, client_id= client_id, client_secret=client_secret,
#                                    redirect_uri='http://localhost:8881/')
# sp = spotipy.Spotify(auth=token)
# #gather playlist names and images.
# #images aren't going to be used until I start building a UI
# id_name = {}
# list_photo = {}
# for i in sp.current_user_playlists()['items']:
#
#     id_name[i['name']] = i['uri'].split(':')[2]
#     list_photo[i['uri'].split(':')[2]] = i['images'][0]['url']
#
# print(id_name)
#
# def create_necessary_outputs(playlist_name, id_dic, df):
#     """
#     Pull songs from a specific playlist.
#
#     Parameters:
#         playlist_name (str): name of the playlist you'd like to pull from the spotify API
#         id_dic (dic): dictionary that maps playlist_name to playlist_id
#         df (pandas dataframe): spotify datafram
#
#     Returns:
#         playlist: all songs in the playlist THAT ARE AVAILABLE IN THE KAGGLE DATASET
#     """
#
#     # generate playlist dataframe
#     playlist = pd.DataFrame()
#     playlist_name = playlist_name
#
#     for ix, i in enumerate(sp.playlist(id_dic[playlist_name])['tracks']['items']):
#         # print(i['track']['artists'][0]['name'])
#         playlist.loc[ix, 'artist'] = i['track']['artists'][0]['name']
#         playlist.loc[ix, 'name'] = i['track']['name']
#         playlist.loc[ix, 'id'] = i['track']['id']  # ['uri'].split(':')[2]
#         playlist.loc[ix, 'url'] = i['track']['album']['images'][1]['url']
#         playlist.loc[ix, 'date_added'] = i['added_at']
#
#     playlist['date_added'] = pd.to_datetime(playlist['date_added'])
#
#     playlist = playlist[playlist['id'].isin(df['id'].values)].sort_values('date_added', ascending=False)
#
#     return playlist
#
# print(id_name)
#
# playlist_EDM = create_necessary_outputs('EDM', id_name,spotify_df)
#
#
#
# def visualize_songs(df):
#     """
#     Visualize cover art of the songs in the inputted dataframe
#
#     Parameters:
#         df (pandas dataframe): Playlist Dataframe
#     """
#
#     temp = df['url'].values
#     plt.figure(figsize=(15, int(0.625 * len(temp))))
#     columns = 5
#
#     for i, url in enumerate(temp):
#         plt.subplot(len(temp) / columns + 1, columns, i + 1)
#
#         image = io.imread(url)
#         plt.imshow(image)
#         plt.xticks(color='w', fontsize=0.1)
#         plt.yticks(color='w', fontsize=0.1)
#         plt.xlabel(df['name'].values[i], fontsize=12)
#         plt.tight_layout(h_pad=0.4, w_pad=0)
#         plt.subplots_adjust(wspace=None, hspace=None)
#
#     plt.show()
# print(playlist_EDM)
# visualize_songs(playlist_EDM)
#
#
# def generate_playlist_feature(complete_feature_set, playlist_df, weight_factor):
#     """
#     Summarize a user's playlist into a single vector
#
#     Parameters:
#         complete_feature_set (pandas dataframe): Dataframe which includes all of the features for the spotify songs
#         playlist_df (pandas dataframe): playlist dataframe
#         weight_factor (float): float value that represents the recency bias. The larger the recency bias, the most priority recent songs get. Value should be close to 1.
#
#     Returns:
#         playlist_feature_set_weighted_final (pandas series): single feature that summarizes the playlist
#         complete_feature_set_nonplaylist (pandas dataframe):
#     """
#
#     complete_feature_set_playlist = complete_feature_set[
#         complete_feature_set['id'].isin(playlist_df['id'].values)]  # .drop('id', axis = 1).mean(axis =0)
#     complete_feature_set_playlist = complete_feature_set_playlist.merge(playlist_df[['id', 'date_added']], on='id',
#                                                                         how='inner')
#     complete_feature_set_nonplaylist = complete_feature_set[
#         ~complete_feature_set['id'].isin(playlist_df['id'].values)]  # .drop('id', axis = 1)
#
#     playlist_feature_set = complete_feature_set_playlist.sort_values('date_added', ascending=False)
#
#     most_recent_date = playlist_feature_set.iloc[0, -1]
#
#     for ix, row in playlist_feature_set.iterrows():
#         playlist_feature_set.loc[ix, 'months_from_recent'] = int(
#             (most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days / 30)
#
#     playlist_feature_set['weight'] = playlist_feature_set['months_from_recent'].apply(lambda x: weight_factor ** (-x))
#
#     playlist_feature_set_weighted = playlist_feature_set.copy()
#     # print(playlist_feature_set_weighted.iloc[:,:-4].columns)
#     playlist_feature_set_weighted.update(
#         playlist_feature_set_weighted.iloc[:, :-4].mul(playlist_feature_set_weighted.weight, 0))
#     playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-4]
#     # playlist_feature_set_weighted_final['id'] = playlist_feature_set['id']
#
#     return playlist_feature_set_weighted_final.sum(axis=0), complete_feature_set_nonplaylist
# complete_feature_set_playlist_vector_EDM, complete_feature_set_nonplaylist_EDM = generate_playlist_feature(complete_feature_set, playlist_EDM, 1.09)
# print(complete_feature_set_playlist_vector_EDM.shape)
#
