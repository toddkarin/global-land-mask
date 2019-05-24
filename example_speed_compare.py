"""

Compare the evaluation speed of globe.is_land and Basemap.is_land()

"""

from global_land_mask import globe
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import time


# Lat/lon points to get
lat = np.linspace(-20,50,100)
lon = np.linspace(-130,-70,100)

# Make a grid
lon_grid, lat_grid = np.meshgrid(lon,lat)

# Get whether the points are on land using globe.is_land
start_time = time.time()
globe_land_mask = globe.is_land(lat_grid, lon_grid)
globe_run_time = time.time()-start_time
print('Time to run globe.is_land(): {}'.format(globe_run_time))

# Get whether the points are on land using Basemap.is_land
# bm = Basemap(projection='cyl',resolution='i')
bm = Basemap(projection='cyl', llcrnrlat=-60, urcrnrlat=90, \
            llcrnrlon=-180, urcrnrlon=180, resolution='c')
f = np.vectorize(bm.is_land)

start_time = time.time()
xpt, ypt = bm( lon_grid, lat_grid)
basemap_land_mask = f(xpt,ypt)
basemap_run_time = time.time()-start_time
print('Time to run Basemap.is_land(): {}'.format(basemap_run_time))

print('Speed up: {}'.format(basemap_run_time/globe_run_time))

# Check agreement (note there is a different treatment for lakes
fraction_agreed = np.sum(globe_land_mask == basemap_land_mask)/len(globe_land_mask.flatten())
print('Fraction agreeing: {}'.format(fraction_agreed))