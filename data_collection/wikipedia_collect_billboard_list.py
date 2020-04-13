from googlesearch import search
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
from time import sleep

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

def get_paragraph_txt(soup):

	webpage_txt = ""
	for link in soup.find_all('p'):
		webpage_txt += link.text+" "

	#print(webpage_txt)
	return webpage_txt

def extract_tables(soup):
	tables = []

	for table in soup.find_all('table'):
		try: 
			tables.append(pd.read_html(str(table))[0])
		except:
			continue
	return tables


base = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_'
years = [x for x in range(1946,2020)]
all_songs = pd.DataFrame({'Song Title':[], 'Artist(s)': [], 'Year': []})
print(all_songs)

not_secured = []
num_songs = 0
for year in years:
	url = base + str(year)
	billboard_data = None
	print('Collecting Billboard for '+str(year))
	if scrapable(url):
		#print("\tScrapable: YES")
		soup_obj = make_soup_object(url)
		web_tables = extract_tables(soup_obj)

		if len(web_tables) > 0:
			for table in web_tables:
				if table.shape[0] > 25 and table.shape[1] > 2:
					#print('\tTable Secured!')
					billboard_data = table
					num_songs += billboard_data.shape[0]
					#print("\tAdded Songs: %d"%(billboard_data.shape[0]))
					#print('\tTotal Songs: %d'%(num_songs))
					break
		else:
			not_secured.append(year)
	
	else:
		print("Scrapable: NO")
		not_secured.append(year)

	if billboard_data is None:
		not_secured.append(year)

	else:
		title = []
		if 'Title' in billboard_data.columns:
			title = billboard_data['Title']
		elif 'Song' in billboard_data.columns:
			title = billboard_data['Song']
		else:
			print("SONG TITLE NOT SECURED")

		artists = []
		if 'Artist' in billboard_data.columns:
			artists = billboard_data['Artist']
		elif 'Artist(s)' in billboard_data.columns:
			artists = billboard_data['Artist(s)']
		else:
			print("SONG ARTISTS NOT SECURED")
		
		yr_list = [str(int(year))]*len(title)
	
		reformed_frame = pd.DataFrame({'Song Title':title, 'Artist(s)':artists, 'Year': yr_list})
		
		all_songs = pd.concat([all_songs, reformed_frame], ignore_index = True)
		#print("\tFull Dataset shape: ",all_songs.shape)

	#sleep(2)

print(all_songs)	
print("Number of Songs there should be: "+str(num_songs))	

print("ERRORS IN SECURING TABLE OR WEBPAGE: ", not_secured)

all_songs.to_csv('../data/billboard_songs_1946-2019.csv', index=False)
