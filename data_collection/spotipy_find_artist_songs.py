import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep, time
from os import path

def print_track_info(track):
	print("\tSong Name:", track['name'])
	print("\tArtist(s):")
	for artist in track['artists']:
		print('\t -->',artist['name'])

	print("\tRelease Date:")
	dates = ['Year', 'Month', 'Day']
	release_date = track['album']['release_date']
	for j, date in enumerate(release_date.split('-')):
		print("\t --> "+dates[j],date)
	
	print("\tDuration:   ", track['duration_ms'])
	print("\tSpotify ID: ", track['id'])
	print("\tPopularity: ", track['popularity'])

def form_spot_data(track):
	artists = ""
	for artist in track['artists']:
		artists += artist['name']+"/"
	return track['name']+'||'+artists+'||'+track['album']['release_date']+'||'+str(track['duration_ms'])+'||'+track['id']+'||'+str(track['popularity'])

def get_artist(name):
	results = sp.search(q='artist:' + name, type='artist')
	items = results['artists']['items']
	if len(items) > 0:
		return items[0]
	else:
		return None

def get_artist_albums(artist):
	if artist is None:
		return []
	albums = []
	album_names = []
	results = sp.artist_albums(artist['id'], album_type='album')
	if results is None:
		return []
	albums.extend(results['items'])
	while results['next']:
		results = sp.next(results)
		albums.extend(results['items'])
	seen = set()  # to avoid dups
	albums.sort(key=lambda album: album['name'].lower())
	for album in albums:
		name = album['name']
		if name not in seen:
			#print('\tALBUM: %s'%name)
			album_names.append(name)
			seen.add(name)
	return album_names

def peek_at_song(track):
	print(track['name'],"\n\t\t-->", track['album']['name'], "\n\t\t\t\t-->", end = "")
	for i,artist in enumerate(track['artists']):
		if i == (len(track['artists'])-1):
			print(artist['name'])
		else:
			print(artist['name']+'/', end='')



sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

with open('../data/artist_list.txt', 'r') as artist_name_handle:
	artist_list = artist_name_handle.read()

artists = artist_list.split('\n')
while "" in artists:
	artists.remove("")

last_artist_file = '../data/last_artist.txt'
start = 0
end = len(artists)
if path.exists(last_artist_file):
	#Find song to start on
	last_artist_handle = open(last_artist_file, 'r')
	last_artist = last_artist_handle.read()

	start = artists.index(last_artist)+1
print("Starting from index", start)

spotify_checked_data = '../data/spotify_songs_found_from_artist.txt'
if not(path.exists(spotify_checked_data)):
	#Create File, so it can be appended
	temp = open(spotify_checked_data, 'w')
	temp.close()

result_list = []

min_loop_time = 0.2
min_album_search = 0.2

for ind in range(start,end):

	temp_time = time()
	artist = artists[ind]
	
	print("\nFinding Spotify songs relating to |"+artist+"| --> %.3f%%"%(ind*100/(len(artists)-2)))
	
	artist_info = get_artist(artist)
	artist_albums = get_artist_albums(artist_info)
	print(len(artist_albums), "found")
	for album in artist_albums:
		al_temp_time = time()
		print("  Searching Spotify for album |"+album+"|")
		result = sp.search(q='album: '+album, limit=50)
		
		for track_obj in result['tracks']['items']:
			result_list.append(form_spot_data(track_obj))

		diff = time() - al_temp_time
		if diff < min_album_search:
			sleep(min_album_search-diff)

	result_list = list(dict.fromkeys(result_list))
	print("\n\t%d Unique Songs From Spotify"%(len(result_list)))

	if len(result_list) > 5000:
		write_str = ""
		for song in result_list:
			write_str += song+"\n"
		with open(spotify_checked_data, 'a') as spot_data:
			spot_data.write(write_str)
		with open(last_artist_file, 'w') as last_artist_handle:
			last_artist_handle.write(artist)
		print("Writing %d ID's to file"%(len(result_list)))
		result_list = []

		file_size = path.getsize(spotify_checked_data)
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

	
	diff = time() - temp_time
	if diff < min_loop_time:
		sleep(min_loop_time-diff)

#All artists checked, clean up and save last bits of data	
if len(result_list) > 0:
	write_str = ""
	for song in result_list:
		write_str += song+"\n"
	with open(spotify_checked_data, 'a') as spot_data:
		spot_data.write(write_str)
	with open(last_artist_file, 'w') as last_artist_handle:
		last_artist_handle.write(artist)
	print("Writing %d ID's to file"%(len(result_list)))

file_size = path.getsize(spotify_checked_data)
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

print('\tFINAL File Size: %.1f'%(file_size_adj), unit)

print("\n\n======================================================================")
print("================= ALL SONGS CHECKED AND RECORED! =====================")
print("======================================================================")







