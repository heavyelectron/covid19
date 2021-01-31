#!/usr/bin/env python3

import sys
import re
import pathlib
import csv
from datetime import date, datetime, timedelta
import os

url_root = '../cssejhu/us_states'


def append():

	# if start from scratch
	start_day = datetime.strptime('04-12-2020', '%m-%d-%Y')
	# if only append
	# start_day = datetime.today()-timedelta(4)

	day = start_day

	# iterate over dates
	while True:
		filename = datetime.strftime(day, '%m-%d-%Y') + '.csv'
		url = os.path.join(url_root, filename)
		if not(os.path.exists(url)):
			print(f"{filename} is not available")
			break

		with open(url, newline='') as newf, open('us_states_cases.csv') as casesf, open('us_states_deaths.csv') as deathsf, open('us_states_cases1.csv', 'w') as ncasesf, open('us_states_deaths1.csv', 'w') as ndeathsf:
			newdata = csv.reader(newf, delimiter=',')
			cases = csv.reader(casesf, delimiter=',')
			deaths = csv.reader(deathsf, delimiter=',')
			ncases = csv.writer(ncasesf, delimiter=',')
			ndeaths = csv.writer(ndeathsf, delimiter=',')

			# read header
			rnew = newdata.__next__()
			rcases = cases.__next__()
			rdeaths = deaths.__next__()

			# figure out the date, as the write position
			last_day = datetime.strptime(rcases[-1], '%m/%d/%y')
			diff = (day-last_day).days
			if diff == 1:
				# append mode
				rcases.append(datetime.strftime(day, '%m/%d/%y'))
				ncases.writerow(rcases)
				rdeaths.append(datetime.strftime(day, '%m/%d/%y'))
				ndeaths.writerow(rdeaths)
			elif diff <= 0:
				# replace mode
				ncases.writerow(rcases)
				ndeaths.writerow(rdeaths)
			else:
				# missing days
				print(f"missing days between {last_day.day} and {day.day}")
				break

			# iterate over states
			for rnew in newdata:
				if rnew[0] == 'Recovered':
					continue
				rcases = cases.__next__()
				rdeaths = deaths.__next__()
				#print(rnew)
				#print(rcases)
				ncaseval = rnew[5]
				ndeathval = rnew[6]
				if diff == 1:
					# append
					rcases.append(ncaseval)
					rdeaths.append(ndeathval)
				else:
					rcases[-1+diff] = ncaseval
					rdeaths[-1+diff] = ndeathval

				rcases[3] = rcases[-1]
				rcases[5] = int(rcases[-1])-int(rcases[-2])
				if rcases[6] != '':
					rcases[4] = int(int(rcases[3])/int(rcases[6].replace(',',''))*100000)
				ncases.writerow(rcases)


				rdeaths[3] = rdeaths[-1]
				rdeaths[5] = int(rdeaths[-1])-int(rdeaths[-2])
				if rcases[6] != '':
					rdeaths[4] = int(int(rdeaths[3])/int(rdeaths[6].replace(',',''))*100000)
				ndeaths.writerow(rdeaths)

		os.remove('us_states_cases.csv')
		os.rename('us_states_cases1.csv', 'us_states_cases.csv')
		os.remove('us_states_deaths.csv')
		os.rename('us_states_deaths1.csv', 'us_states_deaths.csv')

		day += timedelta(1)

	# all done
	return
	
	
def newcases():
	"""
	Compute the new cases/deaths
	"""
	import locale
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	
	# open cumulative cases file
	with open('us_states_cases.csv', newline='') as infile:
		# define a csv reader
		reader = csv.reader(infile, delimiter=',')
		# open the new cases file as output 
		with open('us_states_newcases.csv', 'w') as outfile:
			# define a csv writer
			writer = csv.writer(outfile, delimiter=',')
			# read it line by line
			for row in reader:
				# first line, as header
				if row[0] == 'State':
					nrow = row[0:3] + row[8:]
				else:
					nrow = row[0:3]
					for i in range(8, len(row)):
						dailynewcase = locale.atoi(row[i])-locale.atoi(row[i-1])
						# fix a Puerto Rico case error 11/9/20
						if dailynewcase < -1000:
							dailynewcase = 0
						nrow += [dailynewcase]
				writer.writerow(nrow)
	
	with open('us_states_deaths.csv', newline='') as infile:
		# define a csv reader
		reader = csv.reader(infile, delimiter=',')
		# open the new cases file as output 
		with open('us_states_newdeaths.csv', 'w') as outfile:
			# define a csv writer
			writer = csv.writer(outfile, delimiter=',')
			# read it line by line
			for row in reader:
				# first line, as header
				if row[0] == 'State':
					nrow = row[0:3] + row[8:]
				else:
					nrow = row[0:3]
					for i in range(8, len(row)):
						nrow += [locale.atoi(row[i])-locale.atoi(row[i-1])]
				writer.writerow(nrow)		

if __name__ == '__main__':
	append()
	newcases()
