#!/usr/bin/env python3

import sys
import re
import pathlib
import csv
from datetime import date, datetime, timedelta
import os
from bs4 import BeautifulSoup

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
		if (input_date-last_date).days !=1 :
			print(f"date sequence unmatched, existing {row[-1]}, input {datetime.strftime(input_date, '%m/%d/%y')}")
			match = False
		else:
			match = True
	# all done
	return match

def check_last_date():
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

	# all done
	return last_date


def convert(infile):
	"""
	Read the daily case/deaths number from a text file and convert to spreadsheet
	"""
	# set a counter
	count = 0

	lb_pop = 483984
	pas_pop = 174449


	newfile = pathlib.Path(infile).with_suffix('.csv').name

	# open file and read line by line
	with open(infile) as fp, open(newfile, 'w', newline='') as out:

		# read long beach
		line = fp.readline()
		numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
		lb_case, lb_death = [int(i) for i in numbers]
		# read pasadena
		line = fp.readline()
		numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
		pas_case, pas_death = [int(i) for i in numbers]

		# read the rest
		while True:
			count += 1
			line = fp.readline()
			if not line:
				break

			numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
			if 'Under Investigation' in line :
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
		eof = False
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

def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list

def convert_html(input_file, output_file):

    with open(input_file, "r") as fin:
        soup = BeautifulSoup(fin, 'html.parser')
        contents = [item.get_text() for item in soup.find_all("td")]
        

    indices = get_index_positions(contents, "Laboratory Confirmed Cases ")
    print("test", indices)
    for index in indices:
        print('print ..', contents[index+1])

    indices = get_index_positions(contents, "-- Long Beach")

    longbeach = ['Long Beach']
    for index in indices:
        longbeach.append(contents[index+1])

    indices = get_index_positions(contents, "-- Pasadena")

    pasadena = ['Pasadena']
    for index in indices:
        pasadena.append(contents[index+1])


    ist = get_index_positions(contents, "City of Agoura Hills")[0]

    istart = ist
    stop = False
    end_string = "Under Investigation"

    with open(output_file, "w") as fp: 
        fp.write('\t'.join(longbeach)+'\n')
        fp.write('\t'.join(pasadena)+'\n')

        while not stop:
            # print(istart, contents[istart])
            if end_string in contents[istart] :
                fp.write('\t'.join(contents[istart:istart+4]))
                stop = True
            else:
                fp.write('\t'.join(contents[istart:istart+5])+'\n')
            istart +=5
    return


if __name__ == "__main__":

    current_date = check_last_date()
    iteration = True

    while iteration:
        current_date = current_date + timedelta(1)
        date_string = datetime.strftime(current_date, '%m-%d-%Y')
        print('processing date', date_string)

        input_file = "location/"+date_string+".html"
        if not(os.path.exists(input_file)):
            print(f"{input_file} does not exist")
            iteration = False
        else:
            print("adding new data ...")
            output_file = datetime.strftime(current_date, '%m-%d-%y')+".txt"
            convert_html(input_file, output_file)
            convert(output_file)
            merge(output_file, current_date)
            newcases()

