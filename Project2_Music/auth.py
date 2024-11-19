# import datetime
# import os
# import sys
#
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
# import base64
# import requests
#
# # manual method
# client_id = 'ebb347ce48b140129aaebd06b626f2c6'
# client_secret = 'ce61f6a09b3840c5a6a1e0bfe8aca300'
# # token_url = 'https://accounts.spotify.com/api/token'
# # method = 'POST'
# # token_data = {
# #     'grant_type':'client_credentials'
# # }
# # client_creds = f'{client_id}:{client_secret}'
# # client_creds_b64 = base64.b64encode(client_creds.encode())
# # token_header = {
# #     'Authorization' : f'Basic {client_creds_b64.decode()}'
# # }
# # r= requests.post(token_url,data=token_data,headers=token_header)
# # print(r.json())
# # valid_req = r.status_code in range(200,299)
# # if valid_req:
# #     token_response = r.json()
# #     now = datetime.datetime.now()
# #     access_token = token_response['access_token']
# #     expires_in = token_response['expires_in']
# #     expires = now +datetime.timedelta(seconds=expires_in)
# #     did_expire = expires < now
# #     print(did_expire)
#
# # using credential manager
# os.environ.setdefault('SPOTIPY_CLIENT_ID','ebb347ce48b140129aaebd06b626f2c6')
# os.environ.setdefault('SPOTIPY_CLIENT_SECRET','ce61f6a09b3840c5a6a1e0bfe8aca300')
# os.environ.setdefault('SPOTIPY_REDIRECT_URI','ce61f6a09b3840c5a6a1e0bfe8aca300')
#
# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#
# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])
# for album in albums:
#     print(album['name'])
#
# #30sec playback
# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
# results = spotify.artist_top_tracks(lz_uri)
# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()
#
# # artist image
# if len(sys.argv) > 1:
#     name = ' '.join(sys.argv[1:])
# else:
#     name = 'Radiohead'
#
# results = spotify.search(q='artist:' + name, type='artist')
# items = results['artists']['items']
# if len(items) > 0:
#     artist = items[0]
#     print(artist['name'], artist['images'][0]['url'])
#
# scope = "user-library-read"
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#
# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
#
# auth_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(auth_manager=auth_manager)
#
# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# # import pandas as pd
# # import numpy as np
# # import json
# # import re
# # import sys
# # import itertools
# # from skimage import io
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # from sklearn.preprocessing import MinMaxScaler
# # import matplotlib.pyplot as plt
# #
# #
# # import spotipy
# # from spotipy.oauth2 import SpotifyClientCredentials
# # from spotipy.oauth2 import SpotifyOAuth
# # import spotipy.util as util
# #
# # import warnings
# # warnings.filterwarnings("ignore")
# #
# #
# # client_id = 'ebb347ce48b140129aaebd06b626f2c6'
# # client_secret= 'ce61f6a09b3840c5a6a1e0bfe8aca300'
# # scope = 'user-library-read'
# #
# #
# #
# # auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# # sp = spotipy.Spotify(auth_manager=auth_manager)
# # token = util.prompt_for_user_token(scope, client_id= client_id, client_secret=client_secret, redirect_uri='http://localhost:8881/')
# # sp = spotipy.Spotify(auth=token)
# # print(sp)
# # #gather playlist names and images.
# # #images aren't going to be used until I start building a UI
# # id_name = {}
# # list_photo = {}
# # print(sp.current_user_playlists()['items'])
# # for i in sp.current_user_playlists()['items']:
# #     id_name[i['name']] = i['uri'].split(':')[2]
# #     list_photo[i['uri'].split(':')[2]] = i['images'][0]['url']
# #
# # print(id_name)


