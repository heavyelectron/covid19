#!/usr/bin/env python3

import urllib.request
from datetime import datetime, timedelta
import os.path
import csv

def download_global():
    """
    Download the global data, including US
    """

    # urls for raw csv files
    case_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    death_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

    # download the files
    urllib.request.urlretrieve(case_url, 'global_cases.csv')
    urllib.request.urlretrieve(death_url, 'global_deaths.csv')

    return

def download_states():
    """
    Download US states data
    """
    # csse data available from 4/12/2020
    #

    # url root for US states data
    url_root = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'

    # if download from the first available date
    # day = datetime.strptime('04-12-2020', '%m-%d-%Y')
    # if earlier days are already downloaded, just download the most recent 5 days
    day = datetime.today() - timedelta(4)

    found = True
    # loop till date unavailable
    while found:
        # get the filename
        filename = datetime.strftime(day, '%m-%d-%Y') + '.csv'
        # get the url
        url = url_root + filename
        try: #download
            urllib.request.urlretrieve(url, os.path.join('us_states', filename))
            found = True
        except:
            print(f"{filename} is not available yet")
            found = False
        day += timedelta(1)

    # all done
    return

def download_counties():
    """
    Download US Counties data
    """
    # urls for US counties data
    case_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    death_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'

    # download the files
    urllib.request.urlretrieve(case_url, 'us_counties_cases.csv')
    urllib.request.urlretrieve(death_url, 'us_counties_deaths.csv')

def print_us():
    """
    Print out the US case and death counts for the most recent 5 days
    """
    # the date range
    days = 14

    print("US summary:")
    # open the global file
    with open('global_cases.csv', newline='') as csvfile:
        # use a csv reader
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        # iterate over all lines(countries)
        for row in reader:
            # first line: header
            if row[1] == "Country/Region":
                length = len(row)
                dates = row[length-days:length]
            # find US
            elif row[1] == 'US':
                length = len(row)
                cases =  row[length - days:length]
    with open('global_deaths.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[1] == 'US':
                length = len(row)
                deaths = row[length-days:length]
    
    for i in range(days):
        print(dates[i], f'{int(cases[i]):,}', f'{int(deaths[i]):,}') 
   
    return

def print_cal():
    """
    Print out the California case and death counts for the most recent 5 days
    """

    # set today
    today = datetime.today()

    print("California summary: cases, deaths")
    # count down for 5 days
    for i in range(14):
        day = today - timedelta(i)
        # date string, e.g., 07-22-2020
        datestring = datetime.strftime(day, '%m-%d-%Y')
        # get the full path
        filename = os.path.join('us_states', datestring + '.csv')
        if os.path.exists(filename): # check existence
            # file exists, open it
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                # iterate over all lines (states)
                for row in reader:
                    # find California
                    if row[0] == 'California':
                        print(datestring, [f'{int(row[i]):,}' for i in [5, 6]])

    return

if __name__ == '__main__':
    download_global()
    download_states()
    download_counties()
    print_us()
    print_cal()
