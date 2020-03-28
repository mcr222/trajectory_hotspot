from __future__ import division
import numpy as np;
import matplotlib.pyplot as plt;
from matplotlib import colors;
from gtk.keysyms import marker
from calendar import month
from __builtin__ import str

def fill_data_example(data):
    data[0,0]=[50, 50, 50, 0];
    data[0,2]=[0, 0, 0, 50];

def computeFirstQuantile(time_values):
    n_t = len(time_values);
    first_quantile_idx = n_t//4-1;
    return np.sort(time_values)[first_quantile_idx];
    

def compute_initial_scores(data,scores):
    shape = data.shape;
    for i in range(shape[0]):
        for j in range(shape[1]):
            #no need to divide by area as all cells have same area
            scores[i,j] = computeFirstQuantile(data[i,j]);

def cellOrder(i,j,n):
    return i*n+j;

def cellCoord(k,n):
    return (k//n,k%n);

def displayDataAndScores(data,scores,n_lat,n_lon,n_t):
    f, axarr = plt.subplots(n_lat,n_lon, sharex='col', sharey='row')
    f.text(0.5, 0.04, 'Time interval', ha='center',fontsize=16)
    f.text(0.04, 0.5, 'Number of taxis', va='center', rotation='vertical',fontsize=16)
    for i in range(n_lat):
        for j in range(n_lon):
            axarr[i, j].plot(data[i,j],linestyle='None', marker='o',markersize=8)
            axarr[i, j].set_title("score: " + str(scores[i,j]))
    
    f.suptitle("Time evolution of number of taxis per cell", fontsize=20)
    plt.show()

 
def isInsideArea(i,j,area,n_lat,n_lon):
    return (i+2**area<=n_lat) and (j+2**area<=n_lon);
     

def getAreaDataAndScore(i,j,area,n_lat,n_lon):
    if(not isInsideArea(i, j, area, n_lat,n_lon)):
        return None,None; 
    if(dynamic_matrix[cellOrder(i, j, n_lon)][area] is not None):
        return dynamic_matrix[cellOrder(i, j, n_lon)][area];
     
    tl = getAreaDataAndScore(i, j, area-1, n_lat,n_lon)[1];
    tr = getAreaDataAndScore(i, j+2**(area-1), area-1, n_lat,n_lon)[1];
    bl = getAreaDataAndScore(i+2**(area-1), j, area-1, n_lat,n_lon)[1];
    br = getAreaDataAndScore(i+2**(area-1), j+2**(area-1), area-1, n_lat,n_lon)[1];
#     print i,j,area
#     print tl
#     print tr
#     print bl
#     print br
    area_time = tl+tr+bl+br;
#     print "area_time"
#     print area_time;
#      
    dynamic_matrix[cellOrder(i, j, n_lon)][area] = (computeFirstQuantile(area_time)/(2**area)**2,area_time);
    #this could be done slightly more efficiently by computing the 1st quantile when summing values
     
    return dynamic_matrix[cellOrder(i, j, n_lon)][area];  

def getAllAreaDataAndScore(i,j,area,n_lat,n_lon):
    if(not isInsideArea(i, j, area, n_lat,n_lon)):
        return None,None; 
    if(dynamic_matrix[cellOrder(i, j, n_lon)][area] is not None):
        return dynamic_matrix[cellOrder(i, j, n_lon)][area];
     
    tl = getAreaDataAndScore(i, j, area-1, n_lat,n_lon)[1];
    for k in range(area+1):
        tl += getAreaDataAndScore(i+area, j+k, 0, n_lat,n_lon)[1];
    
    for k in range(area):
        tl += getAreaDataAndScore(i+k, j+area, 0, n_lat,n_lon)[1];
        
#     print i,j,area
#     print tl
#     print tr
#     print bl
#     print br
#     print "area_time"
#     print area_time;
#      
    dynamic_matrix[cellOrder(i, j, n_lon)][area] = (computeFirstQuantile(tl)/((area+1)**2),tl);
    #this could be done slightly more efficiently by computing the 1st quantile when summing values
     
    return dynamic_matrix[cellOrder(i, j, n_lon)][area];  


def displayArea(i,j,area,score, n_lat,n_lon):
    disp = np.full((n_lat,n_lon),0,dtype=int);
    for k in range(2**area):
        for l in range(2**area):
            disp[i+k,j+l]=100; 
    
    plt.matshow(disp, cmap=colors.ListedColormap(['white', 'red']));
    plt.gca().set_xticks([x - 0.5 for x in plt.gca().get_xticks()][1:], minor='true')
    plt.gca().set_yticks([y - 0.5 for y in plt.gca().get_yticks()][1:], minor='true')
    plt.grid(which='minor',linewidth=2,color="white")
    plt.suptitle("Area score: "+ str(score))
    plt.show()    
    
def displayAllArea(i,j,area,score, n_lat,n_lon):
    disp = np.full((n_lat,n_lon),0,dtype=int);
    for k in range(area+1):
        for l in range(area+1):
            disp[i+k,j+l]=100; 
    
    plt.matshow(disp, cmap=colors.ListedColormap(['white', 'red']));
    plt.gca().set_xticks([x - 0.5 for x in plt.gca().get_xticks()][1:], minor='true')
    plt.gca().set_yticks([y - 0.5 for y in plt.gca().get_yticks()][1:], minor='true')
    plt.grid(which='minor',linewidth=2,color="white")
    plt.suptitle("Area score: "+ str(score))
    plt.show()    


def computeExponentialSquareAreas(data,scores, n_lat,n_lon,n_t):
    global dynamic_matrix
    results = [];
    
    # print "display data and scores"
    # displayDataAndScores(data, scores, n_lat,n_lon, n_t)
    
    area_sizes = int(np.log2(min(n_lat,n_lon)))+1;
    print "area sizes"
    print area_sizes
    
    '''
    First index of dynamic matrix is the index of the top-left cell of the area and the second the size
    of the area (2^l)
    '''
    dynamic_matrix = [[None for x in range(area_sizes)] for y in range(n_lat*n_lon)];
    #print len(dynamic_matrix)
    #print len(dynamic_matrix[0])
    
    print "filling initial values dynamic matrix"
    for i in range(n_lat):
            for j in range(n_lon):
                #print cellOrder(i, j, n_lon)
                dynamic_matrix[cellOrder(i, j, n_lon)][0]=(scores[i,j],data[i,j]);
    
    print "finished filling initial values dynamic matrix"
    
    print "filling whole dynamic matrix"
    for i in range(n_lat):
            for j in range(n_lon):
                for ar in range(area_sizes):
                    score,_ = getAreaDataAndScore(i,j,ar,n_lat,n_lon);
                    #score is None when attempted area does not fit in map (areas that go over the edge)
                    if (score is not None):
                        results.append([score,(i,j,ar)])
    
    print "finished filling whole dynamic matrix"
    
    print "ordering results"
    results.sort(reverse=True);
    print "finished ordering results"
    return results


def storeTopResultsExponential(results,show_res,filename):
    output = np.zeros((0,2),dtype=int)
    k=0
    tot_res=0
    res_max = len(results)
    print "resmax"
    print res_max
    while tot_res<50 and k<res_max:
        lat,lon,area = results[k][1];
        
        temp = np.zeros((0,2),dtype=int)
        repeated=False
        for i in range(2**area):
            for j in range(2**area):
                temp=np.concatenate((temp, [[lat+i,lon+j]]),axis=0)
                idx = np.where((output == (lat+i,lon+j)).all(axis=1));
                if(len(idx[0])!=0):
                    repeated=True;
        
        if(not repeated):
            output=np.concatenate((output, temp),axis=0)
            tot_res +=1
            print results[k][1];
            print results[k][0];
        
        k+=1
#         displayArea(*(results[k][1]),score =  results[k][0], n_lat=n_lat,n_lon=n_lon);
        
        #[latitude,longitude] index, not values
    
    np.savetxt(filename, output)
    

def computeAllSquareAreas(data,scores, n_lat,n_lon,n_t):
    global dynamic_matrix
    results = [];
    
    # print "display data and scores"
    # displayDataAndScores(data, scores, n_lat,n_lon, n_t)
    
    area_sizes = min(n_lat,n_lon);
    print "area sizes"
    print area_sizes
    
    '''
    First index of dynamic matrix is the index of the top-left cell of the area and the second the size
    of the area (2^l)
    '''
    dynamic_matrix = [[None for x in range(area_sizes)] for y in range(n_lat*n_lon)];
    #print len(dynamic_matrix)
    #print len(dynamic_matrix[0])
    
    print "filling initial values dynamic matrix"
    for i in range(n_lat):
            for j in range(n_lon):
                #print cellOrder(i, j, n_lon)
                dynamic_matrix[cellOrder(i, j, n_lon)][0]=(scores[i,j],data[i,j]);
    
    print "finished filling initial values dynamic matrix"
    
    print "filling whole dynamic matrix"
    for i in range(n_lat):
            for j in range(n_lon):
                for ar in range(area_sizes):
#                     print (i,j,ar)
                    score,unused = getAllAreaDataAndScore(i,j,ar,n_lat,n_lon);
#                     print score
#                     print unused
                    #score is None when attempted area does not fit in map (areas that go over the edge)
                    if (score is not None):
                        results.append([score,(i,j,ar)])
    
    print "finished filling whole dynamic matrix"
    
    print "ordering results"
    results.sort(reverse=True);
    print "finished ordering results"
    return results


def storeTopResultsAll(results,show_res,filename):
    output = np.zeros((0,2),dtype=int)
    k=0
    tot_res=0
    res_max = len(results)
    while tot_res<50 and k<res_max:
        lat,lon,area = results[k][1];
        
        temp = np.zeros((0,2),dtype=int)
        repeated=False
        for i in range(area+1):
            for j in range(area+1):
                temp=np.concatenate((temp, [[lat+i,lon+j]]),axis=0)
                idx = np.where((output == (lat+i,lon+j)).all(axis=1));
                if(len(idx[0])!=0):
                    repeated=True;

        if(not repeated):
            output=np.concatenate((output, temp),axis=0)
            tot_res +=1
            print results[k][1];
            print results[k][0];
        
        k+=1
#         displayAllArea(*(results[k][1]),score =  results[k][0], n_lat=n_lat,n_lon=n_lon);
        
        #[latitude,longitude] index, not values
    
    np.savetxt(filename, output)

    
# n_lon = 4;
# n_lat = 5;
# n_t = 4;
# data = np.zeros((n_lat,n_lon,n_t));
# fill_data_example(data);

#latitude,longitude,time
month= "010203040506"
data= np.load("building"+month+".npy")
shape = data.shape;
n_lat = shape[0]
n_lon = shape[1]
n_t = shape[2]


print "max data"
print np.max(data)
scores = np.zeros((n_lat,n_lon));
# displayDataAndScores(data, scores, n_lat, n_lon, n_t)

print "computing initial scores"
compute_initial_scores(data, scores)
print "finished computing initial scores"

print "max scores"
print np.max(scores);

# for i in range(n_lat):
#     for j in range(n_lon):
#         if(scores[i,j]>50):
#             print "score: "
#             print (i,j)
#             print scores[i,j]

# i_tot=[248,248,249,249]
# j_tot=[256,257,256,257]
# for k in range(len(i_tot)):
#     toplot=np.delete(data[i_tot[k],j_tot[k]],[31,61,62,63,95,126,127,159,190,191],axis=0)
#     plt.plot(toplot,linestyle='None', marker='o',markersize=8)
#     plt.ylabel('Number of taxis')
#     plt.xlabel('Time interval')
#     plt.title("Time evolution of number of taxis for cell (" +str(i_tot[k])+","+str(j_tot[k])+")")
#     plt.title("score: " + str(scores[i_tot[k],j_tot[k]]), loc='right')
# plt.show()

show_res=50
dynamic_matrix = None;
results = computeExponentialSquareAreas(data, scores, n_lat, n_lon, n_t)
storeTopResultsExponential(results, show_res, "outputexponential"+month+".txt")

 
dynamic_matrix = None;
results = computeAllSquareAreas(data, scores, n_lat, n_lon, n_t)
 
storeTopResultsAll(results,show_res, "outputall"+month+".txt")

