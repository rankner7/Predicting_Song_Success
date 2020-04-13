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

main_sections = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
sub_sections = ['a', 'e', 'j', 'o', 't']

sections = ['0–9']
for sect in main_sections:
	sections.append(sect)
	for sub in sub_sections:
		sections.append(sect+sub)


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

def extract_links(soup):
	links = {}

	for link in soup.find_all('a'):
		url = link.get('href')
		txt = link.text
		if url is not(None):
			links[txt] = url
	
	return links

def get_section_links(soup):
	section_links = {}
	
	all_links = extract_links(soup)
	for key in all_links:
		if key in sections:
			section_links[key] = all_links[key]
	
	#for key in section_links:
	#	print(key+":\t"+section_links[key])

	return section_links

def get_last_section_header(soup):
	div_list = soup.find_all('div', class_='mw-category-generated')
	song_names = []
	last_letter = ''
	if len(div_list) == 1:
		songs_div = soup.find_all('div', class_='mw-category-generated')[0]
		for header in songs_div.find_all('h3'):
			last_letter = header.text
	else:
		print("ERROR GETTING HEADERS -> FORMAT CHANGED")
	
	return last_letter

def get_song_names(soup, year):
	div_list = soup.find_all('div', class_='mw-category-generated')
	song_names = []
	last_letter = ''
	if len(div_list) == 1:
		songs_div = soup.find_all('div', class_='mw-category-generated')[0]
		for lst in songs_div.find_all('ul'):
			#print('\n')
			section_links = extract_links(lst)
			for key in section_links:
				#print(key+":\t"+section_links[key])
				song_names.append(key+"||"+str(year)+"||"+section_links[key])
				
			
	else:
		print("ERROR GETTING SONG NAMES -> FORMAT CHANGED")

	return song_names

def get_all_songs(soup, year):
	last_letter = '0–9'
	last_sub = 0
	letter_before = last_letter
	page_sections = get_section_links(soup)
	all_songs = []
	
	print("\n\tChecking Base Page")

	while True:
		new_songs = get_song_names(soup, year)
	
		all_songs += new_songs

		print('\tLetter: '+last_letter+" | sub: "+sub_sections[last_sub])
		last_letter = get_last_section_header(soup)

		if last_letter == '':
			break

		if len(page_sections.keys()) == 0:
			break

		if (last_letter == letter_before):
			for i in range(last_sub, len(sub_sections)):
				last_sub = i
				key = last_letter+sub_sections[i]
				if key in page_sections:
					url = page_sections[key]
					break
			last_sub += 1
			if last_sub == len(sub_sections):
				break
		else:
			last_sub = 0
			url = page_sections[last_letter]

		letter_before = last_letter

		print("\tScraping Letter |"+last_letter+"| with url: "+url)
		soup = make_soup_object(url)
	
	print("\n\tSongs before Pruning: "+str(len(all_songs)))
	#Remove Duplicates
	all_songs = list(dict.fromkeys(all_songs))
	
	print("\tSongs after Pruning: "+str(len(all_songs)))
	

	return all_songs

song_file = '../data/all_songs_1946-2019.txt'
#song_file = 'data/test.txt'

years = [x for x in range(1946, 2020)]

full_song_list = []
song_cnts = []
for year in years:
	print("\n\nPulling Songs from "+str(year))
	url = 'https://en.wikipedia.org/wiki/Category:'+str(year)+'_songs'
	if scrapable(url):
		print("\tScrapable: YES")
		soup_obj = make_soup_object(url)
	
		new_songs = get_all_songs(soup_obj, year)
		full_song_list += new_songs

		song_cnts.append(len(new_songs))

	else:
		print("Scrapable: NO")

print('======================= DONE =========================')
print('Total Number of Songs: '+str(len(full_song_list)))

full_song_list = list(dict.fromkeys(full_song_list))

print('Total Number of UNIQUE Songs: '+str(len(full_song_list)))
print('\n\n===================== FULL SONG COUNT ==========================')

for i, year in enumerate(years):
	print(str(year)+":   "+str(song_cnts[i]))

song_file_handle = open(song_file, 'w')
for song in full_song_list:
	song_file_handle.write(song+'\n')
song_file_handle.close()
print("ALL SONGS WRITTEN TO FILE")




