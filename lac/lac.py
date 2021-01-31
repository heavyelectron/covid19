#!/usr/bin/env python3

import sys
import re
import pathlib
import csv
from datetime import date, datetime, timedelta
import os

def check_date_seq(input_date):
	"""
	Check whether the input date is right behind the last date of existing file
	:param input_date: input date in datetime
	:return: True or False
	"""
	# open existing case file
	with open("lac_cities_cases.csv") as fp:
		# create a csv reader
		reader = csv.reader(fp, delimiter=',')
		# read the first row
		row = reader.__next__()
		# check the last date
		last_date = datetime.strptime(row[-1], '%m/%d/%y')
		print(last_date)
		print(input_date)
		if (input_date-last_date).days !=1 :
			print(f"date sequence unmatched, existing {row[-1]}, input {datetime.strftime(input_date, '%m/%d/%y')}")
			match = False
		else:
			match = True
	# all done
	return match

def convert(infile, lpfile):
	# set a counter
	count = 0
	
	lpf = open(lpfile)

	lp = re.findall(r"[-+]?\d*\.\d+|\d+", lpf.readline())	
	lpf.close()
	lb_case, pas_case, lb_death, pas_death = [int(i) for i in lp]

	lb_pop = 483984
	pas_pop = 174449


	newfile = pathlib.Path(infile).with_suffix('.csv').name

	# open file and read line by line
	with open(infile) as fp, open(newfile, 'w', newline='') as out: 
		
		while True: 
			count += 1
			line = fp.readline() 

			if not line: 
				break

			numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
			if '- Under Investigation' in line :
				continue
			elif len(numbers)==4:
				if not ( 'Unincorporated' in line and int(numbers[0])==0):
					if 'City of Lynwood' in line:
						out.write(f"City of Long Beach\t{lb_case}\t{int(lb_case/lb_pop*100000)}\t{lb_death}\t{int(lb_death/lb_pop*100000)}\n")
					if 'City of Pico Rivera' in line:
						out.write(f"City of Pasadena\t{pas_case}\t{int(pas_case/pas_pop*100000)}\t{pas_death}\t{int(pas_death/pas_pop*100000)}\n")				
					out.write("{}\n".format(line.strip()))
				elif ("Unincorporated - Roosevelt" in line):
					out.write("{}\n".format(line.strip()))	
				elif ("Unincorporated - San Francisquito Canyon/Bouquet Canyon" in line):
					out.write("{}\n".format(line.strip()))	
				elif ("Unincorporated - Harbor Gateway"in line):
					out.write("{}\n".format(line.strip()))	
			else:
				
				if not ('Unincorporated' in line):
					out.write("{}\n".format(line.strip())) 

	# all done
	return

