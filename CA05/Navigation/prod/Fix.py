import datetime
import time
import os
from xml.etree import ElementTree
import Angle as Angle
from math import *

class Fix():
    """Fix class to perform different calculation based on sightings, aries and stars."""
    
    def __init__(self, logFile="log.txt"):
        """Constructor"""
        
        self.errors = 0
        self.approximateLatitude = 0.0
        self.approximateLongitude = 0.0
        self.assumedLat = None
        self.assumedLon = None
        self.hemi = ""
        
        if not isinstance(logFile, str) or len(logFile) < 1:
            self.raiseException("Fix.__init__:  The file name violates the parameter specification.")

        try:
            txtFile = open(logFile, "a")
            timestamp = time.time()
            tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
            tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
            tmp3 = tmp2.astimezone()
            local = tmp3.replace(microsecond=0)

            self.txtFile = txtFile
            self.txtFile.write("LOG: " + str(local) + " Log file:\t" + os.path.realpath(logFile) + "\n")
        except:
            self.raiseException("Fix.__init__:  The Logfile can not be created or appended for whatever reasons.")

    def raiseException(self, msg):
        """Raises a value error with received message"""

        raise (ValueError(msg))

    def setSightingFile(self, sightingFile=""):
        """Sets the sighting file"""
        
        if len(sightingFile.split(".")[0]) < 1:
            self.raiseException("Fix.setSightingFile:  The sighting file name violates the parameter specification.")

        if (sightingFile.split(".")[1]) != "xml":
            self.raiseException("Fix.setSightingFile:  Invalid sightingFile.")

        timestamp = time.time()
        tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
        tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
        tmp3 = tmp2.astimezone()
        local = tmp3.replace(microsecond=0)

        try:
            xmlFile = open(sightingFile, "r")
            xmlFile.close()
        except:
            self.raiseException("Fix.setSightingFile:  The sighting file not found or could not be opened.")

        self.sightingFile = sightingFile
        self.txtFile.write("LOG: " + str(local) + " Sighting file\t" + os.path.realpath(self.sightingFile) + "\n")

        return os.path.realpath(self.sightingFile)

    def setAriesFile(self, ariesFile=""):
        """Sets the aries file"""

        if len(ariesFile.split(".")[0]) < 1:
            self.raiseException("Fix.setAriesFile:  Received Filename is invalid")

        if ariesFile.split(".")[1] != "txt":
            self.raiseException("Fix.setAriesFile:  Received Filename is invalid")

        timestamp = time.time()
        tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
        tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
        tmp3 = tmp2.astimezone()
        local = tmp3.replace(microsecond=0)

        self.ariesFile = ariesFile

        try:
            f = open(self.ariesFile, "r")
            f.close()
        except Exception as e:
            self.raiseException("Fix.setAriesFile:  Aries file could not be opened")

        self.txtFile.write("LOG: " + str(local) + " Aries file:\t" + os.path.realpath(self.ariesFile) + " \n")

        return os.path.realpath(self.ariesFile)

    def setStarFile(self, starFile=""):
        """Sets the star file"""

        if len(starFile.split(".")[0]) < 1:
            self.raiseException("Fix.setStarFile:  Received Filename is invalid")

        if (starFile.split(".")[1]) != "txt":
            self.raiseException("Fix.setStarFile:  Received Filename is invalid")

        timestamp = time.time()
        tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
        tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
        tmp3 = tmp2.astimezone()
        local = tmp3.replace(microsecond=0)

        self.starFile = starFile
        self.txtFile.write("LOG: " + str(local) + " Star file:\t" + os.path.realpath(self.starFile) + " \n")

        try:
            f = open(self.starFile, "r")
            f.close()
        except Exception as e:
            self.raiseException("Fix.setStarFile:  Stars file could not be opened")

        return os.path.realpath(self.starFile)

    def getSightings(self,assumedLatitude="0d0.0", assumedLongitude="0d0.0"):
        """Performs all the calculations for each sighting record"""
        
        if not self.sightingFile or not self.ariesFile or not self.starFile:
            self.raiseException("Fix.getSightings:  sightingFile and/or ariesFile and/or starFile not set.")

        if not isinstance(assumedLatitude, str):
            self.raiseException("Fix.getSightings:  Invalid assumedLatitude.")

        for char in assumedLatitude:
            if char == "N":
                self.hemi = char
                assumedLatitude = assumedLatitude.replace(char, "")

            elif char == "S":
                self.hemi = char
                assumedLatitude = assumedLatitude.replace(char, "")

        degreesAndMinutes = assumedLatitude.split("d")
        deg = int(degreesAndMinutes[0])
        if deg < 0 or deg >= 90:
            self.raiseException("Fix.getSightings:  Invalid degrees of assumedLatitude.")
            
        minutes = float(degreesAndMinutes[1])
        if minutes < 0 or minutes >= 60:
            self.raiseException("Fix.getSightings:  Invalid minutes of assumedLatitude.")

        self.assumedLatitude = assumedLatitude
        self.assumedLongitude = assumedLongitude

        degreesAndMinutes = assumedLongitude.split("d")

        deg = int(degreesAndMinutes[0])
        if deg < 0 or deg >= 90:
            self.raiseException("Fix.getSightings:  Invalid degrees of assumedLongitude.")

        minutes = float(degreesAndMinutes[1])
        if minutes < 0 or minutes >= 60:
            self.raiseException("Fix.getSightings:  Invalid minutes of assumedLongitude.")

        try:
            tree = ElementTree.parse(self.sightingFile)  # VALUE ERROR 1 OPENING FILE
        except :
            self.raiseException("Fix.getSightings:  No sighting file has been set.")

        sightings = tree.findall("sighting")
        self.errorString = ""
        try:
            self.calculate(sightings)
            self.txtFile.close()
            return (self.approximateLat, self.approximateLon)
        except:
            self.raiseException("Fix.getSightings:  Some Tag are Missing.")

    
    def calculate(self,sightings):
        """Performs all the calculations for received sighting"""
        
        try:
            dataList = []

            for elem in sightings:
                dataDict = {}
                try:
                    dataDict["body"] = elem[0].text
                except:
                    self.errors += 1
                    self.errorString += "Body not found"
                    continue

                try:
                    dataDict["dt"] = elem[1].text
                except:
                    self.errors += 1
                    self.errorString += "Date not found"
                    continue
                try:
                    dataDict["time"] = elem[2].text
                except:
                    self.errors += 1
                    self.errorString += "Time not found"
                    continue
                try:
                    dataDict["observation"] = elem[3].text
                except:
                    self.errors += 1
                    self.errorString += "Observation not found"
                    continue

                try:
                    dataDict["height"] = elem[4].text

                except:
                    dataDict["height"] = "0"

                try:
                    dataDict["temperature"] = float(elem[5].text)
                except :
                      dataDict["temperature"] = 72

                try:
                    dataDict["pressure"] = elem[6].text

                except :
                    dataDict["pressure"] = "1010"

                try:
                    dataDict["horizon"] = elem[7].text
                except :
                    dataDict["horizon"] = "Natural"

                newAngle = Angle.Angle()
                newAngle.setDegreesAndMinutes(dataDict["observation"])

                dip = 0.0
                if  dataDict["horizon"].strip() == "natural":
                    dip = (-0.97 * sqrt(float( dataDict["height"].strip()))) / 60.0

                celcius = ( dataDict["temperature"] - 32) * 5.0 / 9.0
                newAngle.setDegreesAndMinutes( dataDict["observation"].strip())
                altitude = newAngle.getDegrees()

                refraction = -0.00452 * float(dataDict["pressure"].strip()) / float(273 + celcius) / tan(radians(altitude))
                adjustedAltitude = altitude + dip + refraction
                newAngle.setDegrees(adjustedAltitude)
                adjustedAltitude = newAngle.getDegrees()

                hours = dataDict["time"].split(":")[0]
                minutes = dataDict["time"].split(":")[1]
                seconds = dataDict["time"].split(":")[2]

                s = (int(minutes) * 60) + int(seconds)
                formatedDate = datetime.datetime.strptime(dataDict["dt"], '%Y-%m-%d').strftime('%m/%d/%y')

                SHAstarObj = Angle.Angle()
                flag = False
                with open(self.starFile, 'r+') as starFile:
                    for line in starFile:
                        name = line.split("\t")[0]
                        tempDt = line.split("\t")[1]
                        if name == dataDict["body"] and tempDt <= formatedDate:
                            tempStarLine = line
                            flag = True

                    if(not flag):
                        self.errors += 1
                        self.errorString += "Name or date not Found"
                        continue


                self.SHAstar = SHAstarObj.setDegreesAndMinutes(tempStarLine.split("\t")[2])
                self.latitude = (tempStarLine.split("\t")[3]).strip()

                angleObj1 = Angle.Angle()
                angleObj2 = Angle.Angle()

                tempAriesLine1 = ""
                tempAriesLine2 = ""
                with open(self.ariesFile, 'r+') as ariesFile:
                    for line in ariesFile:
                        tempDate = line.split("\t")[0]
                        tempHour = line.split("\t")[1]

                        hours = int(hours)
                        tempHour = int(tempHour)
                        if tempDate == formatedDate and tempHour == hours:
                            tempAriesLine1 = line
                            tempAriesLine2 = next(ariesFile).split("\t")[2]
                            break

                self.GHAaries1 = angleObj1.setDegreesAndMinutes(tempAriesLine1.split("\t")[2])
                self.GHAaries2 = angleObj2.setDegreesAndMinutes(tempAriesLine2)

                self.GHAaries = self.GHAaries1 + abs(self.GHAaries2 - self.GHAaries1) * (s / 3600)

                GHAariesObj = Angle.Angle()
                GHAariesObj.setDegrees(self.GHAaries)

                GHAariesObj.add(SHAstarObj)
                self.GHAobservation = GHAariesObj.getDegrees()

                asLatObj = Angle.Angle()
                asLatObj.setDegreesAndMinutes(self.assumedLatitude)
                asLat = asLatObj.getDegrees()
                if self.hemi == "S":
                    asLat = -asLat

                asLongObj = Angle.Angle()
                asLongObj.setDegreesAndMinutes(self.assumedLongitude)
                asLong = asLongObj.getDegrees()

                LHAObj = Angle.Angle()
                LHAObj.setDegreesAndMinutes(GHAariesObj.getString())
                LHAObj.add(asLongObj)
                LHA = LHAObj.getDegrees()

                latitudeObj = Angle.Angle()
                latitudeObj.setDegreesAndMinutes(self.latitude)

                interDistance = sin(radians(latitudeObj.getDegrees())) * sin(radians(asLat)) + cos(radians(latitudeObj.getDegrees())) * cos(radians(asLat)) * cos(radians(LHA))

                correctedAltitude = degrees(asin(interDistance))

                distanceAdjustment = int(round((correctedAltitude - adjustedAltitude) * 60, 0))
                dataDict['distanceAdjustment'] = distanceAdjustment

                numerator = sin(radians(latitudeObj.getDegrees())) - sin(radians(asLat)) * interDistance
                denominator = cos(radians(asLat)) * cos(radians(correctedAltitude))

                interAzimuth = numerator / denominator
                azimuthAdjustment = degrees(acos(interAzimuth))

                azimuthAdjustmentObj = Angle.Angle()
                azimuthAdjustmentObj.setDegrees(abs(azimuthAdjustment))
                dataDict['azimuthAdjustmentFloat'] = azimuthAdjustment
                dataDict['azimuthAdjustment'] = ("-" if azimuthAdjustment < 0 else "") + azimuthAdjustmentObj.getString()
                dataDict['assumedLatitude'] = "N" + asLatObj.getString() if asLat > 0 else str("S" + asLatObj.getString())
                dataDict['assumedLongitude'] = asLong
                dataDict['dttim'] = datetime.datetime.strptime(dataDict["dt"] + " " + dataDict["time"], "%Y-%m-%d %H:%M:%S")
                dataDict['degrees'] = newAngle.getString()
                dataDict['latitude'] = self.latitude
                dataDict['longitude'] = GHAariesObj.getString()

                dataList.append(dataDict)

            dataList.sort(key=lambda k: k['body'])
            dataList.sort(key=lambda k: k['dttim'])

            latSum = 0.0
            longSum = 0.0
            for data in dataList:
                timestamp = time.time()
                tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
                tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
                tmp3 = tmp2.astimezone()
                local = tmp3.replace(microsecond=0)
                self.txtFile.write(
                    "LOG: " + str(local) + " " + data["body"] + "\t" + data["dt"] + "\t" + data["time"] + "\t"
                    + data['degrees'] + "\t" + data['latitude'] + "\t" + data['longitude'] + "\t"
                    + dataDict['assumedLatitude'] + "\t"
                    + asLongObj.getString() + "\t" + data['azimuthAdjustment'] + "\t"
                    + str(data['distanceAdjustment']) + "\n")

                latSum += data['distanceAdjustment'] * cos(radians(data['azimuthAdjustmentFloat']))
                longSum += data['distanceAdjustment'] * sin(radians(data['azimuthAdjustmentFloat']))

            approximateLatitude = asLat + (latSum / 60)
            approximateLongitude = asLong + (longSum / 60)

            approximateLatitudeObj = Angle.Angle()
            approximateLatitudeObj.setDegrees(abs(approximateLatitude))
            appLat = approximateLatitudeObj.getString()
            if approximateLatitude < 0:
                appLat = "S" + appLat
            elif approximateLatitude > 0:
                appLat = "N" + appLat

            approximateLongitudeObj = Angle.Angle()
            approximateLongitudeObj.setDegrees(approximateLongitude)
            appLong = approximateLongitudeObj.getString()

            timestamp = time.time()
            tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
            tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
            tmp3 = tmp2.astimezone()
            local = tmp3.replace(microsecond=0)

            self.txtFile.write("LOG: " + str(local) + " Sighting errors:" + "\t" + str(self.errors) + "\n")
            self.txtFile.write("LOG: " + str(local) + "\t" + "Approximate latitude:\t" + appLat + "\tApproximate longitude:\t" + appLong + "\n")
            self.txtFile.write("LOG: " + str(local) + "\t" + "End of sighting file " + self.sightingFile)

            self.approximateLat = asLat
            self.approximateLon = asLong

        except:
            self.raiseException("Fix.calculate:  Mandatory tag is missing or the information associated with a tag is invalid.")
            
if __name__ == "__main__":
    fix = Fix()
    #     fix.setSightingFile("sight1.xml")
    fix.setSightingFile("sight2.xml")
    fix.setAriesFile("aries.txt")
    fix.setStarFile("stars.txt")
    #     fix.getSightings("N27d59.5", "85d33.4") # sight1
    fix.getSightings("S53d38.4", "74d35.3")  # sight2
