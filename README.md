# Coinbase-Trade-Data-Extractor
Python tool to poll api.pro.coinbase.com for up to date trade data.

SCRIPT TO RECORD TICKER DATA from api.pro.coinbase.com
Firstly, this script is meant to be run in Python 3. Once started, it will send a rest request to the api for given currency combination(s) every second. Since the api limits each IP to 3 requests/second, this script handles the scenario and places appropriate time gap between each request. So, if the number of combinations is greater than 3, it sends api request in a burst of 3 combination per second and then waits for a second and resume with rest of the combinations in the same pattern. A separate file for each currency combination, each day is created in the naming pattern ‘currency1-currency2-date.csv’.
	Ex: BTC-EUR-2018-09-06.csv
Additionally, a log file is created every day with logs of outgoing requests(optional) and errors occurred. It is named as ‘date_logs.txt’.
	Ex: 2018-09-06_logs.txt

DOWNLOADING AND INSTALLING PYTHON:
1.	Go to https://www.python.org/downloads/
2.	Download the latest version of python available:
 (./snapshots/python-download.png)
3.	A setup file will be downloaded, which when run will be an easy self-guided installation.
4.	Remember the directory in which python is installed, since it needs to be run with the complete path while executing a python script.
5.	From here on, python directory would refer to the python installation path:
‘E:\Installations\Python’ is the path I use and contains all the executables of python.
6.	This script uses a python library which sometimes isn’t included with the default setup. To ensure that the script runs fine, you need to run an installation command for ‘requests’ package. This needs to be run from ‘cmd’ in windows. Go to the python directory in cmd and run the below command:
python -m pip install requests
7.	If the library is already installed, it will give the below messages, otherwise, it will add the library in your python installation.
 



CONFIGURATIONS:
Delivered folder contains below files:
 
 ‘pairs.csv’ is the configuration file which needs to be populated before running the script. Please do not rename it or add any additional columns.
 
Column A(Pairs):
It needs to be populated with ‘/’ separated currency combinations, with exactly one combination in each cell, starting from A2.
Column B(timeperiod in days – Number only):
Only value of importance here should be in cell B2. This is the time period in days, for which the script will run. 
Column C(log interval – Number only):
Again, only one numerical value is expected in this column, in cell C2. This is the burst size of number of request which will be sent after which the data and the logs will be populated. 50 here means, data will be written in the files after every 50 requests. Data/Logs will also be written to files after any failure in request. Also, a separate file will be generated for data and logs after 12:00AM each day.
Column D(requestlog – 0 or 1):
If left on (1), every outgoing api request will be logged. When off (0), only output messages and error messages will be logged.




RUNNING THE SCRIPT:
1.	From cmd, go to the script directory (folder where the above provided files reside).
2.	Execute the below command to run the script in the foreground:

Path_to_python_directory\python.exe get-trade-data-new.py

 

For background, just replace python.exe with pythonw.exe
 

3.	For foreground, a message saying log ‘directory created successfully’ will appear on the screen and the script will start processing. If the log directory already exists, it will show the message ‘Problem creating log directory!’, which just shows that directory already exists and will continue execution.
4.	Everything else will now be logged in a file named date_logs.txt inside folder logs created in the main files’ directory.
5.	Output files will be created in ‘output’ folder in the same directory, in the pattern mentioned in the introductory note above.
6.	Do not run the script again, if the script is already running. Whether the script is already running or not can be insured by checking the update time for log file or output file. For 50 records as loginterval, file is updated approximately every 3-4 minutes apart. Time of update is proportional to loginterval, hence can be estimated accordingly, if you decide to change it from 50.

 

7.	You can also check if the script is running, using cmd. From anywhere in cmd, type the command tasklist, and a complete list of all the running tasks will appear. You can look for ‘python.exe’ or ‘pythonw.exe’ in the list, which will signify that the script is running. Please note, that if there are multiple python scripts running in the background, there will be one entry for each running script in the tasklist, and hence it would be impossible to tell them apart using this method.

 

   

8.	To terminate the script, use below command in cmd:

Taskkill /PID 18288 /F

 

The number after PID represents the process ID for your script and can be found from the tasklist above(highlighted).
