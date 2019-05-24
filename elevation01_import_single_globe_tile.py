"""This script imports and plots a GLOBE datafile. In order to run this,
you need to download the GLOBE datafiles from:

https://www.ngdc.noaa.gov/mgg/topo/gltiles.html

"""


from mpl_toolkits.basemap import Basemap, cm
import matplotlib
import time
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



filename = '/Users/toddkarin/Documents/GLOBE/e10g'

print('importing (takes a little while)...')
z = np.fromfile(filename,dtype='<i2')

z = np.reshape(z,(round(z.__len__()/10800), 10800))

z[z==-500]=0
lat_min = 0
lat_max = 50
lon_min = -180
lon_max = -90

lon = lon_min + 1/120*np.arange(10800)
lat = lat_max - 1/120*np.arange(round(z.size/10800))


downsample = 2
lat_select = np.arange(0,len(lat),downsample)
lon_select = np.arange(0,len(lon),downsample)


y = lat[lat_select]
x = lon[lon_select]

xg, yg = np.meshgrid(x, y)
zm = z[np.ix_(lat_select,lon_select)]

plot_range = 'conus'
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
elif plot_range=='india':
    m = Basemap(projection='cyl', llcrnrlat=5, urcrnrlat=40, \
                llcrnrlon=65, urcrnrlon=95, resolution='c')
    # m = Basemap(llcrnrlon=65, llcrnrlat=5, urcrnrlon=95, urcrnrlat=40,
    #             projection='cyl', lat_1=33, lat_2=45, lon_0=-95,
    #             area_thresh=10000,
    #             resolution='l')

m.drawcoastlines(linewidth=0.5)
m.drawcountries()


cs = m.contourf(xg, yg, zm, levels=40, cmap="jet", latlon=True)

# m,cs = make_gridded_map(x,y,z,fig_number=1)
cbar = m.colorbar(cs,location='bottom',pad="5%")


# plt.text(189841, 139184,year_str)
plt.show()
#

    # print(f.read(2000))
#
# info = {}
# for j in range(len(info_df)):
#     info[info_df[0].iloc[j]] = info_df[1].iloc[j]
#
# print('Importing...')
# elevation = np.loadtxt(filename, skiprows=6,dtype=np.int16)
#
# print('Saving data...')
#
# filename_save = '/Users/toddkarin/Documents/SRTM_1km_ASC/srtm_1km.npz'
# np.savez_compressed(filename_save,
#                     elevation=elevation,
#                     ncols = info['ncols'],
#                     nrows = info['nrows'],
#                     xllcorner = info['xllcorner'],
#                     yllcorner = info['yllcorner'],
#                     cellsize = info['cellsize'],
#                     NODATA_value = info['NODATA_value'],
#                     )
#
# # data = np.load(filename_save)