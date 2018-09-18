import requests
import csv
import datetime
import time
from threading import Thread
import os
import math

def write_log(path, messages, timestamp):
	name = os.path.join(path, str(timestamp).split(' ')[0] + '_logs.txt')
	with open(name, 'a') as logfile:
		for m in messages:
			logfile.write(m)
			logfile.write('\n')


def write_into_csv(path, data):
	#write the output in the csv file

	with open(path, 'a', newline = '') as f:
		for row in data:
			writer = csv.DictWriter(f, row.keys())
			if f.tell() == 0:
				writer.writeheader()
				writer.writerow(row)
			else:
				writer.writerow(row)


def write_all_data(data , outpaths, timestamp):
	for list, path in zip(data, outpaths):
		name = path + '-' + str(timestamp).split(' ')[0] + '.csv'
		write_into_csv(name, list)


def log_message(message):
	return str(datetime.datetime.now()) + ' : ' + message

def main():

	outputpath = os.path.join('output')
	logpath = os.path.join('logs')

	data = []
	logs = []

#creating the log directory
	try:
		os.mkdir(logpath)
	except OSError:
		print("Problem creating log directory !")
	else:
		print("Log directory created successfully !")

#creating the output directory
	try:
		os.mkdir(outputpath)
	except OSError:
		logs.append(log_message("Problem creating output directory !"))
	else:
		logs.append(log_message("Output directory created successfully !"))


#reading pairs.csv for input data
	configs = []
	with open('pairs.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		for row in csv_reader:
			configs.append(row)

	maxrequests = 3
	index = 0
	timeperiod = 0
	loginterval = 0
	urls = []
	pairs = []
	outpaths = []
	switch = 1

#iterating over input data to separate currency pairs and timeperiod
	logs.append(log_message("Working with below currency combination"))
	for config in configs:

		if index == 0:
			index = index + 1
			continue

		#read time period from second column of second row
		if index == 1:
			timeperiod = int(config[1])
			loginterval = int(config[2])
			switch = int(config[3])
			# print(type(timeperiod))
			index = index + 1

		#read currency pairs from first column and create the URL for REST request
		if len(config[0]) > 0:
			split_pair = config[0].split("/")
			pair = split_pair[0] + "-" + split_pair[1]
			logs.append(log_message(pair))
			pairs.append(pair)
			urls.append("https://api.pro.coinbase.com/products/" + pair + "/ticker")
			outpaths.append(os.path.join(outputpath, pair))

	length = len(pairs)
	starttime = datetime.datetime.now()
	lasttime = starttime
	days = 0

	#loop to create REST request until timeperiod is reached
	while days < timeperiod:
		factor = 0
		i = 0

		while i < length:
			# print(i)
			if factor < maxrequests:
				if switch == 1:
					logs.append(log_message('sending request to ' + urls[i]))

				try:
					r = requests.get(url = urls[i])
					if r.status_code == 200:
						current_data = r.json()
						timesplit = current_data["time"].split(".")
						datatime = timesplit[0]
						yourdate = datetime.datetime.strptime(datatime + 'Z', '%Y-%m-%dT%H:%M:%SZ')
						current_data["time"] = yourdate
						if len(data) > i:
							 data[i].append(current_data)
						else:
							temp = []
							temp.append(current_data)
							data.append(temp)
					else:
						logs.append(log_message(r.reason))
						write_log(logpath, logs, lasttime)
						del logs[:]
				except (ConnectionError, TimeoutError):
					logs.append(log_message('Request not fulfilled. Trying again !!'))
					write_log(logpath, logs, lasttime)
					del logs[:]

				i += 1
				factor += 1
			else:
				time.sleep(1)
				factor  = 0

		currenttime = datetime.datetime.now()
		days = currenttime.day - starttime.day

		if len(data[i - 1]) == loginterval:
			logs.append(log_message(str(loginterval) + ' records. Writing data into CSV'))
			write_all_data(data, outpaths, lasttime)
			write_log(logpath, logs, lasttime)
			del data[:]
			del logs[:]

		if currenttime.day - lasttime.day > 0:
			logs.append(log_message('DAY END. Writing data into CSV'))
			write_all_data(data, outpaths, lasttime)
			write_log(logpath, logs, lasttime)
			lasttime = currenttime
			del data[:]
			del logs[:]

		time.sleep(1)


main()
