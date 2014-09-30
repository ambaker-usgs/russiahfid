#!/usr/bin/env python

import os
import glob
import calendar
from subprocess import Popen, PIPE

stations = ['BILL','MA2','PET','TIXI','YAK','YSS']
yearStart = 2010
yearEnd   = 2014
locations = ['10']
channels  = [['SHE', 'SHN', 'SHZ'], ['BH1', 'BH2', 'BHZ']]

def processStations():
	sydlc = makeSYDLClist()
	daysWithData = globOfDaysWithData()
	for stationday in daysWithData:
		command = ['cat', stationday + '/inv_avail.txt']
		avail = Popen(command, stdout=PIPE).communicate()[0].strip().split('\n')
		totalAvailability = []
		for line in avail:
			loc, chan, pct = line.split()
			totalAvailability.append(float(pct))
			if loc in locations:
				if chan in channels[0] or chan in channels[1]:
					totalAvail = getListAverage(totalAvailability)
					if (totalAvail - 5.0) <= float(pct):
						station = stationday.split('_')[-1]
						year    = stationday.split('/')[-1].split('_')[0]
						day     = stationday.split('/')[-1].split('_')[1]
						# print station, year, day, loc, chan, pct
						try:
							sydlc.remove([station, year, day, loc, chan])
						except:
							print 'Problem with', stationday, line, [station, year, day, loc, chan] in daysWithData
	fob = open('RussianDataRecovery.csv','w')
	fob.write('station,year,day,loc,chan\n')
	fob.close()
	fob = open('RussianDataRecovery.csv','a')
	for item in sydlc:
		fob.write(','.join(item) + '\n')
	fob.close()
	print 'DONE'

def makeSYDLClist():
	sydlc = []
	for station in stations:
		# if station == 'BILL':
		for year in range(yearStart, yearEnd + 1):
				# if year == 2010:
			daysInYear = 365
			if calendar.isleap(year):
				daysInYear += 1
			for day in range(1, daysInYear + 1):
				for location in locations:
					channels = ifQ680era(station, year, day)
					for channel in channels:
						sydlc.append([station, str(year), str(day).zfill(3), location, channel])
	return sydlc

def ifQ680era(station, year, day):
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
	daysWithData = []
	for station in stations:
		for year in range(yearStart, yearEnd + 1):
			path = '/xs0/seed/IU_' + station + '/' + str(year) + '/*'
			stationdays = glob.glob(path)
			for stationday in stationdays:
				if len(stationday) < 40:
					daysWithData.append(stationday)
	return daysWithData
	
def getListAverage(lst):
	sumTotal = 0.0
	for index in range(len(lst)):
		sumTotal += lst[index]
	return sumTotal / len(lst)

processStations()
