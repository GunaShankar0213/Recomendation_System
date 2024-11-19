from pprint import pprint
import json
import pandas as pd

'''
This script is used to transform raw json data from the dataset to csv files 
by using pandas json_normalize() function
'''

# Import json
data_path = "C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\Project3\\data\\First_1000.json"
raw_json = json.loads(open(data_path).read())

# Transform Data
playlists = raw_json["playlists"]
df = pd.json_normalize(playlists, record_path='tracks', meta=['name'])

# Output
df.to_csv("C:\\Users\\Admin01\\PycharmProjects\\DEMO1\\Project3\\data\\raw_data.csv")