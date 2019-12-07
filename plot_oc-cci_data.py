#!/usr/bin/env python
"""
Plot OC-CCI data. Modified from nse's script in: https://gitlab.rsg.pml.ac.uk/cci/ccicode/blob/v3.1/rendering/basemap_snippets/nicks_chl.py



"""
import argparse
import datetime
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap

parser = argparse.ArgumentParser(description="Create PNGs from CCI data")
parser.add_argument("inputnetcdf",
                    type=str, help="Input netCDF file")
parser.add_argument("outputpng",
                    type=str, help="Output PNG file")
args = parser.parse_args()

# Open netCDF file
ds = netCDF4.Dataset(args.inputnetcdf)

# Get date for plot title
date_obj = datetime.datetime.strptime(args.inputnetcdf.split("-")[6], "%Y%m")
plot_title = "ESA CCI Ocean Colour - {}".format(date_obj.strftime("%m/%Y"))

# name of the variable to plot in the netCDF
var_name = "chlor_a"
# Label to use
cbar_label = "log(chlorophyll-a) [mg m$^{-3}$]"
# path to the output png
output_name = args.outputpng
# should we plot this with a log scale?
log = True

# What range of values should we plot?
min_value = 0.5
max_value = 20

try:
    lons, lats = ds.variables['lon'][:], ds.variables['lat'][:]
except KeyError:
    lons, lats = ds.variables['longitude'][:], ds.variables['latitude'][:]

# Extent
min_lat = lats.min()
max_lat = lats.max()
min_lon = lons.min()
max_lon = lons.max()

fig = plt.figure(figsize=(9, 4))
plt.title(plot_title)
# Display map in Equidistant Cylindrical Projection
# https://matplotlib.org/basemap/users/cyl.html
m = Basemap(projection='cyl', resolution='h',
            llcrnrlat=min_lat, urcrnrlat=max_lat,
            llcrnrlon=min_lon, urcrnrlon=max_lon)
# find x,y of map projection grid.
lons, lats = np.meshgrid(lons, lats)
x, y = m(lons, lats)
array = ds.variables[var_name][0,:,:]

masked = np.ma.masked_where(array == 0, array)
if log:
    norm = mpl.colors.LogNorm()
else:
    norm = None

im = m.pcolormesh(x, y, masked, vmin=min_value, vmax=max_value, norm=norm, cmap='viridis')
m.drawcoastlines(linewidth=0.1)
m.fillcontinents(color='0', lake_color='white', zorder=0)
m.drawparallels(np.arange(min_lat, max_lat, 1).astype(np.uint8), labels=[1,0,0,0], color='0.3', fontsize=10)
m.drawmeridians(np.arange(min_lon, max_lon, 1).astype(np.uint8), labels=[0,0,0,1], color='0.3', fontsize=10)
cbar = plt.colorbar(im)
cbar.set_label(cbar_label)
plt.tight_layout()
plt.savefig(output_name, bbox_inches='tight', dpi=150)
plt.close("all")
