#!/usr/bin/env python3

import urllib.request
import os
import datetime
import csv

def subtract():
	# subtract cal counties and save to a new file
	start_date = 50 # 3/1/20
	with open('../cssejhu/us_counties_cases.csv', newline='') as infile:
		reader = csv.reader(infile, delimiter=',')
		with open('ca_counties_cases.csv', 'w') as outfile:
			writer = csv.writer(outfile, delimiter=',')
			for row in reader:
				if row[0] == 'UID':
					nrow = ['County', 'Latitude', 'Longitude', 'Cumulative Cases', 'Daily New Cases']
					for i in range(start_date, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)
				if row[6] == 'California' and row[0]!='84080006' and row[0]!='84090006':
					nrow = [row[5], row[8], row[9], row[-1], int(row[-1])-int(row[-2])]
					for i in range(start_date, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)

	with open('../cssejhu/us_counties_deaths.csv', newline='') as infile:
		reader = csv.reader(infile, delimiter=',')
		with open('ca_counties_deaths.csv', 'w') as outfile:
			writer = csv.writer(outfile, delimiter=',')
			for row in reader:
				if row[0] == 'UID':
					nrow = ['County', 'Latitude', 'Longitude', 'Population', 'Cumulative Deaths', 'Daily New Deaths']
					for i in range(start_date+1, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)
				if row[6] == 'California' and row[0]!='84080006' and row[0]!='84090006':
					nrow = [row[5], row[8], row[9], row[11], row[-1], int(row[-1])-int(row[-2])]
					for i in range(start_date+1, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)

	# all done
	return

if __name__ == '__main__':
	subtract()