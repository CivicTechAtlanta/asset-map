#!/bin/python
#---------------------------------------
#
# pyGEarth KML Parser
#
#Description: Simple ESRI Toolbox script to load data from KML file
#and write it to the proper geodatabase table
#
#Copyright 2007 Eric B. Powell, Savannah River National Laboratory
#Date: 9/7/2007
#
#This in licensed under the GNU GPL V3.
#Please see license.txt for license details.

from pyGEarthReadKML import *
from pyGEarthGeometry import *
from pyGEarthESRITools import *

if __name__ == "__main__":
##    #First, read the KML file
    geo_type = sys.argv[2]
    outdb = sys.argv[4]
    systems = []

    if sys.argv[3] == '2.1':
        objPKL = KMLReader21(sys.argv[1], geo_type, sys.argv[5], sys.argv[6])
    else:
        objPKL = KMLReader20(sys.argv[1],geo_type, sys.argv[5], sys.argv[6])
    #Now, write the data to the proper database
    geo_processing_tools = write_geometry(objPKL.getData(), geo_type, outdb)

#    write = geoprocessing_tools.write_geometry(objPKL, 'Point', )

###Testing lines
##    workspace = 'O:\gis\Users\powell_eb\ATG_Data\ATG_Data.mdb'
##    table = 'WatchAreaPerimeter'
##    objPKL = KMLReader20('O:\gis\Users\powell_eb\ATG_Data\warnings.kml','Polyline', 'Placemark','Folder')
##    
##    geo_processing_tools = write_geometry(objPKL, "Polyline", workspace + '\\' + table)
##    
