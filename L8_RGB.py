#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
###############################################################################
#          How to: Create RGB Natural Color Composite from Landsat 8          #
###############################################################################
# @author: Cole Krehbiel                                                      #  
# Last Updated: 10-01-17                                                      #  
###############################################################################
"""
# Import libraries
import glob
import numpy as np
from osgeo import gdal
import scipy.misc as sm

# Set input directory
in_dir = '/Users/cole/Desktop/Website/Landsat/'

# Search directory for desired bands
b2_file = glob.glob(in_dir + '**B2.TIF') # blue band
b3_file = glob.glob(in_dir + '**B3.TIF') # green band
b4_file = glob.glob(in_dir + '**B4.TIF') # red band

# Define a function to normalize each band array by the min and max values
def norm(band):
    band_min, band_max = band.min(), band.max()
    return ((band - band_min)/(band_max - band_min))

# Loop through however many Landsat 8 obs are in the input directory 
for i in range(len(b2_file)):   
    
    # Open each band using gdal
    b2_link = gdal.Open(b2_file[i])
    b3_link = gdal.Open(b3_file[i])
    b4_link = gdal.Open(b4_file[i])
    
    # call the norm function on each band as array converted to float
    b2 = norm(b2_link.ReadAsArray().astype(np.float))
    b3 = norm(b3_link.ReadAsArray().astype(np.float))
    b4 = norm(b4_link.ReadAsArray().astype(np.float))
    
    # Create RGB
    rgb = np.dstack((b4,b3,b2))
    del b2, b3, b4
    
    # Visualize RGB
    #import matplotlib.pyplot as plt
    #plt.imshow(rgb)
    
    # Export RGB as TIFF file
    # Important: Here is where you can set the custom stretch
    # I use min as 2nd percentile and max as 98th percentile
    sm.toimage(rgb,cmin=np.percentile(rgb,2),
               cmax=np.percentile(rgb,98)).save(b2_file[i].split('_01_')[0]
               +'_RGB.tif')
