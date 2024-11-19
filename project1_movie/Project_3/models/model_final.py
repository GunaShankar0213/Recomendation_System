import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import re

songDF = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\project1\\Project3\\data\\allsong_data.csv")
complete_feature_set = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\project1\\Project3\\data\\complete_feature.csv")
playlistDF_test = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\project1\\Project3\\data\\test_playlist.csv")

def generate_playlist_feature(complete_feature_set, playlist_df):
    '''
    convert user's playlist into a single vector
    Dataframe which includes all of the features for the spotify song  and playlist_df
    result for us:
    single vector feature that summarizes the playlist
    complete_feature_set_non playlist
    '''

    # Find song features in the playlist
    complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
    # Find all non-playlist song features
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]
    complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns = "id")
    return complete_feature_set_playlist_final.sum(axis = 0), complete_feature_set_nonplaylist

def generate_playlist_recos(df, features, nonplaylist_features):
    '''
    Generated recommendation based on songs in a specific playlist.
    spotify dataframe
    Output: 
    non_playlist_df_top_40: Top 40 recommendations for that playlist song to be recommended
    '''

    non_playlist_df = df[df['id'].isin(nonplaylist_features['id'].values)]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis = 1).values, features.values.reshape(1, -1))[:,0]
    non_playlist_df_top_40 = non_playlist_df.sort_values('sim',ascending = False).head(40)

    return non_playlist_df_top_40

def recommend_from_playlist(songDF=songDF,complete_feature_set=complete_feature_set,playlistDF_test=playlistDF_test):

    # Find feature
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(complete_feature_set, playlistDF_test)

    # Generate recommendation
    top40 = generate_playlist_recos(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)

    return top40

if __name__ == '__main__':
    print(recommend_from_playlist()[:10])
