#!/bin/python
#---------------------------------------
#
# pyGEarth KML Parser
#
#Description: Class to import and parse  Google Earth
#a KML file and retrun the geometry as OGC compliant
#objects with name as description fields associated.
#
#Copyright 2007 Eric B. Powell, Savannah River National Laboratory
#Date: 9/7/2007
#
#This in licensed under the GNU GPL V3.
#Please see license.txt for license details.

    
import elementtree.ElementTree as ET
import sys
from pyGEarthGeometry import *

class KMLReader:
    
    def __init__(self, filename, datatype):
        self.lstData = []
        self.parsefile = {"Point":self.GetPoint, "Polyline":self.GetLines, "Polygon":self.getPolygons, "Cartography":self.getCartography}
        self.tree = ET.ElementTree(element=None,file = filename)
        self.rootElem = self.tree.getroot()
        ##lstChildren = self.rootElem.getchildren()
        ##self.elemDoc = lstChildren[0]
            
    def GetPoint(self):
        lstData = []
         #look for point geometry and return the data
        for element in self.lstObjs:
                lstChildren = element.getchildren()
                #lstRow = []
                dctRow = {}
                blnAdded = 0
                for objElem in lstChildren:
                        #get the Point element
                        if objElem.tag.count('Point') >0:
                                #now extract the coordinates
                                lstGeo = objElem.getchildren()
                                #Find the coordinates element and hand it to the extractpoints
                                #method - for now assue that this is the proper implementation
                                for objElement in lstGeo:
                                    if objElement.tag.count('coordinates')>0:
                                        lstCoord = self.ExtractPoints(objElement.text)
                                objPoint = Point()
                                objPoint.addPoint(lstCoord[0])
                                #lstRow.append(objPoint)
                                dctRow["Geometry"] = objPoint
                                blnAdded = 1
                        else:
                                #Row.append(objElem.text)
                                
                                #Since the description sometimes contains a <pre> subelment
                                #check for it.
                                if objElem.tag.count('description')>0:
                                    try:
                                        lstChildren = objElem.getchildren()
                                        dctRow[objElem.tag[33:]] = lstChildren[0].text
                                    except:
                                        dctRow[objElem.tag[33:]] = objElem.text
                                else:
                                    if objElem.tag.count('name')>0:
                                        dctRow[objElem.tag[33:]] = objElem.text
                #verify the geometry  -only return valid data
                if blnAdded == 1:
                    if objPoint.verify() == 1:
                        #lstData.append(lstRow)
                        lstData.append(dctRow)
        return lstData
        
    def GetLines(self):
        lstData = []
         #look for point geometry and return the data
        for element in self.lstObjs:
                lstChildren = element.getchildren()
                #lstRow = []
                dctRow = {}
                for objElem in lstChildren:
                        #get the Point element
                        blnAdded = 0
                        if objElem.tag.count('LineString') >0:
                                #now extract the coordinates
                                lstGeo = objElem.getchildren()
                                #Find the coordinates element and hand it to the extractpoints
                                #method - for now assue that this is the proper implementation
                                #determine which list member has the geometry element...
                                for objElement in lstGeo:
                                    if objElement.tag.count('coordinates')>0:
                                        lstCoord = self.ExtractPoints(objElement.text)
                                objLine = Polyline()
                                for objCoord in lstCoord:
                                    objLine.addPoint(objCoord)
                                #lstRow.append(objLine)
                                dctRow["Geometry"] = objLine
                                blnAdded = 1
                        else:
                                #Since the description sometimes contains a <pre> subelment
                                #check for it.
                                #Also, for now, only collect name a description. Other data willbe
                                #handled later
                                if objElem.tag.count('description')>0:
                                    try:
                                        lstChildren = objElem.getchildren()
                                        dctRow[objElem.tag[33:]] = lstChildren[0].text
                                    except:
                                        dctRow[objElem.tag[33:]] = objElem.text
                                else:
                                    if objElem.tag.count('name')>0:
                                        dctRow[objElem.tag[33:]] = objElem.text
                #verify the geometry -only return valid data
                if blnAdded == 1:
                    if objLine.verify() == 1:                                               
                        #lstData.append(lstRow)
                        lstData.append(dctRow)
        return lstData
                                         
    def getPolygons(self):
        lstData = []
        dctRings = {"{http://earth.google.com/kml/"+self.strKMLVer+"}outerBoundaryIs":"Outer", "{http://earth.google.com/kml/"+self.strKMLVer+"}innerBoundaryIs":"Inner"}
         #look for point geometry and return the data
        for element in self.lstObjs:
                lstChildren = element.getchildren()
                #lstRow = []
                dctRow = {}
                for objElem in lstChildren:
                        #get the Point element
                        if objElem.tag.count('Polygon') >0:
                                objPolygon = Polygon()
                                #now get the rings (OuterBoundaryIs, InnerBoundaryIS)
                                lstGeo = objElem.getchildren()
                                for child in lstGeo:
                                    #descend to the Linear Ring level
                                    lr = child.getchildren()
                                    #only support the elements with sub-elements (OutBoundaryIs, innBoundaryIs)
                                    try:
                                        lstGeo = lr[0].getchildren()
                                        objRing = Ring()
                                        #should now have a coordinates tag
                                        if lstGeo[0].tag.count('coordinates')>0:
                                               lstCoord = self.ExtractPoints(lstGeo[0].text)
                                               for objCoord in lstCoord:
                                                       objRing.addPoint(objCoord)
                                        #check that the ring was added properly
                                        if objRing.verify() == 1:
                                            #add the ring with the proper designation of the ring type (inner, outer)
                                            objPolygon.addRing(dctRings[child.tag], objRing)
                                        else:
                                            print 'Ring Geometry Failed', dctRings[child.text]
                                    except:
                                        #do nothing - send line to the terminal
                                        print
                                #lstRow.append(objPolygon)
                                dctRow['Geometry'] = objPolygon
                        else:
                            #add the other attributes
                            #lstRow.append(objElem.text)
                            dctRow[objElem.tag[33:]] = objElem.text
                     #verify the geometry and return -only return valid data
                if objPolygon.verify() == 1: 
                        #lstData.append(lstRow)
                        lstData.append(dctRow)
        
        return lstData
                                    
    def getCartography(self):
        print 'No cartography yet either'
    def getData(self):
        return self.lstData
    def errHandler(self):
        print 'Oops - Unknown Geometry Type Specified.'
            
    def getObjectElements(self, lstChildren, strObjName, dataroot = 'Document'):
        lstObjects = []
        #bore down past the document tag - probably need to beef this up a bit, eventually
        if lstChildren[0].tag.count(dataroot) >0:
            lstChildren = lstChildren[0].getchildren()
        for element in lstChildren:
                strTag = element.tag
                print strTag
                if strTag.count(strObjName) >0:
                        print element
                        lstObjects.append (element)
        return lstObjects

    def ExtractPoints(self, strData):
        #first, reomve the leading newline and leading space
        lstCoords = []
        strData = strData.lstrip()
        while len(strData)>0:
                intEnd = strData.find('\n')
                #Handle the single point special case...
                if intEnd < 0:
                    intEnd = len(strData)
                strCoord = strData[0:intEnd]
                #trim whitespace and newline character
                strCoord = strCoord.strip()
                intFirstComma = strCoord.find(',')
                intSecondComma = strCoord.rfind(',')
                objCoordinate = Coordinate(strCoord[0:(intFirstComma)],strCoord[(intFirstComma)+1: (intSecondComma)],strCoord[intSecondComma+1:len(strCoord)])
                lstCoords.append(objCoordinate)
                #Now, chop the processed data off of the coordinate string...this is where I have been
                #getting hung up.
                strData = strData[intEnd:]
                strData = strData.lstrip()
        return lstCoords
                        
