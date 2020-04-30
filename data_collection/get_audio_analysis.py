import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep, time
from os import path
import pandas as pd


def collect_audio_analysis(id):
    audio_feat = {
        'danceability': [],
        'energy': [],
        'key': [],
        'loudness': [],
        'mode': [],
        'speechiness': [],
        'acousticness': [],
        'instrumentalness': [],
        'liveness': [],
        'valence': [],
        'tempo': [],
        'time_signature': []
    }

    features = sp.audio_analysis(id)
    for feat in features:
        if feat is not (None):
            print(feat + ' ## '+str(features[feat]))
            #for key in audio_feat:
                #audio_feat[key].append(feat[key])
        else:
            print(features[feat])
            # print("NONE TYPE RECIEVED")
            #for key in audio_feat:
                #audio_feat[key].append('NaN')

    return audio_feat

songIdFiles = ['../data/full_dataset_0.csv','../data/full_dataset_1.csv','../data/full_dataset_2.csv','../data/full_dataset_3.csv']
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

loop_cnt = 0
time_sum = 0

step_time = 0.3

temp_time = time()

for idFile in songIdFiles:
    df = pd.read_csv(idFile)
    ids = df['id']
    for id in ids.values:
        analysis = collect_audio_analysis(id)
        print(analysis)
        break
    break

#print('FINAL File Size: %.1f' % (file_size_adj), unit)

print("\n\n======================================================================")
print("============= ALL SONGS CHECKED AND FEATURES RECORED! ================")
print("======================================================================")


