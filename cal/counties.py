#!/usr/bin/env python3

import urllib.request
import os
import datetime
import csv
import locale

def subtract():
	# subtract cal counties and save to a new file
	start_date = 50 # 3/1/20
	with open('../cssejhu/us_counties_cases.csv', newline='') as infile:
		reader = csv.reader(infile, delimiter=',')
		popfile = open('ca_counties_population.csv')
		popreader = csv.reader(popfile, delimiter=',')
		with open('ca_counties_cases.csv', 'w') as outfile:
			writer = csv.writer(outfile, delimiter=',')
			for row in reader:
				if row[0] == 'UID':
					pop=popreader.__next__()
					nrow = ['County', 'Latitude', 'Longitude', 'Population','Cumulative Cases','Cumulative Case Rate','14-day Case Rate', 'Daily New Cases (7-day avg)']
					for i in range(start_date, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)
				if row[6] == 'California' and row[0]!='84080006' and row[0]!='84090006':
					pop=popreader.__next__()
					p = "{:,}".format(int(pop[1]))
					ccase = "{:,}".format(int(row[-1]))
					ccaser = "{:,.2f}".format(int(row[-1])/int(pop[1])*100000)
					ccaser14 = "{:,.2f}".format((int(row[-1])-int(row[-15]))/int(pop[1])*100000)
					ncase = "{:,}".format(int((int(row[-1])-int(row[-8]))/7))  
					
					nrow = [row[5], row[8], row[9], p, ccase, ccaser, ccaser14, ncase]
					for i in range(start_date, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)

	with open('../cssejhu/us_counties_deaths.csv', newline='') as infile:
		reader = csv.reader(infile, delimiter=',')
		with open('ca_counties_deaths.csv', 'w') as outfile:
			writer = csv.writer(outfile, delimiter=',')
			for row in reader:
				if row[0] == 'UID':
					nrow = ['County', 'Latitude', 'Longitude', 'Population', 'Cumulative Deaths', 'Cumulative Death Rate', 'Daily New Deaths (7-day avg)']
					for i in range(start_date+1, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)
				if row[6] == 'California' and row[0]!='84080006' and row[0]!='84090006':
					drate = "{:,.2f}".format(int(row[-1])/int(row[11])*100000)
					nrow = [row[5], row[8], row[9], row[11], row[-1], drate, int((int(row[-1])-int(row[-8]))/7)]
					for i in range(start_date+1, len(row)):
						nrow.append(row[i])
					writer.writerow(nrow)

	# all done
	return
	
def newcases():
	"""
	Compute the new cases/deaths
	"""
	
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	
	# open cumulative cases file
	with open('ca_counties_cases.csv', newline='') as infile:
		# define a csv reader
		reader = csv.reader(infile, delimiter=',')
		# open the new cases file as output 
		with open('ca_counties_newcases.csv', 'w') as outfile:
			# define a csv writer
			writer = csv.writer(outfile, delimiter=',')
			# read it line by line
			for row in reader:
				# first line, as header
				if row[0] == 'County':
					nrow = row[0:3] + row[9:]
				else:
					nrow = row[0:3]
					for i in range(9, len(row)):
						nrow += [locale.atoi(row[i])-locale.atoi(row[i-1])]
				writer.writerow(nrow)
	
	with open('ca_counties_deaths.csv', newline='') as infile:
		# define a csv reader
		reader = csv.reader(infile, delimiter=',')
		# open the new cases file as output 
		with open('ca_counties_newdeaths.csv', 'w') as outfile:
			# define a csv writer
			writer = csv.writer(outfile, delimiter=',')
			# read it line by line
			for row in reader:
				# first line, as header
				if row[0] == 'County':
					nrow = row[0:3] + row[8:]
				else:
					nrow = row[0:3]
					for i in range(8, len(row)):
						nrow += [locale.atoi(row[i])-locale.atoi(row[i-1])]
				writer.writerow(nrow)		
			
		

if __name__ == '__main__':
	subtract()
	newcases()
