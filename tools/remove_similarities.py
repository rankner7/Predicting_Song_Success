from time import time, sleep
import sys
from os import path
import pandas as pd

letters = 'abcdefghijklmnopqrstuvxyz'

def cleaned(temp_list):
	before = len(temp_list)
	temp_list = list(dict.fromkeys(temp_list))
	after = len(temp_list)
	if before != after:
		return False

	pre_sort = temp_list
	temp_list.sort()
	if pre_sort != temp_list:
		return False

	return True

def remove_null_items(temp_list):
	while "" in temp_list:
		temp_list.remove("")
	
	return temp_list


def prompt_user(prompt):
	while True:
		confirmation = input(prompt+"(y/n): ")
		if confirmation == 'y':
			break
		elif confirmation == 'n':
			print("No Recieved, Exiting")
			exit()
		else:
			print("Invalid Response: enter 'y' or 'n'")
	

removefile = ''
checkfile = ''
if len(sys.argv) > 1:

	all_args = sys.argv
	script_name = all_args[0]

	opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
	args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

	if '-h' in opts:
		print('\nUsage: %s -r <removefile> -c <checkfile>'%(script_name))
		print('Desc:  Checks for duplictes between the two files given and')
		print('Tips:\n  1) Duplicates between files will be REMOVED from the removefile')
		print('  2) Make sure to run both files through clean_data.py first -> errors and/or bad results otherwise\n')
		exit()
	if '-r' in opts:
		removefile = all_args[all_args.index('-r')+1]
	if '-c' in opts:
		checkfile = all_args[all_args.index('-c')+1]
		
	
else:	
	print("Must Specify Some Options!!! -> use -h flag if unsure")
	exit()

if checkfile == '':
	print("\nERROR: Need to specify a CHECK file! --> use -h flag for more info\n")
	sys.exit()
if removefile == '':
	print("\nERROR: Need to specify REMOVE file! --> use -h flag for more info\n")
	sys.exit()

if not(path.exists(checkfile)):
	print("ERROR: CHECK File does not exist\n")
	exit()
if not(path.exists(removefile)):
	print("ERROR: REMOVE File does not exist\n")
	exit()

with open(checkfile, 'r') as bill_handle:
	check_list = bill_handle.read().split('\n')

with open(removefile, 'r') as all_handle:
	remove_list = all_handle.read().split('\n')

check_list = remove_null_items(check_list)
remove_list = remove_null_items(remove_list)

print("\nRemove List Count:", len(remove_list))
print("Check List Count:", len(check_list))
print("\nRemove List preview:", remove_list[0:2])
print("Check List preview:", check_list[0:2])

if not(cleaned(check_list)):
	print("\nERROR: You clearly didnt CHECK FILE run the file through clean_data :/ (I would know). Read -h flag output and make sure to run both files through clean_data.py first\n")
	exit()

if not(cleaned(remove_list)):
	print("\nERROR: You clearly didnt REMOVE FILE run the file through clean_data :/ (I would know). Read -h flag output and make sure to run both files through clean_data.py first\n")
	exit()

print('\nREMOVE file:  |'+removefile+'|')
print('Check file: |'+checkfile+'|')

prompt_user("\nAre these file locations correct?")

removed = 0
updated_list = []
int_perc_done = 0

remove_ind = check_ind = 0
start_time = time()

while remove_ind < len(remove_list):
	if remove_list[remove_ind] > check_list[check_ind]:
		#print('    R Greater --> C++')
		check_ind += 1
	else:
		if remove_list[remove_ind] == check_list[check_ind]:
			#Strings are Equal --> Item Found
			removed += 1
			remove_ind +=1
		else:
			#Less Than --> Item was not found
			updated_list.append(remove_list[remove_ind])
			remove_ind += 1

	if check_ind == len(check_list):
		updated_list += remove_list[remove_ind:]
		break

print("Run Time: %.2f s"%(time()-start_time))

print('\n',removed, "To Be Removed! Updated Count:")
print("\tUpdated List:     ", len(updated_list))
print("\tRemove List Count:", len(remove_list))
print("\tDifference:       ", (len(remove_list)-len(updated_list)))

if removed != (len(remove_list)-len(updated_list)):
	print('*********** DIFFERENCE IN REMOVAL SIZES --> DATA BEING LOST **********************')
	print("Not writing to file, exiting")
	exit()

if removed > 0:
	print("Changes to be written to:", removefile)
	prompt_user("\nIs this correct?")

	with open(removefile, 'w') as all_handle:
		for entry in updated_list:
			all_handle.write(entry+'\n')
	print("Updated List written to file")

else:
	print("No Similarities! --> Nothing to do")


	

