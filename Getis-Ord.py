
import numpy as np
import math


unit_length = 0.001
time_length = 60*60*24
max_lat = 40.9 +unit_length
min_lat = 40.5 +unit_length
min_long = -74.25 +unit_length
max_long = -73.7 +unit_length
max_time = 31*24*60*60
min_time = '2016-01-01 00:00:00'
date_format = '%Y-%m-%d %H:%M:%S'


time_size = abs(int(max_time/time_length))
long_size = abs(int((max_long-min_long)/unit_length))
lat_size = abs(int((max_lat-min_lat)/unit_length))


loaded_building= np.load("building010203040506.npy")

def cal_sum(build, i,j,k):
    sum_out = 0
    '''
    if((i==0) and (0<j<long_size-1) and (0<k<time_size-1)):
        for a in [i,i+1]:
            for b in [j-1,j,j+1]:
                for c in [k-1,k,k+1]:
                    sum_out = sum_out+build[a,b,c]
    if((i==lat_size-1) and (0<j<long_size-1) and (0<k<time_size-1)):
        for a in [i-1,i]:
            for b in [j-1,j,j+1]:
                for c in [k-1,k,k+1]:
                    sum_out = sum_out+build[a,b,c]
    if((j==0) and (0<i<lat_size-1) and (0<k<time_size-1)):
        for a in [i-1,i,i+1]:
            for b in [j,j+1]:
                for c in [k-1,k,k+1]:
                    sum_out = sum_out+build[a,b,c]
    if ((j==long_size-1) and (0<i<lat_size-1) and (0<k<time_size-1)):
        for a in [i-1,i,i+1]:
            for b in [j-1,j]:
                for c in [k-1,k,k+1]:
                    sum_out = sum_out + build[a,b,c]
    if ((k==0) and (0<i<lat_size-1) and (0<j<long_size-1)):
        for a in [i-1,i,i+1]:
            for b in [j-1,j]:
                for c in [k,k+1]:
                    sum_out = sum_out + build[a,b,c]
    if ((k==time_size-1) and (0<i<lat_size-1) and (0<j<long_size-1)):
        for a in [i-1,i,i+1]:
            for b in [j-1,j]:
                for c in [k-1,k]:
                    sum_out = sum_out + build[a,b,c]
    '''
    if((0<i<lat_size-1) and (0<j<long_size-1) and (0<k<time_size-1)):
        for a in [i-1,i,i+1]:
            for b in [j-1,j,j+1]:
                for c in [k-1,k,k+1]:
                    sum_out = sum_out + build[a,b,c]
    else:
        sum_out = 0
    return sum_out

# the cells in the side of the building can be ignored
#building_sum = [[[0 for k in xrange(time_size)] for j in xrange(long_size)] for i in xrange(lat_size)]
building_sum = np.zeros((lat_size,long_size,time_size),dtype=int)
for i in range(lat_size):
    for j in range(long_size):
        for k in range(time_size):
            if ((k*lat_size*long_size+j*lat_size+i)%10000==0):
                print(i,j,k)
            building_sum[i,j,k] = cal_sum(loaded_building,i,j,k)




# calculate the statistic
# first we need to transform it into 1d array

cell = np.zeros((time_size*lat_size*long_size),dtype=int)
cell_sum = np.zeros((time_size*lat_size*long_size),dtype=int)
for i in range(time_size):
    for j in range(long_size):
        for k in range(lat_size):
            cell_sum[i*lat_size*long_size+j*lat_size+k] = building_sum[k,j,i]
            cell[i*lat_size*long_size+j*lat_size+k] = loaded_building[k,j,i]



#calculate s
#print np.sum(np.square(cell))
#print len(cell)
cell_mean = np.mean(cell)
#print cell_mean**2
#print(np.sum(np.square(cell))/len(cell)-cell_mean**2)
s = math.sqrt(float(np.sum(np.square(cell)))/float(len(cell))-cell_mean**2)
#calculate the statistic
G = []
for i in range(len(cell)):
    if i%10000==0:
        print(i)
    g = (cell_sum[i]-27*cell_mean)/(s*math.sqrt((27*len(cell)-27**2)/(len(cell)-1)))
    G.append(g)


G = np.asarray(G)
after_index = G.argsort()[-5000:][::-1]
print(after_index)
before_index = np.zeros((50,2),dtype=int)
j=0
total=0
while total<50 and j<5000:
    z_axis = int(after_index[j]/(lat_size*long_size))
    y_axis = int((after_index[j]%(lat_size*long_size))/lat_size)
    x_axis = after_index[j]-z_axis*lat_size*long_size-y_axis*lat_size
    idx = np.where((before_index == ([x_axis,y_axis])).all(axis=1));
    if len(idx[0]) == 0:
        before_index[total]=[x_axis,y_axis]
        total+=1
    j+=1

# save to output_getis
before_index = np.asarray(before_index)
print(before_index[0],before_index[1])
output = np.zeros((50,2),dtype=int)
for i in range(len(before_index)):
    output[i] = before_index[i]

np.savetxt("output_getis010203040506.txt", output)