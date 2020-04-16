import sys
from os import path

def create_file(file_name):
	hd = open(file_name, 'w')
	hd.close()

def add_suffix(file_name, suff_num):
	folders = file_name.split('/')

	fil = folders[len(folders)-1]
	new_fil = fil.split('.')[0]+'_'+str(suff_num)+'.'+fil.split('.')[1]

	new_name = ''
	for i in range(0, len(folders)-1):
		new_name += folders[i]+'/'
	
	new_name += new_fil
	
	return new_name

def get_combined_file_sizes(file_name, num_files):
	combined_size = 0

	for i in range(0, num_files+1):
		fil = add_suffix(file_name, i)
		combined_size += path.getsize(fil)

	return combined_size

inputfile = ''
if len(sys.argv) > 1:

	all_args = sys.argv
	script_name = all_args[0]

	opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
	args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

	if '-h' in opts:
		print('\nUsage: %s -f <file2breakup>'%(script_name))
		print('Desc:  Breaksup large data files into less 100 MB files of similar name to allow for upload to github')
		exit()
	if '-f' in opts:
		inputfile = all_args[all_args.index('-f')+1]
else:	
	print("Must Specify Some Options!!! -> use -h flag if unsure")
	exit()

if inputfile == '':
	print("Need to specify an input file! --> use -h flag for more info")
	sys.exit()

print('Input file:  |'+inputfile+'|')

if not(path.exists(inputfile)):
	print("ERROR Input File does not exist")
	exit()

with open(inputfile, 'r') as data_handle:
	dataset = data_handle.read().split('\n')

data_size_before = path.getsize(inputfile)
max_file_size = 90*10**6 #90 MB just to be safe

file_cnt = 0
current_file = add_suffix(inputfile, file_cnt)
create_file(current_file)

print("Starting at", current_file)

for data in dataset:
	with open(current_file, 'a') as file_handle:
		file_handle.write(data+'\n')
	
	file_size = path.getsize(current_file)
	if file_size > max_file_size:
		print("\nFile Size above maximum size: %.2f MB"%(file_size/(10**6)))
		file_cnt += 1
		current_file = add_suffix(inputfile, file_cnt)
		create_file(current_file)
		print("Starting New File:", current_file)

if abs(data_size_before - get_combined_file_sizes(inputfile, file_cnt)) > 5:
	print("ERROR: DATA DOES NOT ADD UP -->", data_size_before, "|", get_combined_file_sizes(inputfile, file_cnt))
else:
	print("Good Split! --> All Done")
		
	
