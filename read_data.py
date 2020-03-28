import csv;

with open('yellow_tripdata_2016-01.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in spamreader:
        i+=1
        if(i%10000==0):
            print i;
            print row;