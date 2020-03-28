from __future__ import division
import numpy as np
import pandas as pd
import time
import datetime
import math
import csv
from openpyxl.formula.tests.test_tokenizer import ROW

month="01"
unit_length = 0.001
time_length = 60*60*24
max_lat = 40.9 +unit_length
min_lat = 40.5 +unit_length
min_long = -74.25 +unit_length
max_long = -73.7 +unit_length
max_time = 31*24*60*60
min_time = '2016-'+month+'-01 00:00:00'
date_format = '%Y-%m-%d %H:%M:%S'
neo_time = datetime.datetime.strptime(min_time, date_format)

## create 3-dimensional building
time_size = int(max_time/time_length)
print "time slots"
print time_size
long_size = int((max_long-min_long)/unit_length)+1
lat_size = int((max_lat-min_lat)/unit_length)+1
#building = [[[0 for k in xrange(time_size)] for j in xrange(long_size)] for i in xrange(lat_size)]
building = np.zeros((lat_size,long_size,time_size),dtype=int)

##
file_path = 'yellow_tripdata_2016-'+month+'.csv'
with open(file_path, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    i=0
    first=True
    for row in spamreader:
        if (not first and (max_long>float(row[5])>min_long)  and (min_lat<float(row[6])<max_lat) and
                (min_lat < float(row[10]) < max_lat) and (max_long>float(row[9])>min_long)):
            #pick_up
            x_axis = int((float(row[6])-min_lat)/unit_length) #latitude
            y_axis = int((float(row[5])-min_long)/unit_length) #longtitude 
            temp = datetime.datetime.strptime(row[1], date_format)
            seconds = (temp - neo_time).total_seconds()
            z_axis= int(seconds/(time_length))
            try:
                building[x_axis,y_axis,z_axis] +=1
            except:
                print row
                print (x_axis,y_axis,z_axis)

            #drop_off
            x_axis = int((float(row[10]) - min_lat) / unit_length)  # latitude
            y_axis = int((float(row[9]) - min_long) / unit_length)  # longtitude
            temp = datetime.datetime.strptime(row[2], date_format)
            seconds = (temp - neo_time).total_seconds()
            z_axis = int(seconds / (time_length))
            try:
                building[x_axis,y_axis,z_axis] +=1
            except:
                print row
                print (x_axis,y_axis,z_axis)

            i+=1
            if i%50000==0:
                print i
        else:
            first=False
'''
cell = [0 for k in xrange((time_size)*(long_size)*(lat_size))]
for i in range(lat_size):
    for j in range(long_size):
        for k in range(time_size):
            cell[i*lat_size*long_size+j*long_size+k] = building[i][j][k]
'''
#latitude,longitude,time
print 'final'
print building[268, 287,28]
np.save("building"+month, building)

# loaded_building= np.load("building.npy")
# print 'loaded final'
# print loaded_building[268, 287,28]




