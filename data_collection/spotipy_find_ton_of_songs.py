import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep, time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from os import path

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

def scrapable(url_to_check):
	req = Request(url=url_to_check, headers=headers)
	readable = False
	try:
		html = urlopen(req).read()
		readable = True
		#print("\tStock is Good to Go Boss")
	except:
		print("\tERROR: Can't Read Boss")
	return readable

def make_soup_object(stock_url):
	req = Request(url=stock_url, headers=headers) 
	html = urlopen(req).read() 

	soup = BeautifulSoup(html, 'html.parser')
		
	return soup

def get_paragraph_txt(soup):

	webpage_txt = ""
	for link in soup.find_all('p'):
		webpage_txt += link.text+" "

	#print(webpage_txt)
	return webpage_txt

def form_spot_data(track):
	artists = ""
	for artist in track['artists']:
		artists += artist['name']+"/"
	return track['name']+'||'+artists+'||'+track['album']['release_date']+'||'+str(track['duration_ms'])+'||'+track['id']+'||'+str(track['popularity'])+'\n'

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

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

with open('../data/all_songs_1946-2019.txt', 'r') as song_name_handle:
	song_name_data = song_name_handle.read()

songs = song_name_data.split('\n')

website_base = 'https://en.wikipedia.org/'

last_song_file = '../data/last_song_ton.txt'
start = 0
if path.exists(last_song_file):
	#Find song to start on
	last_song_handle = open(last_song_file, 'r')
	last_song = last_song_handle.read()

	start = songs.index(last_song)+1
print("Starting from index", start)

spotify_checked_data = '../data/spotify_ton_of_songs.txt'
if not(path.exists(spotify_checked_data)):
	#Create File, so it can be appended
	temp = open(spotify_checked_data, 'w')
	temp.close()

id_list = []

min_time = 0.3

for ind in range(start,len(songs)-1):
	temp_time = time()
	song_name = songs[ind].split('||')[0]
	song_year = songs[ind].split('||')[1]
	
	print("\nFinding Spotify songs relating to |"+song_name+"| ["+song_year+"] --> %.3f%%"%(ind*100/(len(songs)-2)))
	

	max_limit = 50
	result = sp.search(q = song_name, limit = max_limit)

	for track_obj in result['tracks']['items']:
		id_list.append(form_spot_data(track_obj))

	id_list = list(dict.fromkeys(id_list))
	print("\t%d Unique Song ID's From Spotify"%(len(id_list)))

	if len(id_list) > 5000:
		write_str = ""
		for ID in id_list:
			write_str += ID+"\n"
		with open(spotify_checked_data, 'a') as spot_data:
			spot_data.write(write_str)
		with open(last_song_file, 'w') as last_song_handle:
			last_song_handle.write(songs[ind])
		print("Writing %d ID's to file"%(len(id_list)))
		id_list = []
	
	diff = time() - temp_time
	if diff < min_time:
		sleep(min_time-diff)
	

print("\n\n======================================================================")
print("================= ALL SONGS CHECKED AND RECORED! =====================")
print("======================================================================")

if len(id_list) > 0:
	write_str = ""
	for ID in id_list:
		write_str += ID+"\n"
	with open(spotify_checked_data, 'a') as spot_data:
		spot_data.write(write_str)
	with open(last_song_file, 'w') as last_song_handle:
		last_song_handle.write(songs[ind])
	print("Writing %d ID's to file"%(len(id_list)))







