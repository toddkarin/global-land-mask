"""
Make maps of climate variables.
"""

import globe

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

# Plot in conus or world.
plot_range = 'conus'
# plot_range = 'world'


# Set up the map
fig = plt.figure(0, figsize=(5.5, 4.5))
plt.clf()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])


if plot_range=='conus':
    m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                projection='lcc', lat_1=33, lat_2=45, lon_0=-95,
                area_thresh=200,
                resolution='i')
    m.drawstates(linewidth=0.2)
elif plot_range=='world':
    m = Basemap(projection='cyl', llcrnrlat=-60, urcrnrlat=90, \
                llcrnrlon=-180, urcrnrlon=180, resolution='c')

m.drawcoastlines(linewidth=0.2)
m.drawcountries(linewidth=0.2)

print('Drawing map...')
cs = m.contourf(lon_grid, lat_grid, z, levels=[-0.5, 0.5,1.5], cmap="jet", latlon=True)

# m,cs = make_gridded_map(x,y,z,fig_number=1)
cbar = m.colorbar(cs,location='bottom',pad="5%")


plt.show()

