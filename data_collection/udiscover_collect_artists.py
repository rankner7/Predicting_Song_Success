from googlesearch import search
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd

num_returned = num_stop = 10

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

def search_google(search_query, num_to_search, key_phrase):
	found_url = None
	for result in search(search_query,        # The query you want to run
                tld = 'com',  # The top level domain
                lang = 'en',  # The language
                num = num_to_search,     # Number of results per page
                start = 0,    # First result to retrieve
                stop = num_to_search,  # Last result to retrieve
                pause = 2.0,  # Lapse between HTTP requests
               ):

		if result.find(key_phrase) != -1 and scrapable(result):
			found_url = result
			break
	return found_url

def make_soup_object(stock_url):
	req = Request(url=stock_url, headers=headers) 
	html = urlopen(req).read() 

	soup = BeautifulSoup(html, 'html.parser')
		
	return soup

def extract_artists(soup):
	artists = []

	for link in soup.find_all('a'):
		url = link.get('href')
		txt = link.text
		if url is not(None) and url.find('/artists/') != -1:
			artists.append(txt)
	
	return artists
	
url = 'https://www.udiscovermusic.com/artists-a-z/'
output_file = '../data/artist_list.txt'

if scrapable(url):
	print("Scrapable: YES")
	soup_obj = make_soup_object(url)
	artists = extract_artists(soup_obj)
	with open(output_file, 'w') as ofile_h:
		for artist in artists:
			ofile_h.write(artist+'\n')
	print("Artist List Written To File")

else:
	print("Scrapable: NO")

