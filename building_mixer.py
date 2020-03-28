import numpy as np

data01 = np.load("building01.npy")
shape = data01.shape;
n_lat = shape[0]
n_lon = shape[1]
n_t_tot = shape[2]
print np.max(data01)

data02 = np.load("building02.npy")
shape = data02.shape;
n_t_tot += shape[2]
print np.max(data02)
          
data03 = np.load("building03.npy")
shape = data03.shape;
n_t_tot += shape[2]
print np.max(data03)

data04 = np.load("building04.npy")
shape = data04.shape;
n_t_tot += shape[2]
print np.max(data04)

data05 = np.load("building05.npy")
shape = data05.shape;
n_t_tot += shape[2]
print np.max(data05)

data06 = np.load("building06.npy")
shape = data06.shape;
n_t_tot += shape[2]
print np.max(data06)

data = np.zeros((n_lat,n_lon,n_t_tot),dtype=int)

for i in range(n_lat):
    for j in range(n_lon):
        data[i,j] = np.append(data01[i,j],np.append(data02[i,j],np.append(data03[i,j],np.append(data04[i,j],np.append(data05[i,j],data06[i,j])))))

print np.max(data) 
np.save("building010203040506", data)
        
        
        