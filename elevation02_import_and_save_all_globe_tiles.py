"""

Import the GLOBE datasets and combine them into a one big data file. Saves
the data to npz format.

In order to run this, you need to download the GLOBE datafiles from:
https://www.ngdc.noaa.gov/mgg/topo/gltiles.html

"""
import os
os.environ['PROJ_LIB'] = '/Users/toddkarin/anaconda3/share/proj'

from mpl_toolkits.basemap import Basemap, cm
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob



filename_save = '/Users/toddkarin/Documents/GLOBE/globe_combined.npz'
info = pd.read_csv('globe_file_info.csv')


fullpath = glob.glob('/Users/toddkarin/Documents/GLOBE/*10g')
fullpath.sort()

tile = []

# Import each tile
for j in range(len(fullpath)):
    filename_parts = os.path.split(fullpath[j])


    file_info = info[filename_parts[-1]==info['filename']]

    lat_max = file_info['lat_max'].iloc[0]
    lon_min = file_info['lon_min'].iloc[0]
    ncols = file_info['ncols'].iloc[0]
    nrows = file_info['nrows'].iloc[0]

    z_temp = np.fromfile(fullpath[j], dtype='<i2')

    z_temp = np.reshape(z_temp,(nrows, 10800))

    tile.append(z_temp)
    # z = np.concatenate( (z,z_temp),axis=0)


    lon_tile = lon_min + 1 / 120 * np.arange(10800)
    lat_tile = lat_max - 1 / 120 * np.arange(nrows)

# For tile, index 0 is lat, index 1 is longitude


# Put all the tiles together.
z = np.concatenate((
    np.concatenate((tile[0],tile[4],tile[8],tile[12]),axis=0),
    np.concatenate((tile[1],tile[5],tile[9],tile[13]),axis=0),
    np.concatenate((tile[2],tile[6],tile[10],tile[14]),axis=0),
    np.concatenate((tile[3],tile[7],tile[11],tile[15]),axis=0),
 ),axis=1)

# Set lat/lon lists
lat = 90 - 1/120 * np.arange(z.shape[0])
lon = -180 + 1/120 * np.arange(z.shape[1])

# Save the compressed data.
np.savez_compressed(filename_save,
                    z=z,
                    lat=lat,
                    lon=lon)


# Make a plot

downsample = 4
lat_select = np.arange(0,len(lat),downsample)
lon_select = np.arange(0,len(lon),downsample)

y = lat[lat_select]
x = lon[lon_select]

xg, yg = np.meshgrid(x, y)
zm = z[np.ix_(lat_select,lon_select)]

zm = np.ma.array(zm,mask=(zm==-500))


plot_range = 'world'
# plot_range = 'world'
# plot_range = 'india'


fig = plt.figure(0, figsize=(5.5, 4.5))
# Set up the map
# fig = plt.figure(j, figsize=(5.5, 4.5))
plt.clf()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# m = Basemap(projection='robin', lon_0=0, resolution='c')
if plot_range=='conus':
    m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                projection='lcc', lat_1=33, lat_2=45, lon_0=-95,
                area_thresh=3000,
                resolution='l')
    m.drawstates()
elif plot_range=='world':
    m = Basemap(projection='cyl', llcrnrlat=-60, urcrnrlat=90, \
                llcrnrlon=-180, urcrnrlon=180, resolution='c')


m.drawcoastlines(linewidth=0.5)
m.drawcountries()


print('Drawing map...')
cs = m.contourf(xg, yg, zm, levels=np.linspace(0,4000,40), cmap="jet", latlon=True)

# m,cs = make_gridded_map(x,y,z,fig_number=1)
cbar = m.colorbar(cs,location='bottom',pad="5%")


# plt.text(189841, 139184,year_str)
plt.show()

