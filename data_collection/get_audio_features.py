import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep, time
from os import path
import pandas as pd

blank_feature_obj = {
		'Song Title':[],
		'Artist(s)':[],
		'Date':[],
		'id':[],
		'Popularity':[],
		'Duration':[],
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

def collect_audio_features(uri_list):
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
	
	features = sp.audio_features(uri_list)
	for feat in features:
		if feat is not(None):
			for key in audio_feat:
				audio_feat[key].append(feat[key])
		else:
			#print("NONE TYPE RECIEVED")
			for key in audio_feat:
				audio_feat[key].append('NaN')
	
	return audio_feat

def collect_track_info(data_list):
	track_info = {
		'Song Title':[],
		'Artist(s)':[],
		'Date':[],
		'id':[],
		'Popularity':[],
		'Duration':[]
	}
	
	for data_line in data_list:
		track_info['Song Title'].append(data_line.split('||')[0])
		track_info['Artist(s)'].append(data_line.split('||')[1])
		track_info['Date'].append(data_line.split('||')[2])
		track_info['id'].append(data_line.split('||')[4])
		track_info['Popularity'].append(data_line.split('||')[5])
		track_info['Duration'].append(data_line.split('||')[3])

	return track_info

	

	
	
def dissect_track_info(track):
	artists = ""
	for artist in track['artists']:
		artists += artist['name']+'/'
	track_info = {
		'Song Title':track['album']['name'],
		'Artist(s)':artists,
		'id':track['id'],
		'Popularity':track['popularity'],
		'Duration': track['duration_ms']
	}
	return track_info


data_set = 'all'

last_id_file = ''
audio_feature_file = ''

if data_set == 'all':
	track_data_file = '../data/spotify_ton_of_songs.txt'
	last_id_file = '../data/last_id_all.txt'
	audio_feature_file = '../data/audio_features_all.csv'

elif data_set == 'billboards':
	track_data_file = '../data/spotify_billboard_songs.txt'
	last_id_file = '../data/last_id_billboards.txt'
	audio_feature_file = '../data/audio_features_billboards.csv'

else:
	print("INVALID DATASET SELECTION --> must be 'all' or 'billboards'")
	exit()


with open(track_data_file, 'r') as all_handle:
	data_list = all_handle.read().split('\n')

#Remove Duplicates if any
data_list = list(dict.fromkeys(data_list))
while '' in data_list:
	data_list.remove('')

id_list = []
for data in data_list:
	id_list.append(data.split('||')[4])


partition_size = 50

start = 0
if path.exists(last_id_file):
	#Find ID to start on
	with open(last_id_file, 'r') as last_id_handle:
		last_id = last_id_handle.read()

	start = int(id_list.index(last_id)/partition_size)+1

end = int(len(id_list)/partition_size)

print("Working on Dataset:", data_set)
print("Starting from index", start, "out of", end)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

loop_cnt = 0
time_sum = 0

step_time = 0.3

temp_time = time()
#Goes to (end+1) becuase partitions are in full sets of 50, ind must go one extra to get all songs
for ind in range(start, end+1):
	loop_cnt += 1
	diff = time()-temp_time
	if (diff) < step_time:
		sleep(step_time - diff)
	loop_time = time()-temp_time
	time_sum += loop_time
	time_left = time_sum*(end-ind)/loop_cnt
	tm_hrs = int(time_left/3600)
	print("Progress: %.3f%% | Time Left: %d hr %d min | Time For last 50: %.3f s"%((ind*100/end), tm_hrs, int((time_left-tm_hrs*3600)/60), loop_time))
	temp_time = time()

	if ind == end:
		track_list = data_list[partition_size*ind:len(data_list)]
		list_to_get = id_list[partition_size*ind:len(id_list)]
	else:
		track_list = data_list[partition_size*ind:partition_size*(ind+1)]
		list_to_get = id_list[partition_size*ind:partition_size*(ind+1)]

	pref = 'spotify:track:'
	for i,ID in enumerate(list_to_get):
		list_to_get[i] = pref+ID
		

	audio_features = collect_audio_features(list_to_get)
	track_info = collect_track_info(track_list)

	track_info.update(audio_features)
	full_features = track_info

	new_frame = pd.DataFrame(full_features)
	
	if path.exists(audio_feature_file):
		new_frame.to_csv(audio_feature_file, mode='a', header=False, index=False)
	else:
		new_frame.to_csv(audio_feature_file, index=False)
		print("File Does Not Exist --> Starting csv")

	with open(last_id_file, 'w') as last_id_handle:
			last_id_handle.write(id_list[ind*partition_size])
	
	if ind%20 == 0:
		file_size = path.getsize(audio_feature_file)
		unit = 'B'
		file_size_adj = file_size
		if file_size > 10**3:
			unit = 'KB'
			file_size_adj = file_size/(10**3)
		if file_size > 10**6:
			unit = 'MB'
			file_size_adj = file_size/(10**6)
		if file_size > 10**9:
			unit = 'GB'
			file_size_adj = file_size/(10**9)

		print('\tFile Size: %.1f'%(file_size_adj), unit)
		print('\t\t--> Projected Final Size: %.3f GB'%((file_size/(ind+1))*end/(10**9)))

file_size = path.getsize(audio_feature_file)
unit = 'B'
file_size_adj = file_size
if file_size > 10**3:
	unit = 'KB'
	file_size_adj = file_size/(10**3)
if file_size > 10**6:
	unit = 'MB'
	file_size_adj = file_size/(10**6)
if file_size > 10**9:
	unit = 'GB'
	file_size_adj = file_size/(10**9)

print('FINAL File Size: %.1f'%(file_size_adj), unit)

print("\n\n======================================================================")
print("============= ALL SONGS CHECKED AND FEATURES RECORED! ================")
print("======================================================================")


