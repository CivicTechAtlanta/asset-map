#!/python
#---------------------------------------------------------------
#
# pyGEarth Geometry Classes
#
#Description: Class (and subclasses) to implement the OGC simple feature Geomtry
#
#Copyright 2007 Eric B. Powell, Savannah River National Laboratory
#Date: 9/7/2007
#
#This in licensed under the GNU GPL V3.
#Please see license.txt for license details.

#Geometry is an abstract class to be overloaded by Point, MultiPoint, PolyLine, Ring and Polygon
#We don't do complex geometry yet....
#------------------------------------------------------------------
class Geometry:
    def __init__(self):
        self.lstCoordinates = []
    def addPoint(self,objCoordinate):
        self.lstCoordinates.append(objCoordinate)
    def Verify(self):
        #abstract method to be pverloaded as appropriate
        return 0
    def getCoordinates(self):
        return self.lstCoordinates
        
class Point(Geometry):
    def __init__(self):
        Geometry.__init__(self)

    def verify(self):
       intResult = 0
       #check number of coordinates (need at least three)
       if len(self.lstCoordinates) > 0:
           intResult =  1
       return intResult
    
class Polyline(Geometry):
    def __init__(self):
        Geometry.__init__(self)

    def verify(self):    
       intResult = 0
       #check number of coordinates (need at least three)
       if len(self.lstCoordinates) >= 2:
           intResult =  1
       return intResult
        
class MultiPoint(Geometry):
    def __init__(self):
       Geometry.__init__(self,parent)
        
    def verify(self):
       intResult = 0
       #check number of coordinates (need at least three)
       if len(self.lstCoordinates) >= 2:
           intResult =  1
       return intResult
       
class Polygon(Geometry):
    def __init__(self):
       Geometry.__init__(self)
       self.lstRings = []
    def addRing(self, strRingType, objRing):
       pRing = []
       pRing.append(strRingType)
       pRing.append(objRing)
       self.lstRings.append(pRing)
    def getRing(self, RingType):
        lstRings = []
        for objRing in self.lstRings:
            if objRing[0] == RingType:
                lstRings.append(objRing)
        return lstRings

    def getRingInfo(self):
        dctRing = {'Outer':0, 'Inner':0}
        for objRing in self.lstRings:
            if objRing[0] == 'Outer':
                dctRing['Outer'] = dctRing['Outer'] + 1
            else:
                dctRing['Inner'] = dctRing['Inner'] + 1
        return dctRing

    def verify(self):
       #verify that there is an outer ring
       intResult = 0
       for Ring in self.lstRings:
          if Ring[0] == 'Outer':
                intResult = 1
           # else:
                #verify that the inner ring points are within the outer ring
           #     lstCoords[0] = self.LstRings['Outer']
           #     lstCoords[1] = Ring
            #iterate through the lists
       return intResult
        
        
class Ring(Geometry):
    def __init__(self):
        Geometry.__init__(self)

    def verify(self):
       intResult = 0
       #check number of coordinates (need at least three)
       if len(self.lstCoordinates) >= 3:
           #check that ring closes (first and last are the same)
           sc=  self.lstCoordinates[0]
           ec= self.lstCoordinates[len(self.lstCoordinates)-1]
           if ec.X == sc.X and ec.Y==sc.Y and ec.Z==sc.Z:
               intResult =  1
       return intResult

class Coordinate:
    def __init__(self, dblX=0.0, dblY=0.0, dblZ=0.0):
        self.X = dblX
        self.Y= dblY
        self.Z= dblZ
    def getValue(self, strCoord):
        dctValue = {'X':self.X, 'Y':self.Y, 'Z':self.Z}
        return dctValue[strCoord]
