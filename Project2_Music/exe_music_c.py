import pandas as pd
import numpy as np
import json
import re
import sys
import itertools
from skimage import io
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
#If you're not familiar with this, save it! Makes using jupyter notebook on laptops much easier
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))

#another useful command to make data exploration easier
# NOTE: if you are using a massive dataset, this could slow down your code.


spotify_df = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\Project2\\clean_spotify_df_spotify.csv")
print(spotify_df.head())

# Observations:
# This data is at a song level
# Many numerical values that I'll be able to use to compare movies (liveness, tempo, valence, etc)
# Release date will useful but I'll need to create a OHE variable for release date in 5 year increments
# Similar to 2, I'll need to create OHE variables for the popularity. I'll also use 5 year increments here
# There is nothing here related to the genre of the song which will be useful. This data alone won't help us ' \
# 'find relavent content since this is a content based recommendation system. Fortunately there is a data_w_genres.' \
# 'csv file that should have some useful information

data_w_genre = pd.read_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\Project2\\data_w_genres.csv")
data_w_genre.head()

# Observations:
# This data is at an artist level
# There are similar continuous variables as our initial dataset but I won't use this. I'll just use the values
# int he previous dataset.
# The genres are going to be really useful here and I'll need to use it moving forward. Now, ' \
# 'the genre column appears to be in a list format but my past experience tells me that it's likely not.
# Let's investigate this further.

print(data_w_genre.dtypes)
print(data_w_genre['genres'].values[0])

# As we can see, it's actually a string that looks like a list. Now, look at the example above, ' \
#                  'I'm going to put together a regex statement to extract the genre and input into a list

data_w_genre['genres_upd'] = data_w_genre['genres'].apply(lambda x: [re.sub(' ','_',i) for i in re.findall(r"'([^']*)'", x)])
print(data_w_genre['genres_upd'].values[0][0])

# Voila, now we have the genre column in a format we can actually use. If you go down, you'll see how we use it.
# Now, if you recall, this data is at a artist level and the previous dataset is at a song level. So what here's what we need to do:
# Explode artists column in the previous so each artist within a song will have their own row
# Merge data_w_genre to the exploded dataset in Step 1 so that the previous dataset no is enriched with genre dataset
# Before I go further, let's complete these two steps.
# Step 1. Similar to before, we will need to extract the artists from the string list.

spotify_df['artists_upd_v1'] = spotify_df['artists'].apply(lambda x: re.findall(r"'([^']*)'", x))
print(spotify_df['artists'].values[0])
print(spotify_df['artists_upd_v1'].values[0][0])
#This looks good but did this work for every artist string format. Let's double check

spotify_df[spotify_df['artists_upd_v1'].apply(lambda x: not x)].head(5)

# #So, it looks like it didn't catch all of them and you can quickly see that it's because artists with an
#     apostrophe in their title and the fact that they are enclosed in a full quotes. I'll write another regex to
#     handle this and then combine the two

spotify_df['artists_upd_v2'] = spotify_df['artists'].apply(lambda x: re.findall('\"(.*?)\"',x))
spotify_df['artists_upd'] = np.where(spotify_df['artists_upd_v1'].apply(lambda x: not x), spotify_df['artists_upd_v2'],
                                     spotify_df['artists_upd_v1'] )

#need to create my own song identifier because there are duplicates of the same song with different ids. I see different
spotify_df['artists_song'] = spotify_df.apply(lambda row: row['artists_upd'][0]+row['name'],axis = 1)
spotify_df.sort_values(['artists_song','release_date'], ascending = False, inplace = True)
print(spotify_df[spotify_df['name']=='Adore You'])
spotify_df.drop_duplicates('artists_song',inplace = True)
print(spotify_df[spotify_df['name']=='Adore You'])
artists_exploded = spotify_df[['artists_upd','id']].explode('artists_upd')
artists_exploded_enriched = artists_exploded.merge(data_w_genre, how = 'left', left_on = 'artists_upd',right_on = 'artists')
artists_exploded_enriched_nonnull = artists_exploded_enriched[~artists_exploded_enriched.genres_upd.isnull()]
print(artists_exploded_enriched_nonnull[artists_exploded_enriched_nonnull['id'] =='6KuQTIu1KoTTkLXKrwlLPV'])

# Alright we're almost their, now we need to:
#
# Group by on the song id and essentially create lists lists
# Consilidate these lists and output the unique values

artists_genres_consolidated = artists_exploded_enriched_nonnull.groupby('id')['genres_upd'].apply(list).reset_index()
artists_genres_consolidated['consolidates_genre_lists'] = artists_genres_consolidated['genres_upd'].apply(lambda x: list(set(list(itertools.chain.from_iterable(x)))))
print(artists_genres_consolidated.head())
spotify_df = spotify_df.merge(artists_genres_consolidated[['id','consolidates_genre_lists']], on = 'id',how = 'left')

print(spotify_df.tail())

# 2. Feature Engineering
# - Normalize float variables
# - OHE Year and Popularity Variables
# - Create TF-IDF features off of artist genres

spotify_df['year'] = spotify_df['release_date'].apply(lambda x: x.split('-')[0])
float_cols = spotify_df.dtypes[spotify_df.dtypes == 'float64'].index.values
ohe_cols = 'popularity'
print(spotify_df['popularity'].describe())

# create 5 point buckets for popularity
spotify_df['popularity_red'] = spotify_df['popularity'].apply(lambda x: int(x/5))
# tfidf can't handle nulls so fill any null values with an empty list
spotify_df['consolidates_genre_lists'] = spotify_df['consolidates_genre_lists'].apply(lambda d: d if isinstance(d, list) else [])
print(spotify_df.head(5))


# simple function to create OHE features
# this gets passed later on
def ohe_prep(df, column, new_name):
    """
    Create One Hot Encoded features of a specific column

    Parameters:
        df (pandas dataframe): Spotify Dataframe
        column (str): Column to be processed
        new_name (str): new column name to be used

    Returns:
        tf_df: One hot encoded features
    """

    tf_df = pd.get_dummies(df[column])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop=True, inplace=True)
    return tf_df


# function to build entire feature set
def create_feature_set(df, float_cols):
    """
    Process spotify df to create a final set of features that will be used to generate recommendations

    Parameters:
        df (pandas dataframe): Spotify Dataframe
        float_cols (list(str)): List of float columns that will be scaled

    Returns:
        final: final set of features
    """

    # tfidf genre lists
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['consolidates_genre_lists'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
    genre_df.reset_index(drop=True, inplace=True)

    # explicity_ohe = ohe_prep(df, 'explicit','exp')
    year_ohe = ohe_prep(df, 'year', 'year') * 0.5
    popularity_ohe = ohe_prep(df, 'popularity_red', 'pop') * 0.15

    # scale float columns
    floats = df[float_cols].reset_index(drop=True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns=floats.columns) * 0.2

    # concanenate all features
    final = pd.concat([genre_df, floats_scaled, popularity_ohe, year_ohe], axis=1)

    # add song id
    final['id'] = df['id'].values

    return final

complete_feature_set = create_feature_set(spotify_df, float_cols=float_cols)#.mean(axis = 0)
print(complete_feature_set.head())