def merge(infile, input_date):

	newfile = pathlib.Path(infile).with_suffix('.csv').name

	with open(newfile, newline='') as newf, open('lac_cities_cases.csv') as casesf, open('lac_cities_deaths.csv') as deathsf, open('lac_cities_cases1.csv', 'w') as ncasesf, open('lac_cities_deaths1.csv', 'w') as ndeathsf:
		new = csv.reader(newf, delimiter='\t')
		cases = csv.reader(casesf, delimiter=',')
		deaths = csv.reader(deathsf, delimiter=',')
		ncases = csv.writer(ncasesf, delimiter=',')
		ndeaths = csv.writer(ndeathsf, delimiter=',')
		
		# first line headers
		rcase = cases.__next__()
		rdeath = deaths.__next__()

		adate = input_date.strftime("%-m/%-d/%y")
		print("adding data for ", adate)
		rcase.append(adate)
		rdeath.append(adate)
		ncases.writerow(rcase)
		ndeaths.writerow(rdeath)
		
		len_cases = len(rcase)
		len_deaths = len(rdeath)
		
		skip = False
		for new_row in new:
			if not skip:
				rcase = cases.__next__()
				rdeath = deaths.__next__()
			city = new_row[0].replace("*", "")
			if city == "Los Angeles":
				city = "City of Los Angeles (inc. all communities)"
			#print(city, rcase[0], rdeath[0])
			if city ==  rcase[0] and city == rdeath[0]:
				skip = False
				
				rcase.append(new_row[1])
				rcase[3] = new_row[1]
				rcase[4] = new_row[2]
				rcase[5] = new_row[3]
				rcase[6] = new_row[4]
				#print(city, len(rcase), rcase[-1], rcase[-2], rcase[-8], rcase[-31])
				rcase[7] = int(rcase[-1])-int(rcase[-2]) if rcase[-2] !='' else rcase[-1]
				rcase[8] = int(rcase[-1])-int(rcase[-8]) if rcase[-8] !='' else rcase[-1]
				if rcase[-31] != '':
					rcase[9] = (int(rcase[-1])-int(rcase[-15]))*100000//int(rcase[10]) 
				else:
					rcase[9] = int(rcase[-1])*100000//int(rcase[10]) 
				ncases.writerow(rcase)
				
				rdeath.append(new_row[3])
				ndeaths.writerow(rdeath)
				
			else:
				skip = True
				print(city, " is new, please add its lat/lon")
				nrcase = [None]*len_cases
				nrcase[0] = new_row[0]
				nrcase[3] = new_row[1]
				nrcase[4] = new_row[2]
				nrcase[5] = new_row[3]
				nrcase[6] = new_row[4]
				nrcase[10] = int(int(nrcase[3])/int(nrcase[4])*100000)
				nrcase[-1] = nrcase[3]
				nrcase[7] = int(nrcase[-1])
				nrcase[8] = int(nrcase[-1])
				nrcase[9] = int(nrcase[-1])*100000//int(nrcase[10])
				ncases.writerow(nrcase)
				
				nrdeath = [None]*len_deaths
				nrdeath[0] = new_row[0]
				nrdeath[-1] = new_row[3]
				ndeaths.writerow(nrdeath)
	
	os.remove('lac_cities_cases.csv')
	os.rename('lac_cities_cases1.csv', 'lac_cities_cases.csv')
	os.remove('lac_cities_deaths.csv')
	os.rename('lac_cities_deaths1.csv', 'lac_cities_deaths.csv')

	# all done
	return

def newcases():
	casefile = 'lac_cities_cases.csv'
	ncasefile = 'lac_cities_newcases.csv'

	with open(ncasefile, 'w') as ncasesf, open(casefile, newline='') as casesf:
		cases = csv.reader(casesf, delimiter=',')
		ncases = csv.writer(ncasesf, delimiter=',')

		rcase = cases.__next__()
		len_cases = len(rcase)
		len_ncases = len_cases - 9

		rncase = [None] * len_ncases

		rncase[0] = rcase[0]
		rncase[1] = rcase[1]
		rncase[2] = rcase[2]
		for i in range(3, len_ncases):
			rncase[i] = rcase[i + 9]
		ncases.writerow(rncase)
		#print(rncase)

		for rcase in cases:
			rncase[0] = rcase[0]
			rncase[1] = rcase[1]
			rncase[2] = rcase[2]
			for i in range(3, len_ncases):

				ocase = rcase[i + 8]
				ncase = rcase[i + 9]
				if ocase == '' or ocase == ' ':
					ocase = 0
				ocase = int(ocase)

				if ncase == '' or ncase == ' ':
					ncase = 0
				try:
					ncase = int(ncase)
				except ValueError:
					print("input value error ", ncase)
				rncase[i] = ncase - ocase
			ncases.writerow(rncase)
			#print(rncase)
	# all done
	return

if __name__ == "__main__":
	
	if len(sys.argv) == 2 :
		# with an input %m-%d-%y.txt file
		input_date_file = sys.argv[1]
		input_date = datetime.strptime(os.path.splitext(input_date_file)[0], '%m-%d-%y')
	else:
		# without an input file, assuming today
		input_date = datetime.today()
		input_date_file = datetime.strftime(input_date, '%m-%d-%y') + '.txt'

	if not(os.path.exists(input_date_file)):
		print(f"{input_date_file} does not exist")
		sys.exit(1)

	lb_pas_file = 'lb_pas.txt'

	# check whether the date matches
	if check_date_seq(input_date):
		print("matches, adding new data ...")
		convert(input_date_file, lb_pas_file)
		merge(input_date_file, input_date)
		newcases()
	else:
		print("not matched")
