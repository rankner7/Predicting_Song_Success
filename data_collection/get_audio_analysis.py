import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep, time
from os import path
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import csv
import concurrent.futures
import os
import threading
from time import sleep
from threading import Lock

lock = Lock()
def collect_audio_analysis(ids ,analysis_data_file):
    print(str(threading.current_thread()) + 'collect_audio_analysis' + str(ids))
    results = []
    for id in ids:
        try:
            result = {}
            result['id'] = id
            features = sp.audio_analysis(id)
            for feat in features:
                if feat is not (None):
                    if 'segments' == feat:
                        timbre = None
                        pitches = None
                        for seg in features[feat]:
                            tim = seg['timbre']
                            if timbre is None:
                                timbre = np.array([0,0,0,0,0,0,0,0,0,0,0,0], dtype='float32')
                            else:
                                timbre = np.vstack((timbre ,tim))
                            pit = seg['pitches']
                            if pitches is None:
                                pitches = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='float32')
                            else:
                                pitches = np.vstack((pitches, pit))
                        pca = PCA(n_components=1)
                        x = pca.fit_transform(timbre)
                        result['timbre_mean'] = x.mean(axis= 0)[0]
                        result['timbre_max'] = x.max( axis = 0 )[0]
                        result['timbre_min'] = x.min( axis  = 0 )[0]

                        pca = PCA(n_components=1)
                        x = pca.fit_transform(pitches)
                        result['pitches_mean'] = x.mean(axis= 0)[0]
                        result['pitches_max'] = x.max( axis = 0 )[0]
                        result['pitches_min'] = x.min( axis  = 0 )[0]
                else:
                    print("Why else!! No song analysis data!!")
        except:
            print('Spotipy data not found {}'.format(id))
        results.append(result)
    write_to_analysis(analysis_data_file, results)
def write_to_analysis(analysis_data_file, records):
    try:
        lock.acquire()
        with open(analysis_data_file, 'a') as csvfile:
            fieldnames = ['id', 'timbre_mean', 'timbre_max', 'timbre_min', 'pitches_mean', 'pitches_max', 'pitches_min']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for record in records:
                print(str(record))
                writer.writerow(record)
        csvfile.close
        lock.release()
        print('Batch {} data recorded'.format(500))
    except Exception as exc:
        print('exception occured while writing to analysis csv file')
        print(exc)

def get_discard_ids(analysis_data_file):
    try:
        df = pd.read_csv(analysis_data_file)
        print(df.shape)
        ids = df['id']
        return ids
    except Exception as exc:
        print('exception occured while writing to analysis csv {} file'.format)


#songIdFiles = ['../data/full_dataset_0.csv','../data/full_dataset_1.csv','../data/full_dataset_2.csv','../data/full_dataset_3.csv']
songIdFiles = ['../data/full_dataset_0.csv']
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

loop_cnt = 0
time_sum = 0

step_time = 0.3

temp_time = time()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

for idFile in songIdFiles:
    analysis_data_file = idFile[:-4] + '_analysis_data.csv'
    to_discard = get_discard_ids(analysis_data_file)
    writer = None
    df = pd.read_csv(idFile)
    print(df.shape)
    ids = df['id']
    batch = 0
    id_batch = []
    for id in ids.values:
        if not (to_discard is None) and id in to_discard:
            continue
        batch += 1
        if batch == 50:
            executor.submit(collect_audio_analysis, id_batch, analysis_data_file)
            id_batch = []
            #run_parallel(id_batch, writer)
            batch = 0
        else:
            id_batch.append(id)

    print("Data recorded to {}".format(analysis_data_file))
print("\n\n======================================================================")
print("============= ALL SONGS CHECKED AND ANALYSIS RECORED! ================")
print("======================================================================")


