import datetime
import time
import os
from xml.etree import ElementTree
import Angle as Angle
from math import *


class Fix():
    """ Fix is calculating approximate a geographical position base on received navigational information.
    """
    def __init__(self, logFile="log.txt"):
        """ Default constructor, check filename size is valid or note.
         if valid file name than it open file in write mode and write starter line of entry with utc time format.

         Parameters:
             logFile : text file for write log entry.

         Returns:
             No returns.

         Exceptions:
              raised exception while file file not created or appended.

        """
        if len(logFile) < 1:
            self.raisedException("Fix.__init__:  The file name violates the parameter specification.")

        try:
            txtFile = open(logFile, "w")
            timestamp = time.time()
            tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
            tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
            tmp3 = tmp2.astimezone()
            local = tmp3.replace(microsecond=0)

            self.txtFile = txtFile
            txtFile.write("LOG:\t" + str(local) + "\tStart of log\n")

        except ValueError as raisedException:
            raise (ValueError("Fix.__init__:  The Logfile can not be created or appended for whatever reasons."))


    def raiseException(self, msg):
        """ validate filename size if filename less than 1 than raise value error.

        Parameters:
             fileName: for validate filename.

        Returns:
            No returns.
        """
        raise (ValueError(msg))



    def setSightingFile(self, sightingFile):
        """ This method receive xml file as parameter.split it with . and validate file name.
        write message that sighting file start  with current datetime and filename.

        Parameters:
            sightingFile: xml data file.

        Returns:
            A string having the value passed as the sightingFile name.
        """
        if len(sightingFile.split(".")[0]) < 1:
            self.raisedException("Fix.setSightingFile:  The sighting file name violates the parameter specification.")

        timestamp = time.time()
        tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
        tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
        tmp3 = tmp2.astimezone()
        local = tmp3.replace(microsecond=0)

        self.txtFile.write("LOG:\t" + str(local) + "\tStart of sighting file\t" + sightingFile + "\n")
        self.sightingFile = sightingFile

        try:
            xmlFile = open(sightingFile, "r")
            xmlFile.close()
        except:
            self.raisedException("Fix.setSightingFile:  The sighting file not found or could not be opened.")

        return self.sightingFile

    def getSightings(self):
        """ Set default approximate Latitude and approximate Longitude to 0d0.0
        parse xml file using ElementTree and find all parents and childes tags from file.
        calculate approximate a geographical position and write calculation in text file with
        current date time.

        Parameters:
             No parameters.

        Returns:
             approximateLatitude and approximateLongitude.

        Exception:
             "No sighting file has been set" raised when parse xml file if file not set.
             "Some Tag are Missing" raised when any tag is empty.
        """
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        try:
            tree = ElementTree.parse(self.sightingFile)  # VALUE ERROR 1 OPENING FILE
        except :
            self.raisedException("Fix.getSightings:  No sighting file has been set.")

        sightings = tree.findall("sighting")

        try:
            self.calculate(sightings)
            self.txtFile.close()
            return (approximateLatitude, approximateLongitude)

        except:
            self.raisedException("Fix.getSightings:  Some Tag are Missing.")

    def calculate(self,sightings):
        """calculate approximate a geographical position using xml file data. validate tag values and set default
        value if some tags are empty.store all data in dictionary like tag name as key and tag value as value.

            Parameters:
                sightings: tag values.

            Returns :
                No returns.

            Exception:
                "Mandatory tag is missing" raised when some tags are empty.
                ValueError when observ degrees or minutes are invalid.

        """
        try:
            dataList = []

            for elem in sightings:
                dataDict = {}
                dataDict["body"] = elem[0].text
                dataDict["dt"] = elem[1].text
                dataDict["time"] = elem[2].text
                dataDict["observation"] = elem[3].text
                dataDict["height"] = elem[4].text
                dataDict["temperature"] = float(elem[5].text)
                dataDict["pressure"] = elem[6].text
                dataDict["horizon"] = elem[7].text

                newAngle = Angle.Angle()

                newAngle.setDegreesAndMinutes( dataDict["observation"])

                if newAngle.degrees < 0 or newAngle.degrees > 90:
                    raise (ValueError("observation:  Degrees are invalid"))
                elif newAngle.minutes < 0 or newAngle.minutes > 60:
                    raise (ValueError("observation:  Minutes are invalid"))
                elif  dataDict["height"] == "":
                     dataDict["height"] == 0
                elif  dataDict["temperature"] == "":
                     dataDict["temperature"] = 72
                elif  dataDict["pressure"] == "":
                     dataDict["pressure"] = 1010
                elif  dataDict["horizon"] == "":
                     dataDict["horizon"] == "Natural"

                dip = 0.0
                if  dataDict["horizon"].strip() == "Natural":
                    dip = (-0.97 * sqrt(float( dataDict["height"].strip()))) / 60.0

                celcius = ( dataDict["temperature"] - 32) * 5.0 / 9.0
                newAngle.setDegreesAndMinutes( dataDict["observation"].strip())
                altitude = newAngle.degrees + (newAngle.minutes / 60) % 360

                refraction = -0.00452 * float(dataDict["pressure"].strip()) / float(273 + celcius) / tan(radians(altitude))

                adjustedAltitude = altitude + dip + refraction
                newAngle.setDegrees(adjustedAltitude)

                dataDict['dttim'] = datetime.datetime.strptime(dataDict["dt"] + " " + dataDict["time"], "%Y-%m-%d %H:%M:%S")
                dataDict['degrees'] = newAngle.getString()
                dataList.append(dataDict)

            dataList.sort(key=lambda k: k['body'])
            dataList.sort(key=lambda k: k['dttim'])

            for dataDict in dataList:
                timestamp = time.time()
                tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
                tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
                tmp3 = tmp2.astimezone()
                local = tmp3.replace(microsecond=0)

                self.txtFile.write("LOG:\t" + str(local) + "\t" + dataDict["body"] + "\t" +  dataDict["dt"] + "\t" +  dataDict["time"] + "\t" + dataDict['degrees'] + "\n")

            self.txtFile.write("LOG:\t" + str(local) + "\tEnd of sighting file\t" + self.sightingFile)
            self.txtFile.close()

        except:
            self.raisedException("Fix.calculate:  Mandatory tag is missing or the information associated with a tag is invalid.")

if __name__ == "__main__":
    f = Fix()
    f.setSightingFile("sight.xml")
    f.getSightings()
