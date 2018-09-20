"""
2d Ising Ferromagnet (on torus)
perhaps to be extended
"""
from PIL import Image
from datetime import datetime
import numpy as np
import random, os

# constants
# coupling strength is inverse temperature K = 1/T
# or beta = 1 / (k_B * T)
lattice_size = (300, 400) # h, w in image
lattice = np.random.randint(2, size=lattice_size)
lattice[lattice == 0] = -1
iterations = 50000
frames = 300
beta_crit = np.log(1 + 2 ** (1/2)) / 2
beta = 15
current_time = datetime.now().strftime('%Y-%m-%d-%H%M%S')
filename = f"{current_time}-beta-{beta}-"

# pick a site at uniform
def pick_site(lat):
    (x,y) = (np.random.randint(lat.shape[0]),
             np.random.randint(lat.shape[1]))
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
for j in range(frames):
    for i in range(iterations):
        point = pick_site(lattice)
        update_lattice(lattice, point, beta)
    imglist.append(draw_lattice(lattice))

img2 = draw_lattice(lattice)
#img1.show()
#img2.show()
img1.save((filename + ".gif"), save_all=True, append_images=imglist,
          duration=50, loop=0)

with open((filename + ".txt"), "w") as txt:
    print(f"Beta:  {beta}\nIterations per frame:  {iterations}\n"
          f"Frames:  {frames}\nSize:  {lattice_size}", file=txt)
