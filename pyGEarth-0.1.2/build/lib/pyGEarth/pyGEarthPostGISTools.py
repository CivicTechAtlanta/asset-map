#!/python
#---------------------------------------
#
# pyGEarth KML Writer
#
#Description: Class to write Geodata to PostGIS 
#
#
#
#Copyright 2008 Eric B. Powell, Savannah River National Laboratory
#Date: 4/1/2008
#
#This in licensed under the GNU GPL V3.
#Please see license.txt for license details.
###########################################


import elementtree.ElementTree as ET
import sys
from pyGEarthGeometry import *
import psycopg2

class PostGIS:
        def __init__(self, dbName, UserName, HostName, Password):
            self.ConnString = "dbname='"+dbName+"' user='"+UserName+"' host='"+HostName+"' password='"+Password+"'"
        
        def connect(self):
                conn=psycopg2.connect(self.ConnString)
                return conn


class PostGISWrite(PostGIS):
        def __init__(self, dbName, UserName, HostName, Password,GeometryType, lstData, TableName, FieldList, intSRID):
                lstQuery = []
                PostGIS.__init__(self, dbName, UserName, HostName, Password)
                self.connection = self.connect()
                geoType = {"POINT":self.loadPoint, "LINE":self.loadLine,"POLYGON":self.loadPolygon}
                #ITerate through the items in the object and create an insert statement
                for objRow in lstData:
                    objGeo =geoType.get(GeometryType, self.errHandler(GeometryType, TableName))(objRow['shape'], intSRID)
                    #Generate the rest of the query
                    #First, extract the Z Coordinate and write to an elevation field....OGC Points are 2D so we carry Z as an attribute
                    Data = objRow['shape']
                    objCoord = Data.getCoordinates()
                    strFields = '(Elevation, '
                    strValues = '(' + str(objCoord[0][2]) + ", " 
                    del Data
                    del objCoord
                    for Field in FieldList:
                        strFields = strFields +  Field + ', '
                        #TODO: Filter the shape/geometry column
                        if Field != 'shape' and Field != 'Geometry':
                            strValues = strValues  + str(objRow[Field])+ ', '
                    strFields = strFields[:-2] +')'
                    strValues = strValues[:-2] + ', ' + objGeo + ')'
                    strSQL = 'INSERT INTO ' + TableName  + strFields + ' VALUES ' + strValues
                    #print strSQL
                    self.runInsert(strSQL)
                
        def loadPoint(self, Data, intSRID):
                objCoord = Data.getCoordinates()
                #strPointData = str(objCoord[0][0]) + " "+ str(objCoord[0][1])+ " "+ str(objCoord[0][2])
                strPointData = str(objCoord[0][0]) + " "+ str(objCoord[0][1])
                strGeometry = "GeomFromText('POINT(" + strPointData + ")', "+str(intSRID)+")";
                #Move to PostGIS 3D geometry
               # strGeometry = "GeomFromEWKT('SRID= "+str(intSRID)+"; POINT("+strPointData+")')"
                return strGeometry
                
        def loadLine(self,Data, TableName, FieldList):
                lstCoords = Data.getCoordinates()
                for objCoord in lstCoords:
                    strData = strData + str(objCoord[0][0]) + " "+ str(objCoord[0][1])+ " "+ str(objCoord[0][2])+', '
                strGeometry = 'GeomFromText("POLYLINE('+strData[:-2]+')" )';
                return strGeometry
                
        def loadPolygon(self, Data):
                for objPoint in Data:
                    strData = strData + str(objCoord[0][0]) + " "+ str(objCoord[0][1])+ " "+ str(objCoord[0][2])+', '
                strGeometry = 'GeomFromText("POLYGON('+ strData[:-2] +')" )';
                return strGeometry
            
        def errHandler(self,GeometryType, strTableName):
                print 'Unknown Geometry Type: ', GeometryType           
                
        def runInsert(self, strCommand):
                #iterate through the list insert statements
                cur = self.connection.cursor()
                #run the query
                cur.execute(strCommand)
                #commit each 
                self.connection.commit()
                        

class readPostGIS(PostGIS):
        def __init__(self, dbName, UserName, HostName, Password):
            print 'Not Yet written'
            PostGIS.__init__(self, dbName, UserName, HostName, Password)
                
if __name__ == "__main__":
        objPKL = parseKML(sys.argv[1], sys.argv[2])
        for strRow in objPKL.lstData:
                #print strRow
                objDBWrite = writeGeoData(sys.argv[2], objPKL.lstData, sys.argv[3], lstFields)
         
