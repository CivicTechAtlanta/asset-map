
#---------------------------------------
#
# pyGEarth ESRI Geoprocessing Interface
#
#Description: Read and Write data to ESRI formats via the GeoProcessing
#Toolkit
#
#Copyright 2007 Eric B. Powell, Savannah River National Laboratory
#Date: 9/7/2007
#
#This in licensed under the GNU GPL V3.
#Please see license.txt for license details.

    
import win32com.client, os, math
from pyGEarthGeometry import *
import math
from pyproj import Proj
#Reprojects a point from one projection to another

class reproject: #modified from test script by Bruce Reeves
    def __init__(self):
        self.conv_x = 0.0
        self.conv_y = 0.0
    def convert(self, point, insys, outsys):
        print point[0], point[1], insys, outsys
        oSRS=win32com.client.Dispatch("Srs_con.Point2D.1")
        oSRS.Projection=insys
        oSRS.X=point[0]
        oSRS.Y=point[1]
        oSRS.Convert()
        if int(outsys) == 1:
            self.conv_x = oSRS.SRSeast
            self.conv_y = oSRS.SRSnorth
        elif int(outsys) == 2:
            self.conv_x = oSRS.SPeast
            self.conv_y = oSRS.SPnorth
        elif int(outsys) == 3:
            self.conv_x = oSRS.UTMeast
            self.conv_y = oSRS.UTMnorth
        else:
            print 'Shouldnt be here'
            self.conv_x = oSRS.Longitude
            self.conv_y = oSRS.Lattitude

#Write geoemtry to a geodatabase
#Imput data is in the form of a list of records consisting of a list of points.
class gdbworkspace:
    def __init__(self):
        self.exists = 0
        
    def checkexists(self, workspace, table, geo_type):
        if geo_type == 'Line String':
           gtype = 'polyline'
        else:
            gtype = geo_type

        gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
        gp.Workspace = workspace
        if gp.Exists(table):
            print 'Table' + table +  ' exists'
            print gp.Describe(table).FeatureType
            self.exists = 1
            #Commented out for debugging 6/9/2005
            #if gp.Describe(table).FeatureType == gtype:
            #    self.exists = 1
                
    def create(self,workspace, table, geo_type, refws, reffc):
        #Need to add code to set spatial reference
        gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
        gp.Workspace = workspace
        if geo_type == 'Line String':
           gtype = 'polyline'
        else:
            gtype = geo_type
        spatialref = self.build_spatialref(refws, reffc)
        gp.CreateFeatureClass(gp.workspace, table, gtype, '','','', spatialref.SpatialReference)

    def build_spatialref(self, refws, reffc):
        gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
        gp.Workspace = refws
        ptDesc=gp.Describe(reffc)
        return ptDesc

