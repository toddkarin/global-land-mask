# global-land-mask
Check whether a lat/lon point is on land for any point on earth

# Description
This python module, global-land-mask, contains scripts for checking whether a lat/lon point is on land or sea. In order to do this, we use the GLOBE dataset,which samples the entire earth at 1 km resolution. We then simply extract all 'invalid' values from this elevation map and save to file.

The global mask is of shape (21600, 43200), equating to about 980 mB when saved without compression. This data can be compressed to 2.5 mb using numpy savez_compressed, making for a very compact package.

The raw elevation data from the GLOBE dataset can be downloaded from 
https://www.ngdc.noaa.gov/mgg/topo/gltiles.html
It is not necessary to download this data in order to use the global land mask. However, by downloading one can build a global elevation dataset.