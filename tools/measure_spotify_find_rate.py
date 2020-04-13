from os import path
import pandas as pd
import sys

print("Measuring Find Rate For Billboard Songs")
song_frame = pd.read_csv('../data/billboard_songs_1946-2019.csv', index_col=False)
songs = song_frame['Song Title'].tolist()

last_song_file = '../data/last_song_bill.txt'
current = 0
if path.exists(last_song_file):
	#Find song to start on
	last_song_handle = open(last_song_file, 'r')
	last_song = last_song_handle.read()

	current = songs.index(last_song)

song_handle = open('../data/spotify_billboard_songs.txt', 'r')
song_list = song_handle.read().split('\n')

curr_cnt = len(song_list)
print("Current ID count:", str(curr_cnt))
print("Current Find Rate: %.3f%%"%(curr_cnt*100/current))
