"""

Convert the elevation map into a global binary mask.

"""


import numpy as np

filename_save = '/Users/toddkarin/Documents/GLOBE/globe_combined.npz'

# Import the globe elevation map
elev = np.load(filename_save)

z = elev['z']
lat = elev['lat']
lon = elev['lon']

# Get the invalid values.
mask = z==-500

# Save as a compressed mask
filename_mask_save_compressed = 'globe_combined_mask_compressed.npz'
np.savez_compressed(filename_mask_save_compressed,
                    mask=mask,
                    lat=lat,
                    lon=lon)