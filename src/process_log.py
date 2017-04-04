# import csv
from datetime import datetime
import operator
import re
from collections import defaultdict
import numpy as np
from pathlib import Path
request = []
host = []
date_in_file = []
bytes_sent = []
replycode = []
num_lines = 0
parent_path = Path(__file__).parents[1]
print('starting to read the file\n')
file_path = Path.joinpath(parent_path,'log_input/log.txt').__str__()
output_path = Path.joinpath(parent_path,'log_output')
with open(file_path, encoding="Latin-1") as f:
    for line in f:
        new_param = line.split()
        quotes = re.findall(r'"[^"]*"', line, re.U)
        temp = quotes.__str__()
        request.append(temp[3:-3])
        host.append(new_param[0])
        date_in_file.append(new_param[3][1:])
        replycode.append(new_param[-2])
        bytes_sent.append(new_param[-1])
        num_lines = num_lines+1
print('finished reading the file\n')
# make a dictionary of indicies
print('preparation for the features\n')
unique_host, unique_index, unique_inverse, occ = np.unique(
    host, return_index=True, return_counts=True, return_inverse=True)
index_dict = defaultdict(list)
for k in range(len(unique_inverse)):
    index_dict[unique_inverse[k]].append(k)
# ### feature 1
print('starting feature 1\n')
sort_occ = sorted(occ, reverse=True)
index = sorted(range(len(occ)), reverse=True, key=lambda z: occ[z])
file_path1 = Path.joinpath(output_path, 'hosts.txt').__str__()
with open(file_path1, "w") as f:
    f.writelines(map("{},{}\n".format, unique_host[index[0:10]], sort_occ[0:10]))
f.close()

# ### feature 2
print('starting feature 2\n')
bytes_sent = [w.replace('-', '0') for w in bytes_sent]
bytes_sent = list(map(int, bytes_sent))
bytes_sent = np.asarray(bytes_sent)
tot_bytes = defaultdict(int)
for k in range(len(unique_inverse)):
    tot_bytes[unique_inverse[k]] += bytes_sent[k]
highest_bytes_to_print = 10   # find highest 10
sorted_tot_bytes = sorted(tot_bytes.items(), key=operator.itemgetter(1), reverse=True)
highest_bytes_host = []
for k in range(highest_bytes_to_print):
    highest_bytes_host.append(unique_host[sorted_tot_bytes[k][0]])
file_path2 = Path.joinpath(output_path, 'resources.txt').__str__()
thefile = open(file_path2, 'w')
for item in highest_bytes_host:
    thefile.write("%s\n" % item)
thefile.close()
# ## Feature 3
# find busiest hour period .. use dictionary for day and hours
print('starting feature 3\n')
hour_dict = defaultdict(int)
highest_periods_to_print = 10
busiest_period = []
occ_period = []
for k in range(len(date_in_file)):
    hour_dict[date_in_file[k][0:-6]] += 1
sorted_hour_dec = sorted(hour_dict.items(), key=operator.itemgetter(1), reverse=True)
for k in range(highest_periods_to_print):
    busiest_period.append(sorted_hour_dec[k][0] + ":00:00 -0400")
    occ_period.append(sorted_hour_dec[k][1])
file_path3 = Path.joinpath(output_path, 'hours.txt').__str__()
with open(file_path3, "w") as f:
    f.writelines(map("{},{}\n".format, busiest_period, occ_period))
f.close()
# ### feature 4
print('starting feature 4\n')
blocked_dict = defaultdict(list)
replycode = list(map(int, replycode))
pat = [401, 401, 401]
l = []
for key, value in index_dict.items():
    l = [replycode[i] for i in value]
    # temp_a = []
    temp_a = [i for i, x in enumerate(l) if(l[i:i+len(pat)] == pat)]
    if temp_a:
        t = [date_in_file[i] for i in value]
        t_format = [datetime.strptime(ll, '%d/%b/%Y:%H:%M:%S') for ll in t]
        index_to_print = []
        for x in temp_a:
            time_diff = (t_format[x+2] - t_format[x]).total_seconds()
            if time_diff <= 20:
                all_time_diff = [(ll - t_format[x+2]).total_seconds() for ll in t_format]
                find_index_to_print = [i for i, x in enumerate(all_time_diff) if 0 < x <= 5*60]
                index_to_print.extend(find_index_to_print)
        unique_index_to_print = set(index_to_print)
        blocked_dict[key] = [list(value)[x] for x in unique_index_to_print]
v = blocked_dict.values()
v_list = [item for sublist in v for item in sublist]
file_path4 = Path.joinpath(output_path, 'blocked.txt').__str__()
fileID = open(file_path4, 'w')
for x in v_list:
    print('{:s} - - [{:s} -0400] "{:s}" {:d} {:d}\n'.format(
        host[x], date_in_file[x], request[x], replycode[x], bytes_sent[x]), end='', file=fileID)
fileID.close()
print('end of features\n')
# bonus feature .. .find the hours of days for all blocked users access to monitor their traffic print out host, hour, number of access, total occ