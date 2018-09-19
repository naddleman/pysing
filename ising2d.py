"""
2d Ising Ferromagnet (on torus)
perhaps to be extended
"""
from PIL import Image
import numpy as np
import random, os 

# constants
# coupling strength is inverse temperature K = 1/T
# or beta = 1 / (k_B * T)
lattice_size = (600, 800) # h, w in image
lattice = np.random.randint(2, size=lattice_size)
lattice[lattice == 0] = -1
iterations = 100000
beta = 10



# pick a site at uniform
def pick_site(lat):
    (x,y) = (np.random.randint(lat.shape[0]), np.random.randint(lat.shape[1]))
    return (x,y)

#adjacent sites on 2d flat torus
# lattice, (x,y) -> [(x,y)]
def adjacencies(lat, point):
    x, y = point
    sites = []
    xs = []
    ys = []
    if x == 0:
        xs.append((lat.shape[0]-1, y))
        xs.append((x+1, y))
    elif x == lat.shape[0]-1:
        xs.append((0,y))
        xs.append((x-1,y))
    else:
        xs.append((x-1,y))
        xs.append((x+1,y))

    if y == 0:
        ys.append((x, lat.shape[1]-1))
        ys.append((x, y+1))
    elif y == lat.shape[1]-1:
        ys.append((x,0))
        ys.append((x,y-1))
    else:
        ys.append((x,y+1))
        ys.append((x,y-1))
    sites = xs + ys
    return sites

# calculate energy contribution of specific site on lattice
# energy :: lattice, (int, int) -> (float, float)
def calc_energy(lat, point):
    x, y = point
    current_energy = 0
    new_energy = 0
    for site in adjacencies(lat, (x,y)):
        current_energy += (-1) * lat[(x,y)] * lat[site]
        new_energy += lat[(x,y)] * lat[site]
    return (current_energy, new_energy)

# update site :: lattice, (int,int), beta -> lattice
def update_lattice(lat, point, beta):
    x,y = point
    (cur, new) = calc_energy(lat, (x,y))
    if new < cur:
        lat[(x,y)] *= -1
    elif np.exp(-beta*(new - cur)) > np.random.rand():
        lat[(x,y)] *= -1
    return lat

def draw_lattice(lat):
    imgarr = np.zeros(lat.shape, dtype=np.uint8)
    imgarr[lat == 1] = 255
    img = Image.fromarray(imgarr, mode="L")
    return img


# quench random lattice
img1 = draw_lattice(lattice)
imglist = []
for j in range(1000):
    for i in range(iterations):
        point = pick_site(lattice)
        update_lattice(lattice, point, beta)
    imglist.append(draw_lattice(lattice))

img2 = draw_lattice(lattice)
img1.show()
img2.show()
img1.save("test2.gif", save_all=True, append_images=imglist, duration=100,
          loop=0)
## vector (-1, 1) -> bw image
#def vec_to_img(vec, dims):
#    assert (dims[0] * dims[1] == vec.size),"vector size must mage output image"
#    arr = vec.reshape(dims)
#    imgarr = np.zeros(arr.shape, dtype = np.uint8)
#    imgarr[arr == 1] = 255
#    img = Image.fromarray(imgarr, mode="L")
#    return img
#
#
## turns all images in training directory into vectors
## Dir -> [Vec]
#def read_dir(dir, dims, threshold): 
#    files = os.listdir(dir)
#    vecs = np.zeros((len(files), dims[0]*dims[1]))
#    paths = []
#    for i in range(len(files)):
#        vecs[i]= vectorize_image(dir+ "/"+ files[i], dims, threshold)
#    return vecs
#
## generates weight matrix from directory of training images, Hebbian learning
#def hebbianWeights(vecs):
#    W = np.zeros((len(vecs[0]), len(vecs[0])))
#    for i in range(len(vecs)):
#        slice = vecs[i:(i+1),:]
#        W += np.dot(slice.T, slice)
#    W -= len(vecs) * np.identity(len(vecs[0]))
#    return W
#    
## Updates vector according to weight matrix
#def update_vector(vec, iterations):
#
#    return outvec
