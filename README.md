# Table of Contents
1. [Challenge Summary](README.md#Insight-Fansite)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Getting Started](README.md#getting-started)
4. [Description of Data](README.md#description-of-data)
5. [Writing clean, scalable, and well-tested code](README.md#writing-clean-scalable-and-well-tested-code)
6. [Repo directory structure](README.md#repo-directory-structure)
7. [Testing your directory structure and output format](README.md#testing-your-directory-structure-and-output-format)
8. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
9. [FAQ](README.md#faq)

# Insight Fansite

This project is to tackle the insight data challenge. The target is to read and process large log files from the site as quick as possible

## Details of Implementation

The code is implemented in Python 3 and is not guaranteed to be compatiable with Python 2. The problem is solved by reading the log file either specified by the user or by default. In addition, a user has an option to load from a previously parsed version of a pickle file to save time instead of reparsing the file. Moreover, a user has the ability to save data parsed from a file into a pickle object that can be used for quick loading instead of parsing the file again.

The data is parsed using a class called ChallengeInsight that we created to enhance readability and avoid passing large variables to functions to increase memory and time efficiency.

After that, a feature preparation unit process the data to provide all the common variables that is being shared by different features.

Finally, features functions are called according to user's choice, or by default all will be called. 

The code runs quick and memory efficient. In less than a minute, it was able to complete processing the provided log of more than four Milion records.

## Getting Started

Clone or download the repository. Ensure that the log file exists in the right place or provide the log file path to the code as shown in the section how to run

### Prerequisites
Make Sure you have Python 3 installed and can be called using python command. If the python program needs to be called using python 3 then create an alias or modify the run.sh and run_tests.sh accordingly

### Dependencies
'''
from datetime import datetime
import operator
import re
from collections import defaultdict
import numpy as np
from pathlib import Path
import sys
import pickle
import argparse
'''

### How to Run

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
