import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd

def extract(URL):
    client_id = "ebb347ce48b140129aaebd06b626f2c6"
    client_secret = "ce61f6a09b3840c5a6a1e0bfe8aca300"

    #use the clint secret and id details
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # the URI is split by ':' to get the username and playlist ID
    playlist_id = URL.split("/")[4].split("?")[0]
    print(playlist_id)
    playlist_tracks_data = sp.playlist_tracks(playlist_id)

    #lists that will be filled in with features
    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []

    #go through the dictionary to extract the data
    for track in playlist_tracks_data['items']:
        playlist_tracks_id.append(track['track']['id'])
        playlist_tracks_titles.append(track['track']['name'])
        # adds a list of all artists involved in the song to the list of artists for the playlist
        artist_list = []
        for artist in track['track']['artists']:
            artist_list.append(artist['name'])
        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])

    #create a dataframe
    features = sp.audio_features(playlist_tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['title'] = playlist_tracks_titles
    features_df['first_artist'] = playlist_tracks_first_artists
    features_df['all_artists'] = playlist_tracks_artists
    features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                                'danceability', 'energy', 'key', 'loudness',
                                'mode', 'acousticness', 'instrumentalness',
                                'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]
    
    return features_df



