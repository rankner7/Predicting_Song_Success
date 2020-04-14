import sys
from os import path

inputfile = ''
outputfile = ''
if len(sys.argv) > 1:

	all_args = sys.argv
	script_name = all_args[0]

	opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
	args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

	if '-h' in opts:
		print('\nUsage: %s -d <dirtyfile> [-c] <cleanfile>'%(script_name))
		print('Desc:  Script Sorts data, Removes Empty Lines and Removes duplicate lines from a data file')
		print('Tips:\n  1) If cleanfile is not specified, cleaned data will overwrite data in the same input file (dirtyfile)\n')
		exit()
	if '-d' in opts:
		inputfile = all_args[all_args.index('-d')+1]
	if '-c' in opts:
		outputfile = all_args[all_args.index('-c')+1]
		
	
else:	
	print("Must Specify Some Options!!! -> use -h flag if unsure")
	exit()

if inputfile == '':
	print("Need to specify a dirty file! --> use -h flag for more info")
	sys.exit()
if outputfile == '':
	outputfile = inputfile
print('Input file:  |'+inputfile+'|')
print('Output file: |'+outputfile+'|')

if not(path.exists(inputfile)):
	print("ERROR Input File does not exist")
	exit()

print("Good to go!")

with open(inputfile, 'r') as bill_handle:
	bill_data = bill_handle.read().split('\n')

while "" in bill_data:
	bill_data.remove("")

print("\nLine Count Before:", len(bill_data))
bill_data.sort()
dup_cnt = 0
duplicates = []
for i in range(0, len(bill_data)-1):
	if bill_data[i] == bill_data[i+1]:
		dup_cnt += 1
		duplicates.append(bill_data[i])
		#print("DUPLICATE ENTRY")
		#print('\t-->', bill_data[i])
		#print('\t-->', bill_data[i+1])

print(dup_cnt, "Duplicates")

bill_data = list(dict.fromkeys(bill_data))
print("Line Count After:", len(bill_data))
print("Percent Unique: %.2f%%"%(len(bill_data)*100/(len(bill_data)+dup_cnt)))


with open(outputfile, 'w') as bill_handle:
	for bill in bill_data:
		bill_handle.write(bill+'\n')

print("Updated List re-written")
