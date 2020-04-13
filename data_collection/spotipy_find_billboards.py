import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep, time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from os import path
import pandas as pd

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

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

billboard_songs = pd.read_csv('../data/billboard_songs_1946-2019.csv', index_col=False)
end = billboard_songs.shape[0]


last_song_file = '../data/last_song_bill.txt'
start = 0
if path.exists(last_song_file):
	#Find song to start on
	last_song_handle = open(last_song_file, 'r')
	last_song = last_song_handle.read()

	song_list = billboard_songs['Song Title'].tolist()
	start = song_list.index(last_song) + 1

print("Starting from index", start)

spotify_checked_data = '../data/spotify_billboard_songs.txt'
if not(path.exists(spotify_checked_data)):
	#Create File, so it can be appended
	temp = open(spotify_checked_data, 'w')
	temp.close()
	
wait_time = 0.3

for ind in range(start,end):
	start_time = time()
	song_name = billboard_songs.iloc[ind]['Song Title']
	song_artist = billboard_songs.iloc[ind]['Artist(s)']
	song_year = str(billboard_songs.iloc[ind]['Year'])
	
	print("\n\nFinding Spotify info for |"+song_name+"| by "+song_artist+" ["+song_year+"] --> %.3f%%"%(ind*100/(end-1)))
	
	max_limit = 50
	result = sp.search(q = song_name, limit = max_limit)

	found = False
	best_match = None
	max_similarity = 0

	for i,track_obj in enumerate(result['tracks']['items']):
		similarity_cnt = 0
		
		year = track_obj['album']['release_date'].split('-')[0]
		if year == song_year:
			similarity_cnt += 1

		for artist in track_obj['artists']:
			if song_artist.find(artist['name']) != -1:
				similarity_cnt += 1
		
		if similarity_cnt > max_similarity:
			found = True
			max_similarity = similarity_cnt
			best_match = track_obj

		#if similarity_cnt > 0:
		#	print_track_info(track_obj)
		#	print('\n')
			

	if not(found):
		print("\tSONG NOT FOUND")

	else:
		print('\t============================================================')
		print("\tBest Match:")
		print("\tMatched Artists:", end = " ")
		for artist in track_obj['artists']:
			if song_artist.find(artist['name']) != -1:
				print(artist['name']+",", end=" ")
		print("\n\tSimilarity:", max_similarity,'\n')
				
		print_track_info(best_match)
		print('\t============================================================')
		with open(spotify_checked_data, 'a') as spot_data:
			spot_data.write(form_spot_data(best_match))
				
		

	with open(last_song_file, 'w') as last_song_handle:
		last_song_handle.write(song_name)

	diff = time()-start_time
	if diff < wait_time:
		print("Processed too fast! Waiting for %.3f s"%(wait_time-diff))
		sleep(wait_time-diff) #Make sure we don't get fcuked by spotify's rate limiting

print("\n\n======================================================================")
print("================= ALL SONGS CHECKED AND RECORED! =====================")
print("======================================================================")







