import numpy as np

unit_length = 0.001
time_length = 60*24
max_lat = 40.9
min_lat = 40.5
min_long = -74.25
max_long = -73.7
max_time = 31*24*60

n=3
#[latitude,longitude] index, not values
output = np.zeros((n,2),dtype=int)

output[0]=[0,2]
output[1]=[10,100]
output[2]=[20,50]

np.savetxt("output.txt", output)

#How to read array
output_read = np.loadtxt("output.txt")
print output_read[0]
print output_read[1]