class write_geometry:
    def __init__(self, lstGeo, geo_type, workspace, lstFields):
        self.OID = ''
        #Set up the cursor and the geoprocessor
        self.gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
        #Set to overwrite mode
        self.gp.OverwriteOutput = 1
        self.workspace = workspace
        self.result = []
        dctgeometry = {"Point":self.writePoint, "Polyline":self.writeLine,\
                       "Polygon":self.writePolygon}
        
        #New code to make things a little cleaner
        cur = self.gp.InsertCursor(self.workspace)
        #print len(lstGeo), " Rows"
        for row in lstGeo:
            
            objGeo = dctgeometry.get(geo_type, self.errHandler)(row['Geometry'])
            feat = cur.NewRow()
            feat.setvalue('Shape', objGeo)
            try:
                for Field in lstFields:
                    feat.setvalue(Field, row[Field]) 
            #insert the record into the ESRI feture class
            except:
                print "Error generating record"
                del cur
                raise
            try:
                cur.InsertRow(feat)
            except:
                #Discard record and continue
                print "Error Inserting Row. Discarded"
                for Field in lstFields:
                    print Field, row[Field]
                #print row['Shape']
            else:
                #If everything goes well, insert record into featureclass
                self.result.append(0)   
        #Close the cursor to free-up database
        del cur
            
    def writePoint(self,objGeometry):
        x = 1
        pnt = self.gp.CreateObject("Point")
        #now extract the point from the row
        objPoint = objGeometry
        objCoord = objPoint.getCoordinates()
        #now write the point to the ESRI point object
        pnt.id = x + 1
        pnt.x = objCoord[0].getValue('X')
        pnt.y= objCoord[0].getValue('Y')
        pnt.z= objCoord[0].getValue('Z')

        return pnt

    def writeLine(self, objGeometry):
        x = 1
        objLine = objGeometry
        lstPoints = objLine.getCoordinates()
        lineArray = self.gp.CreateObject("Array")
        pnt = self.gp.CreateObject("Point")
        for point in lstPoints:
            #need to extract the Coordinate object, and from there the coord values
            pnt.id = x
            pnt.x = point.getValue('X')
            pnt.y = point.getValue('Y')
            pnt.z = point.getValue('Z')
            lineArray.add(pnt)
            x = x + 1

        return lineArray
    
 # Simple polygon suppport until I can figure out how to do
        #donut holes etc.
    def writePolygon(self, objGeometry):
        lstPoints = []
        polyArray = self.gp.CreateObject("Array")
        #get the outer ring from the Polygon object
        lstORings = objGeometry.getRing('Outer')
        lstIRings = objGeometry.getRing('Inner')
            #generate the list of points for the outer ring
        for oRing in lstORings:
            lstCoords = self.writeRing(oRing)
            for pnt in lstCoords:
                lstPoints.append(pnt)
        for iRing in lstIRings:
            lstPoints.append()
            lstCoords = self.writeRing(oRing)
            for pnt in lstCoords:
                lstPoints.append(pnt)
        for pnt in lstPoints:
            polyArray.add(pnt)
        return polyArray
    
    def writeRing(self, objRing):
        x = 1
        lstPnts =[]
        lstPoints = []
        lstPoints = objRing[1].getCoordinates()
        for point in lstPoints:
            try:
                pnt = self.gp.CreateObject("Point")
                pnt.id = x
                pnt.x = point.getValue('X')
                pnt.y = point.getValue('Y')
                pnt.z = point.getValue('Z')
                #print point.getValue('X'),point.getValue('Y'),point.getValue('Z')
                lstPnts.append(pnt)
                x = x + 1
            except:
                print 'Bad Point Detected. Discarded'
        return lstPnts
    
    def errHandler(self):
        print 'Unknown geometry type specified.'
        return 0
    
    def getResult(self):
        return self.result
        
class readgeometry:
    #Reads the geometry from a given location
    #Returns a list of pointsets for each geomtric element in the source database, translated into the
    #desired coordinate system, from the starting coordinate system
    def __init__(self,workspace, featureclass):
        self.geometry = []
        self.dctgeometry = {"Point":self.readPoint, "Polyline":self.readLine, \
                            "Polygon":self.readPolygon}
        self.workspace = workspace
        self.featureclass = featureclass
        
        
    def read(self, whereclause=""):
        lstRows = []
        lstFields = []
        gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
        gp.Workspace = self.workspace
        #get the fieldnames collection - com object
        objArrFieldNames = gp.listfields(self.featureclass)
        #Work arround a long-standing ESRI bug - cursor reset method does not work, iterate through and write values to python list
        objField = objArrFieldNames.next()
        while objField:    
            lstFields.append(objField.name)
            objField = objArrFieldNames.next()
        del objArrFieldNames
        #End work around
        lstData = gp.SearchCursor(self.featureclass, whereclause)
        objRow = lstData.next()
        #iterate through the list of rows
        geo_type = gp.Describe(self.featureclass).ShapeType
        while objRow:
            dctRow = {}
            #First extract the information from the binary blob...
            objShape = objRow.shape
            dctRow['Geometry'] = self.dctgeometry.get(geo_type, self.errHandler)(objShape)
            del objShape
            #add the other attributes of the row
            for strFieldName in lstFields:
                dctRow[strFieldName]= objRow.getvalue(strFieldName)
            lstRows.append(dctRow)
            del dctRow
            objRow = lstData.next()
        del objRow
        del lstData
        del lstFields
        return lstRows

    def readPoint(self, objShape):
        objPoint = Point()
        #pointarray = objShape.GetPart(0)
        #point = pointarray.Next()
        point = objShape.GetPart(0)
        objCoord = Coordinate(point.X, point.Y, point.Z)
        objPoint.addPoint(objCoord)
        return objPoint

    def readPolygon(self,objShape):
        #Initial implementation does NOT include donut hole support....
        #I suspect that these are handled via multi-part...
        objPoly = Polygon()
        objRing = Ring()
        #Get the binary shape blob from the Geoprocessor....
        pointarray = objShape.GetPart(0)
        point = pointarray.next()
        while point:
            objCoord = Coordinate(point.X, point.Y, point.Z)
            objRing.addPoint(objCoord)
            del objCoord
            point = pointarray.next()
        objPoly.addRing("Outer", objRing)
        del objRing
        return objPoly

    def readLine(self,objShape):
        objLine = Polyline()
        pointarray = objShape.GetPart(0)
        coord = pointarray.next()
        while coord:
            objCoord = Coordinate(coord.X, coord.Y, coord.Z)
            objLine.addPoint(objCoord)
            coord = pointarray.next()
        return objLine
    
    def errHandler(self, objShape):
        print 'Unknown geometry type specified.'
        return 0

