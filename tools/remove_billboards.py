from time import time

with open('data/spotify_billboard_songs.txt', 'r') as bill_handle:
	bill_ids = bill_handle.read().split('\n')

with open('data/spotify_ton_of_songs.txt', 'r') as all_handle:
	all_ids = all_handle.read().split('\n')

for a in all_ids:
	if len(a) == 0:
		all_ids.remove(a)
for a in bill_ids:
	if len(a) == 0:
		bill_ids.remove(a)

print("Billboard Songs:", len(bill_ids))
bill_ids = list(dict.fromkeys(bill_ids))
print("Billboard Songs Unique:", len(bill_ids))

print("All Songs:", len(all_ids))
print("\nBillboard preview:", bill_ids[0:5])
print("\nAll Song preview:", all_ids[0:5])

removed = 0
updated_ids = []
int_perc_done = 0

loop_list = all_ids
check_list = bill_ids

start_time = temp_time = time()
for i,aid in enumerate(loop_list):
	perc_done = i*100/(len(loop_list)-1)
	if int_perc_done != int(perc_done):
		int_perc_done = int(perc_done)
		last_perc_time = time()-temp_time
		time_left = (100-int_perc_done)*last_perc_time/60
		print("Progress --> %d%% Time Left: %.2f min  Time Taken: %.3fs"%(int_perc_done, time_left, last_perc_time))
		temp_time = time()
		
	if aid in check_list:
		removed += 1
	else:
		updated_ids.append(aid)

print("Run Time: %.2f  min"%((time()-start_time)/60))

print('\n',removed, "Removed! Updated Count:")
print("Updated Songs:", len(updated_ids))
print("All Songs:", len(all_ids))
print("Difference:", (len(all_ids)-len(updated_ids)))

if removed > 0:
	with open('data/spotify_ton_of_songs.txt', 'w') as all_handle:
		for ID in updated_ids:
			all_handle.write(ID+'\n')
	print("Updated ID list written to file")
else:
	print("No Similarities! --> Nothing to do")


	

