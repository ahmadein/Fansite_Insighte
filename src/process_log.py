# import csv
from datetime import datetime
import operator
import re
from collections import defaultdict
from collections import OrderedDict
import numpy as np
from pathlib import Path
import sys
import pickle
import argparse
from collections import Counter


class ChallengeInsight:
    def __init__(self, file_path, output_path):
        self.request = []
        self.host = []
        self.date_in_file = []
        self.bytes_sent = []
        self.replycode = []
        self.date_datetime = None
        self.index_dict = defaultdict(list)
        self.unique_host = None
        self.unique_index = None
        self.unique_inverse = None
        self.occ = None
        self.blocked = None
        self.parent_path = Path(__file__).parents[1]  # get the repo parent's path
        self.data_path = Path.joinpath(self.parent_path, 'data_stored/objs.pickle').__str__()
        self.file_path = file_path
        self.output_path = output_path
        if self.output_path is None:
            self.output_path = Path.joinpath(self.parent_path, 'log_output')
        if self.file_path is None:
            self.file_path = Path.joinpath(self.parent_path, 'log_input/log.txt').__str__()

    def save_pickle(self):
        """
        Saves Data Parsed from log file into pickle file for next fast processing
        """
        print('storing data in {:s}'.format(self.data_path))
        with open(self.data_path, 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([self.host, self.date_in_file, self.request, self.replycode, self.bytes_sent], f)

    def read_pickle(self):
        """
        Read data from a pickle file already saved .. faster than parsing the file every time
        """
        try:
            print('reading from stored data in {:s}'.format(self.data_path))
            with open(self.data_path, 'rb') as f:  # Python 3: open(..., 'rb')
                self.host, self.date_in_file, self.request, self.replycode, self.bytes_sent = pickle.load(f)
        except:
            print('error while opening file .. exiting')
            return 1

    def parse_file(self):
        """
        Function that read a log file and parse it
        """
        print('starting to read the file\n')
        formatting = r'(.*) - - \[(.*) -.*\] \"(.*)\" (\d+) (\d+|-)'
        # using regex as it is cleaner and without hard coding
        pattern = re.compile(formatting)
        with open(self.file_path, encoding="Latin-1") as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    self.host.append(match.group(1))
                    self.date_in_file.append(match.group(2))
                    self.request.append(match.group(3))
                    self.replycode.append(int(match.group(4)))
                    if match.group(5) == '-':
                        self.bytes_sent.append('0')
                    else:
                        self.bytes_sent.append(match.group(5))
                else:
                    print('found corrupted line {:s} \n'.format(line))
                    # new_param = line.split()
                    # quotes = re.findall(r'"[^"]*"', line, re.U)
                    # temp = quotes.__str__()
                    # request.append(temp[3:-3])
                    # host.append(new_param[0])
                    # date_in_file.append(new_param[3][1:])
                    # replycode.append(new_param[-2])
                    # bytes_sent.append(new_param[-1])
        print('finished reading the file\n')

    def preprocess(self, feature_to_run):
        """
                make a dictionary of indices and unique and occurrences of host
        """
        print('preparation for the features\n')
        self.unique_host, self.unique_index, self.unique_inverse, self.occ = np.unique(self.host, return_index=True,
                                                                                       return_counts=True,
                                                                                       return_inverse=True)
        for k in range(len(self.unique_inverse)):
            self.index_dict[self.unique_inverse[k]].append(k)  # dict of each host and the line index it happened at
        # bytes_sent = [w.replace('-', '0') for w in bytes_sent]
        self.bytes_sent = list(map(int, self.bytes_sent))  # change bytes to int
        self.bytes_sent = np.asarray(self.bytes_sent)

        # if 3 in feature_to_run:
        #    self.date_datetime = [datetime.strptime(ll, '%d/%b/%Y:%H:%M:%S') for ll in self.date_in_file]

    def do_feature1(self):
        # ### feature 1
        print('starting feature 1\n')
        sort_occ = sorted(self.occ, reverse=True)  # sort number of occurances
        index = sorted(range(len(self.occ)), reverse=True, key=lambda z: self.occ[z])
        file_path1 = Path.joinpath(self.output_path, 'hosts.txt').__str__()
        with open(file_path1, "w") as f:  # print
            f.writelines(map("{},{}\n".format, self.unique_host[index[0:10]], sort_occ[0:10]))
        f.close()

    def do_feature2(self):
        """
        feature 2: Identify the 10 resources that consume the most bandwidth on the site         
        """
        print('starting feature 2\n')
        tot_bytes = defaultdict(float)
        for k in range(len(self.request)):
            tot_bytes[self.request[k]] += self.bytes_sent[k]  # count number of bytes for each request using dict
        highest_bytes_to_print = min(len(tot_bytes), 10)  # find highest 10
        sorted_tot_bytes_keys = sorted(tot_bytes.items(), key=operator.itemgetter(1), reverse=True)
        file_path2 = Path.joinpath(self.output_path, 'resources.txt').__str__()
        thefile = open(file_path2, 'w')
        formatting = r'(/.*) '
        formatting1 = r'(/.*)'
        pattern = re.compile(formatting)  # sometimes request does not have any HTTP after so either format or format1
        pattern1 = re.compile(formatting1)
        for k in range(highest_bytes_to_print):
            match = pattern.search(sorted_tot_bytes_keys[k][0])
            if match is None:
                match = pattern1.search(sorted_tot_bytes_keys[k][0])
            s = match.group(1)
            thefile.write("%s\n" % s)
        thefile.close()

    def do_feature3(self):
        """
        find busiest hour period .. use dictionary for day and hours
        """
        print('starting feature 3\n')
        hour_dict = defaultdict(int)
        busiest_period = []
        occ_period = []
        for k in range(len(self.date_in_file)):
            hour_dict[self.date_in_file[k][0:-6]] += 1
        sorted_hour_dec = sorted(hour_dict.items(), key=operator.itemgetter(1), reverse=True)
        highest_periods_to_print = min(len(sorted_hour_dec), 10)
        for k in range(highest_periods_to_print):
            busiest_period.append(sorted_hour_dec[k][0] + ":00:00 -0400")
            occ_period.append(sorted_hour_dec[k][1])
        file_path3 = Path.joinpath(self.output_path, 'hours.txt').__str__()
        with open(file_path3, "w") as f:
            f.writelines(map("{},{}\n".format, busiest_period, occ_period))
        f.close()

        def do_try_feature3(self):
            hour_dict = OrderDict()
            for items in self.date_in_file:
                hour_dict[items] = 0
            for items in self.date_in_file:
                hour_dict[items] += 1




    # def do_feature3(self):
    #     # ## Feature 3
    #     # find busiest hour period .. use dictionary for day and hours
    #     print('starting feature 3\n')
    #     hour_dict = defaultdict(int)
    #     highest_periods_to_print = 10
    #     busiest_period = []
    #     occ_period = []
    #     for k in range(len(self.date_in_file)):
    #         hour_dict[self.date_in_file[k]] += 1
    #     sorted_hour_dec = sorted(hour_dict.items(), key=operator.itemgetter(1), reverse=True)
    #     highest_periods_to_print = min(len(sorted_hour_dec), 10)
    #     for k in range(highest_periods_to_print):
    #         busiest_period.append(sorted_hour_dec[k][0] + ":00:00 -0400")
    #         occ_period.append(sorted_hour_dec[k][1])
    #     file_path3 = Path.joinpath(self.output_path, 'hours.txt').__str__()
    #     with open(file_path3, "w") as f:
    #         f.writelines(map("{},{}\n".format, busiest_period, occ_period))
    #     f.close()

    def do_feature4(self):
        """
        feature 4 
        """
        print('starting feature 4\n')
        blocked_dict = defaultdict(list)
        pat = [401, 401, 401]  # the pattern of three consecutive failures
        for key, value in self.index_dict.items():
            l = [self.replycode[i] for i in value]
            # temp_a = []
            temp_a = [i for i, x in enumerate(l) if (l[i:i + len(pat)] == pat)]  # find who has 3 consecutive failures
            if temp_a:
                t = [self.date_in_file[i] for i in value]
                t_format = [datetime.strptime(ll, '%d/%b/%Y:%H:%M:%S') for ll in t]
                index_to_print = []
                for x in temp_a:
                    time_diff = (t_format[x + 2] - t_format[x]).total_seconds()
                    # among those with 3 find if they are within 20 sec
                    if time_diff <= 20:
                        all_time_diff = [(ll - t_format[x + 2]).total_seconds() for ll in t_format]
                        find_index_to_print = [i for i, x in enumerate(all_time_diff) if 0 < x <= 5 * 60]
                        index_to_print.extend(find_index_to_print)   # get all their events for the next 5 minutes
                        # get the unique list of events in case more than 3 consecutive failures
                unique_index_to_print = set(index_to_print)
                blocked_dict[key] = [list(value)[x] for x in unique_index_to_print]
        v = blocked_dict.values()
        self.blocked = blocked_dict.keys()
        v_list = [item for sublist in v for item in sublist]
        file_path4 = Path.joinpath(self.output_path, 'blocked.txt').__str__()
        fileID = open(file_path4, 'w')
        for x in v_list:
            print('{:s} - - [{:s} -0400] "{:s}" {:d} {:d}\n'.format(
                self.host[x], self.date_in_file[x], self.request[x], self.replycode[x], self.bytes_sent[x]), end='',
                file=fileID)
        fileID.close()

    def do_feature5(self):
        """
        bonus feature .. .find the hours of days for all blocked users access to monitor their traffic 
        print out host, hour, number of access 
        """
        print('starting feature 5\n')
        blocked_hour_dic = defaultdict(list)
        for key in self.blocked:  # find the hours for blocked users
            temp_hr_list = [int(self.date_in_file[i][12:14]) for i in self.index_dict[key]]
            most_common, num_most_common = Counter(temp_hr_list).most_common(1)[0]  # find most common hour per user
            blocked_hour_dic[key] = [most_common, num_most_common]
        file_path5 = Path.joinpath(self.output_path, 'blocked_hours.txt').__str__()
        fileID = open(file_path5, 'w')
        for key, value in blocked_hour_dic.items():
            print('{:s}, {:d}, {:d} \n'.format(self.unique_host[key], value[0], value[1]), end='', file=fileID)
            # print host , hours, number of occurances
        fileID.close()
        print('end of features\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input_file", metavar="FILE NAME", required=False)
    parser.add_argument("-f", "--features", type=int, required=False, nargs='+', default=[1, 2, 3, 4, 5],
                        help="Enter list of features to run")
    parser.add_argument("-s", "--save_pickle", action='store_true', required=False, default=False,
                        help="Dump data to pickle file")
    parser.add_argument("-r", "--read_pickle", action='store_true', required=False, default=False,
                        help="Read data from pickle file instead of log")
    parser.add_argument("-out", "--output_dir", metavar="Output Folder", required=False)
    args = parser.parse_args()
    # obtained the arguments passed to the fi

    file_path = args.input_file
    read_pickle = args.read_pickle
    features_to_run = args.features
    save_pickle = args.save_pickle
    output_path = args.output_dir

    solver = ChallengeInsight(file_path, output_path)  # initiate class
    print('read from file {:s},\n output path is {:s}\n, features to run is {:s}, \n'
          'save data to pickle is {:s} and read from pickle is {:s}\n'.format(solver.file_path, str(solver.output_path),
                                                            str(features_to_run), str(save_pickle), str(read_pickle)))

    if read_pickle:
        solver.read_pickle()   # read from pickle file if specified
    else:
        solver.parse_file()    # otherwise parse the log file

    if save_pickle:
        solver.save_pickle()   # save in pickle file

    solver.preprocess(features_to_run)

    if 1 in features_to_run:
        solver.do_feature1()

    if 2 in features_to_run:
        solver.do_feature2()

    if 3 in features_to_run:
        solver.do_feature3()

    if 4 in features_to_run or 5 in features_to_run:  # feature 4 is mandatory to run if feature 5 was to run alone
        solver.do_feature4()

    if 5 in features_to_run:
        solver.do_feature5()

    return 0


if __name__ == "__main__":
    return_code = main()
    sys.exit(return_code)