class KMLReader20(KMLReader):
    def __init__(self, filename, datatype, georoot, dataroot):
        KMLReader.__init__(self, filename, datatype)
        self.strKMLVer = '2.0'
        lstChildren = self.rootElem.getchildren() #now have schema and wsr elements
        self.lstObjs = self.getObjectElements(lstChildren, georoot, dataroot)        
        self.lstData = self.parsefile.get(datatype, self.errHandler)()

class KMLReader21(KMLReader):
    def __init__(self, filename, datatype, georoot, dataroot):
        KMLReader.__init__(self, filename, datatype)
        self.strKMLVer = '2.1'
        lstChildren = self.rootElem.getchildren() #now we should have the Placemark and maybe schema elements
        self.lstObjs = self.getObjectElements(lstChildren, georoot, dataroot)
        self.lstData = self.parsefile.get(datatype, self.errHandler)()
        
                
if __name__ == "__main__":
##    if argv[3] == '2.1':
##        objPKL = KMLReader21(argv[1], argv[2])
##    else:
##        objPKL = KMLReader20(argv[1],argv[2])
    objPKL = KMLReader21("/home/ebpowell/Work/gvp_layer.kml", "Point", 'Placemark','Document')
    for strRow in objPKL.lstData:
        print 'Record: ',strRow 
