"""
Make map of CONUS
"""

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


# # Compare to basemap is_land (this takes a very long time).

# print('Calculating points in map coordinates')
# xpt, ypt = m( lon_grid, lat_grid )
# print('Basemap is_land')
# f = np.vectorize(m.is_land)
# basemap_is_land = f(xpt,ypt)
#
# # Set up map 1
# fig = plt.figure(1, figsize=(5.5, 4.5))
# plt.clf()
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
#
# if plot_range=='conus':
#     m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
#                 projection='lcc', lat_1=33, lat_2=45, lon_0=-95,
#                 area_thresh=200,
#                 resolution='i')
#     m.drawstates(linewidth=0.2)
# elif plot_range=='world':
#     m = Basemap(projection='cyl', llcrnrlat=-60, urcrnrlat=90, \
#                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
#
# m.drawcoastlines(linewidth=0.2)
# m.drawcountries(linewidth=0.2)
#
# print('Drawing map...')
# cs = m.contourf(lon_grid, lat_grid, basemap_is_land, levels=[-0.5, 0.5,1.5], cmap="jet", latlon=True)
#
# plt.show()
#
