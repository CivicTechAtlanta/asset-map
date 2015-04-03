#/usr/bin/python

#----------------------------------------------------------
#
#   Class pyGEarthWriteKML
#   Written By: Eric B. Powell
#
#   October 2, 2007
#
#   Based very loosely on pyKML but implemented
#   using ElementTree instead of minidom
#
#   Decription: Class to write KML files from the pyGEarth
#   geometry objects.
#----------------------------------------------------------

from elementtree.ElementTree import ElementTree
from elementtree.ElementTree import Element, SubElement
from pyGEarthGeometry import *
import os, sys
class KMLWriteGeo:
    def __init__(self, lstData, GeoType, strPath, strFilename, strLayername):
            
            dctWriteKML = {'Point': self.writePoint, 'Polyline': self.writeLine, 'Polygon': self.writePolygon}

            #Create new element tree with a root of KML...
            
            objRoot = Element("{http://earth.google.com/kml/2.1}kml")
            objTree = ElementTree(element=objRoot)
            elemDoc = SubElement(objRoot, 'Document')
            elemDocName = SubElement(elemDoc, 'name')
    #According the KML spec, default Polystyle stuff goes here...
            elemDocName.text = strLayername
            #Add a document name element here...populate from supplied parameters
            for objRow in lstData:
                    elemPlace = SubElement(elemDoc, 'Placemark')
                    elemName =SubElement(elemPlace,'name')
                    elemName.text = objRow['Name']
                    #Add support for the description tag...
                    elemDesc = SubElement(elemPlace, 'description')
                    elemDesc.text = objRow['Description']
                    elemGeo = dctWriteKML.get(GeoType, self.errHandler)(objRow['Geometry'], elemPlace)
                    elemPlace.append(elemGeo)
            self.Write(objTree, strPath, strFilename)
            
    def writePoint(self, objGeo, elemPlace):
            elemGeo = Element('Point')
            elemCoords = SubElement(elemGeo, "coordinates")
            strCoord = self.addCoordinates(objGeo) 
            elemCoords.text = self.addCoordinates(objGeo)
            return elemGeo
    
    def writeLine(self, objGeo, elemPlace):
            elemGeo = Element('LineString')
            elemCoords = SubElement(elemGeo, "coordinates")
            elemCoords.text = self.addCoordinates(objGeo)
            return elemGeo
     
    def writePolygon(self, objGeo, elemPlace):
            elemGeo = Element('Polygon')
            #Now add the ring(s)
            dctRings = objGeo.getRingInfo()
            #get the external ring(s)
            lstOuter = objGeo.getRing('Outer')
            lstInner = objGeo.getRing('Inner')
            for x in range(0, dctRings['Outer']):
                    elemRing = self.addRing(lstOuter[x], 'Outer')
                    elemGeo.append(elemRing)
                    
            for x in range(0, dctRings['Inner']):
                    elemRing = self.addRing(lstInner[x], 'Inner')
                    elemGeo.append(elemRing)
                    
            return elemGeo

    def addCoordinates(self, objGeo):
            #get the coordinates from the Geometry object
            lstCoords = objGeo.getCoordinates()
            strCoords = '\n'
            #serialize the data
            for objCoord in lstCoords:
                    strCoords = strCoords +  str(objCoord.getValue('X')) + ',' + str(objCoord.getValue('Y')) + ',' + str(objCoord.getValue('Z')) + "\n"
            #write the string to the elemCoords text attribute
            return strCoords

    def addRing(self, objRing, strType):
            if strType == 'Inner':
                    elemBnd = Element('innerBoundaryIs')
            else:
                    elemBnd = Element('outerBoundaryIs')
            elemRing = SubElement(elemBnd, 'LinearRing')
            elemCoords = SubElement(elemRing, "coordinates")
            elemCoords.text = self.addCoordinates(objRing[1])
            return elemBnd
            
    def errHandler(self,objGeo, elemPlace):
            print 'Error Occured Generating output'
            return 0
            
    def Write(self, tree, Path, Filename):
            #Write the tree to a temp file
            TempPath = Path + r"\\temp1.xml"
            tree.write(TempPath, "UTF-8")
            #perform postprocessing on the file to remove the added ns0 tags
            #elementtree helpfully adds and Google Earth chokes upon.
            self.PostProcess(TempPath, Path+ "\\" + Filename)
     
    def PostProcess(self, TempPath, FPath):
            f = open(TempPath, 'r')
            f1 = open(FPath, 'w')
            for line in f:
                    line = line.replace('ns0:','')
                    line = line.replace(':ns0','')
                    f1.write(line)
            f.close()
            #Delete the temporary file...
            os.remove(TempPath)
            #Close the output file
            f1.close()


if __name__ == '__main__':
    lstPnts = []
    objGeo = Polygon()
    objRing = Ring()
    X = 1
    Y=2
    Z=3
    for x in range (0,5):
        objCoord = Coordinate(X+x, Y+x, Z+x)
        objRing.addPoint(objCoord)
        #objGeo.addPoint(objCoord)
    objGeo.addRing('Outer', objRing)
    print objGeo
    objRow = {'Geometry':objGeo, 'Name':'Some Random Text'}
    lstPnts.append(objRow)
    objKML = KMLWriteGeo(lstPnts, 'Polygon', 'c:\\test\\', "test.kml")
    
