# Table of Contents
1. [Project Summary](README.md#Insight-Fansite)
2. [Details of Implementation](README.md#details-of-implementation)
3. [List of Implemented Features ](README.md#list-features)
4. [Getting Started](README.md#getting-started)
5. [## Prerequisites](README.md#pre)
6. [Dependencies](README.md#dep)
7. [IHow to Run](README.md#run)
8. [Running the tests](README.md#testing)


# Insight Fansite

This project is to tackle the insight data challenge. The target is to read and process large log files from the site as quick as possible

## Details of Implementation

The code is implemented in Python 3 and is not guaranteed to be compatiable with Python 2. The problem is solved by reading the log file either specified by the user or by default. In addition, a user has an option to load from a previously parsed version of a pickle file to save time instead of reparsing the file. Moreover, a user has the ability to save data parsed from a file into a pickle object that can be used for quick loading instead of parsing the file again.

The data is parsed using a class called ChallengeInsight that we created to enhance readability and avoid passing large variables to functions to increase memory and time efficiency.

After that, a feature preparation unit process the data to provide all the common variables that is being shared by different features.

Finally, features functions are called according to user's choice, or by default all will be called. 

The code runs quick and memory efficient. In less than a minute, it was able to complete processing the provided log of more than four Milion records.

## List of Implemented Features 

### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

In addition, the code provides some flexability and additional advantages

1- ABility to determine the input and output path
2- Ability of quick reading from a previously parsed file saved in pickle
3- Fast and quick reading using regex
4- Fast and quick processing using classes and dictionaries while maintaining memory efficiency
5- Ability to run subset of features

## Getting Started

Clone or download the repository. Ensure that the log file exists in the right place or provide the log file path to the code as shown in the section how to run

## Prerequisites

Make Sure you have Python 3 installed and can be called using python command. If the python program needs to be called using python 3 then create an alias or modify the run.sh and run_tests.sh accordingly

## Dependencies

```
from datetime import datetime
import operator
import re
from collections import defaultdict
import numpy as np
from pathlib import Path
import sys
import pickle
import argparse
```

### How to Run

You can run the code by calling the code log_process inside the folder ...\src\. This will run the default code which will read a text file called 'log.txt' inside the folder ...\log_input\ and will run all the features. In addition, you can run the code by passing arguments to it which can define some parameters for the code different than the default.

Here are all the possible arguments for the code

```
-in or --input_file defines the input file path. For example, '...\insight_testsuite\tests\test_features\log_input\log.txt'. The default is '...\log_input\log.txt'
-out or --output_folder defines the input file path. For example, '...\insight_testsuite\tests\test_features\log_output'. The default is '...\log_output'
-f or --features defines which features would the user like to run. For example, -f 1 3 will run features 1 and 3 only. The default is to run all features. 
-s or --save_pickle gives the user the option to save the data parsed from the input file into pickle file to enable quick reading when needed. The defult is False. The pickle file will be stored in '...\data_stored\'
-r or -- read_pickle gives the user the option to read from a pickle file already saved intead of parsing the entire log file for quick reading. The defult is False. The pickle file is assumed to be stored in '...\data_stored\'
```
Here are some examples

```
python process_log.py .. everything is in default .. read from log in log_input and out in log_output while running all features. No pickle saving nor loading
python process_log.py -f [1 2 4] will run only features 1, 2 and 4
pyhon process_log.py -r will not parse the log file but read the variables host, time, request, reply code and bytes directly from a pickle file
```

## Running the tests

All tests exist in the run_tests.sh inside ...\insight_testsuite. Additional test cases can be added such as
1- handling empty files
2- handling corrupted files
3- Duplicated Entries
4- Non existing pickle file