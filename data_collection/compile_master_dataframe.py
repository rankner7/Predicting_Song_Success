import pandas as pd
import numpy as np

billboards_file = '../data/audio_features_billboards.csv'
all_songs_file = '../data/audio_features_all.csv'
artist_songs_file = '../data/audio_features_artist_songs.csv'
compiled_file = '../data/full_dataset.csv'

headers = [
	'Song Title', 
	'Artist(s)', 
	'Date', 
	'id', 
	'Popularity', 
	'Duration', 
	'danceability',
	'energy',
	'key',
	'loudness',
	'mode',
	'speechiness', 
	'acousticness',
	'instrumentalness',
	'liveness',
	'valence',
	'tempo',
	'time_signature']

data_types = {
	'Song Title': str, 
	'Artist(s)': str, 
	'Date': str, 
	'id': str, 
	'Popularity': int, 
	'Duration': int, 
	'danceability': float,
	'energy': float,
	'key': float,
	'loudness': float,
	'mode': float,
	'speechiness': float, 
	'acousticness': float,
	'instrumentalness': float,
	'liveness': float,
	'valence': float,
	'tempo': float,
	'time_signature': float
}
type_adjust = {
	'key': int,
	'mode': int,
	'time_signature': int
}

def find_errors(dtype, series):
	remove_list = []
	for i,entry in enumerate(series):
		try:
			dtype(entry)
		except:
			print("\tError Converting |",entry,"| (#", i, ") to ", dtype)
			remove_list.append(i)

	return remove_list


files = [billboards_file, all_songs_file, artist_songs_file]
data_frames = []
big_frame = pd.DataFrame(columns=headers)

for fil in files:
	print("Reading", fil)
	data_frames.append(pd.read_csv(fil, index_col=False, low_memory=False, header=None))

for i,df in enumerate(data_frames):
	df.columns = headers

	print("SIZE BEFORE NA REMOVAL", df.shape[0])
	df.dropna(inplace=True, axis=0)
	df.reset_index(inplace=True, drop=True)
	print("SIZE AFTER NA REMOVAL", df.shape[0])

	remove = []
	#Before Running Datatype Change, check for rows that wont convert and remove them
	for head in headers:
		print("Investigating", head)
		remove += find_errors(data_types[head], df[head])
	
	remove = list(set(remove))
	print("Removing", len(remove), "rows")
	df.drop(remove, inplace=True)
	df.reset_index(inplace=True, drop=True)

	#Do Datatype Conversion
	df = df.astype(data_types)
	df = df.astype(type_adjust)
	
	#Add success Column
	if i == 0:
		df['Success'] = [int(1)]*df.shape[0]
	else:
		df['Success'] = [int(0)]*df.shape[0]
	
	
	#Data Type Preview
	print(df.head(10))
	print(df.info())
	
	big_frame = pd.concat([big_frame, df], axis=0, ignore_index=True)

print("\n\n================= Big Frame =======================")
big_frame.info()
print("Writing Dataframe to File")
big_frame.to_csv(compiled_file, index=False)
print("Writing Completed :)")









