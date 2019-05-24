# global-land-mask
Check whether a lat/lon point is on land for any point on earth.

# Description
This python module, global-land-mask, contains scripts for checking whether a lat/lon point is on land or sea. In order to do this, we use the GLOBE dataset, which samples the entire earth at 1 km resolution. We then simply extract all 'invalid' values from this elevation map and save to file.

The global mask is of shape (21600, 43200), equating to about 980 mB when saved without compression. This data can be compressed to 2.5 mb using numpy savez_compressed, making for a very compact package.

The raw elevation data from the GLOBE dataset can be downloaded from 
https://www.ngdc.noaa.gov/mgg/topo/gltiles.html
It is not necessary to download this data in order to use the global land mask. However, by downloading one can build a global elevation dataset using the functions provided.

This package provides globe.is_land(), an alaternative to Basemap.is_land(). For 10,000 data points, globe.is_land is around 6000 times faster than Basemap.is_land.

# Simple example

Here is a simple example showing the use of global_land_mask to check if lat/lon points are on land.
```python
from global_land_mask import globe
import numpy as np

# Check if a point is on land:
lat = 40
lon = -120
is_on_land = globe.is_land(lat, lon)

print('lat={}, lon={} is on land: {}'.format(lat,lon,is_on_land))
# lat=40, lon=-120 is on land: True

# Check if several points are in the ocean
lat = 40
lon = np.linspace(-150,-110,3)
is_in_ocean = globe.is_ocean(lat, lon)
print('lat={}, lon={} is in ocean: {}'.format(lat,lon,is_in_ocean))
# lat=40, lon=[-150. -130. -110.] is in ocean: [ True  True False]

```

# Speed test

Compare performance of global_land_mask and Basemap.
```python
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
```

# Example of map over US

Try running

```python
from global_land_mask import globe
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# Lat/lon points to get
lat = np.linspace(-20,90,1000)
lon = np.linspace(-130,-60,1002)

# Make a grid
lon_grid, lat_grid = np.meshgrid(lon,lat)

# Get whether the points are on land.
z = globe.is_land(lat_grid, lon_grid)

# Set up map
fig = plt.figure(0, figsize=(5.5, 4.5))
plt.clf()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
            projection='lcc', lat_1=33, lat_2=45, lon_0=-95,
            area_thresh=200,
            resolution='i')
m.drawstates(linewidth=0.2)
m.drawcoastlines(linewidth=0.2)
m.drawcountries(linewidth=0.2)


cs = m.contourf(lon_grid, lat_grid, z,
                levels=[-0.5, 0.5,1.5],
                cmap="jet",
                latlon=True)
plt.show()

plt.savefig('example_plot_globe_map_us.png',
            bbox_inches='tight',
            dpi=400)

```

to create the binary mask for the US, shown in the image below:

![Map of Land Mask](https://github.com/toddkarin/global-land-mask/blob/master/global_land_mask/example_plot_globe_map_us.png "Map of Land Mask")

Note that lakes are included as "on land" and the resolution isn't perfect, but it's good enough for many purposes!