#!/usr/bin/env python

#Imports dependencies
import os
import glob
import calendar
from subprocess import Popen, PIPE

#Variables to set
stations = ['BILL','MA2','PET','TIXI','YAK','YSS']
yearStart = 2010
yearEnd   = 2014
locations = ['10']
#Channels[0] is for Q680, channels[1] is for Q330
channels  = [['SHE', 'SHN', 'SHZ'], ['BH1', 'BH2', 'BHZ']]

def processStations():
	#Begin processing all valid stationdays
	print 'Scan initiated'
	sydlc = makeSYDLClist()
	daysWithData = globOfDaysWithData()
	for stationday in daysWithData:
		#Check availability for each stationday and valid date
		#Gets the contents of inv_avail.txt for the stationday
		command = ['cat', stationday + '/inv_avail.txt']
		avail = Popen(command, stdout=PIPE).communicate()[0].strip().split('\n')
		#Initiates list to append the availability of each channel to find an average
		totalAvailability = []
		for line in avail:
			#Steps through each line in inv_avail.txt, getting loc, chan, and availability pct
			loc, chan, pct = line.split()
			totalAvailability.append(float(pct))
			if loc in locations:
				#If the loc in the line is a valid location (as set by the "locations"), proceed
				if chan in channels[0] or chan in channels[1]:
					#If the chan in the line is a valid channel (as set by "channels"), proceed
					totalAvail = getListAverage(totalAvailability)
					if (totalAvail - 5.0) <= float(pct):
						#If avail% for the desired channels is > or within 5 points of the avg, proceed
						station = stationday.split('_')[-1]
						year    = stationday.split('/')[-1].split('_')[0]
						day     = stationday.split('/')[-1].split('_')[1]
						try:
							#Remove stationday locchan entry from sydlc if there is little probability that
							#Obninsk has more data than exists on /xs0/
							sydlc.remove([station, year, day, loc, chan])
						except:
							#Print the following to the console if stationday loccahn is not within sydlc
							print 'Problem with', stationday, line, [station, year, day, loc, chan] in daysWithData
	#Initate the output file and write the header
	fob = open('RussianDataRecovery.csv','w')
	fob.write('station,year,day,loc,chan\n')
	fob.close()
	#Open the file and append each stationday locchan entry
	fob = open('RussianDataRecovery.csv','a')
	for item in sydlc:
		fob.write(','.join(item) + '\n')
	fob.close()
	print 'Scan complete'

def makeSYDLClist():
	#Given the available stations, time frame, and desired locations and channels
	#make a list of all possible permutations to check for and return said list (SYDLC)
	sydlc = []
	for station in stations:
		#Stepping through each station in the list
		for year in range(yearStart, yearEnd + 1):
			#Stepping through each year, set length of year in days
			daysInYear = 365
			if calendar.isleap(year):
				#Checks if the year in question is a leap year
				daysInYear += 1
			for day in range(1, daysInYear + 1):
				#Steps through each day
				for location in locations:
					#Steps through each location and checks if it has been upgraded to a Q330
					channels = ifQ680era(station, year, day)
					for channel in channels:
						#Steps through the channels
						#Appends each station, year, day, location, and channel to a list
						sydlc.append([station, str(year), str(day).zfill(3), location, channel])
	return sydlc

def ifQ680era(station, year, day):
	#Checks to see if the stationday has a Q680 or Q330
	#and returns appropriate list of channels
	day = str(day).zfill(3)
	if   station == 'MA2':
		q330date = 2010201
	elif station == 'PET':
		q330date = 2014207
	elif station == 'YAK':
		q330date = 2012254
	elif station == 'YSS':
		q330date = 2013295
	else:
		q330date = 9999999
	if int(str(year) + str(day)) < q330date:
		return channels[0]
	else:
		return channels[1]

def globOfDaysWithData():
	#Checks to see for which stationdays data exists on /xs0/ so that we can
	#later step through and check availability percentages
	daysWithData = []
	for station in stations:
		#Steps through each station
		for year in range(yearStart, yearEnd + 1):
			#Steps through each year and globs the existing days
			path = '/xs0/seed/IU_' + station + '/' + str(year) + '/*'
			stationdays = glob.glob(path)
			for stationday in stationdays:
				#Steps through each stationday and checks to see that the standard naming convention
				#has been applied. If the stationday's folder name is nonstandard, it is disregarded
				if len(stationday) < 40:
					#Appends the paths to the stationdays that stick to the standard naming convention
					daysWithData.append(stationday)
	return daysWithData
	
def getListAverage(lst):
	#Takes a list of floats and averages them
	sumTotal = 0.0
	for index in range(len(lst)):
		sumTotal += lst[index]
	return sumTotal / len(lst)

#Initiates the script
processStations()