class geodatabase:
    def create(self,workspace):
        gp = win32com.client.Dispatch('esriGeoprocessing.GpDispatch.1')
        pathlist = os.path.split(workspace)
        gp.CreatePersonalGDB(pathlist[0], pathlist[1])

def genCircle(dblOrX, dblOrY, dblRadius, intPntCnt):
    #First determine the X and Y value of the point at 0 degrees
    StartX = dblOrX-dblRadius
    StartY = dblOrY
    lstCoords = []
    #Scale the point count steps to the diameter of the cirle
    dblStep = (2*dblRadius)/intPntCnt
    #Generate the Y Coordinate above the origin (order left to right)
    XCoord = StartX
    for i in range(intPntCnt+1):
        XCoord= StartX + i*dblStep
        YCoord = math.sqrt(dblRadius**2 - (XCoord - dblOrX)**2)+dblOrY
        objCoord = (XCoord, YCoord)
        lstCoords.append(objCoord)
    #Generate the X coordinates below the origin (order right to left)
    for i in range(intPntCnt,-1, -1):
        XCoord= StartX + i*dblStep
        objCoord1 = (XCoord, dblOrY -math.sqrt(dblRadius**2 - (XCoord - dblOrX)**2))
        lstCoords.append(objCoord1)
    return lstCoords


if __name__ == "__main__":
    p = Proj(proj="lcc", lon_0='-96', lat_1='33',  lat_2='45', lat_0='39')
    lstPolys = []
    lstPoints = [[-96.001002553566011, 39.000634944983922, 0], \
                 [-96.001002569405244, 39.000634945431393, 0],\
                 [-96.001002566037087, 39.000634953849875, 0], \
                 [-96.001002550197384, 39.000634953402425, 0],\
                 [-96.001002553566011, 39.000634944983922, 0]]
    lstPolys.append(lstPoints)
    del lstPoints
    lstPoints = [[-81.6432745404, 33.2546205163, 0], \
             [-81.6432787044, 33.2551887409, 0],\
             [-81.6426023895, 33.2551922377, 0], \
             [-81.6425982299, 33.254624013, 0],\
             [-81.6432745404, 33.2546205163, 0]]
    lstPolys.append(lstPoints)
    del lstPoints
    for poly in lstPolys:
        objPoly = Polygon()
        objRing  =Ring()
        
        for pnt in poly:
            print pnt[0], pnt[1], pnt[2]
            point = p(pnt[0],pnt[1])
            print point[0],point[1]
            objCoord = Coordinate(point[0], point[1], pnt[2])
            del point
            objRing.addPoint(objCoord)
            del objCoord
        objPoly.addRing("Outer", objRing)
        dctRow = {"Geometry":objPoly}
        lstData = [dctRow]
        lstFields = []
        write = write_geometry(lstData, "Polygon", "Database Connections\\ESD_Sandbox.sde\\LPDM_Poly", lstFields)
                            
