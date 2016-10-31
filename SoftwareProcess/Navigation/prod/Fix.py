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
        self.errors = 0
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
            txtFile = open(logFile, "a")
            timestamp = time.time()
            tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
            tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
            tmp3 = tmp2.astimezone()
            local = tmp3.replace(microsecond=0)

            self.txtFile = txtFile
            self.txtFile.write("LOG: " + str(local) + " Log file:\t" + os.path.realpath(logFile) + "\n")

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

        self.sightingFile = sightingFile
        self.txtFile.write("LOG: " + str(local) + " Sighting file\t" +os.path.realpath(self.sightingFile) + "\n")

        try:
            xmlFile = open(sightingFile, "r")
            xmlFile.close()
        except:
            self.raisedException("Fix.setSightingFile:  The sighting file not found or could not be opened.")

        return os.path.realpath(self.sightingFile)

    def setAriesFile(self, ariesFile):
        """ setAriesFile method receive text file as parameter. split it with '.' and validate file name.
            write in log.txt file that filename and full path of aries file  with current datetime.

            Parameters:
                ariesFile: aries data file.

            Returns:
                A string having the value passed as the ariesFile's full path.
            """
        actualFileName = ariesFile.split(".")[0]

        if (len(actualFileName)) < 1:
            raise (ValueError("Fix.setAriesFile:  Received Filename is invalid"))

        timestamp = time.time()
        tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
        tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
        tmp3 = tmp2.astimezone()
        local = tmp3.replace(microsecond=0)

        self.ariesFile = actualFileName + ".txt"

        try:
            f = open(self.ariesFile, "r")
            f.close()
        except Exception as e:
            raise (ValueError("Fix.setAriesFile:  Aries file could not be opened"))

        self.txtFile.write("LOG: " + str(local) + " Aries file:\t" + os.path.realpath(self.ariesFile) + " \n")

        return os.path.realpath(self.ariesFile)

    def setStarFile(self, starFile):
        """ setStarFile method receive text file as parameter. split it with '.' and validate file name.
            write in log.txt file that filename and full path of stars file  with current datetime.

            Parameters:
                starFile: stars data file.

            Returns:
                A string having the value passed as the starsFile's full path.
            """
        actualFileName = starFile.split(".")[0]

        if (len(actualFileName)) < 1:
            raise (ValueError("Fix.setStarFile:  Received Filename is invalid"))
        timestamp = time.time()
        tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
        tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
        tmp3 = tmp2.astimezone()
        local = tmp3.replace(microsecond=0)

        self.starFile = actualFileName + ".txt"
        self.txtFile.write("LOG: " + str(local) + " Star file:\t" + os.path.realpath(self.starFile) + " \n")

        try:
            f = open(self.starFile, "r")
            f.close()
        except Exception as e:
            raise (ValueError("Fix.setStarFile:  Stars file could not be opened"))

        return os.path.realpath(self.starFile)

    def getSightings(self):
        """ Set default approximate Latitude and approximate Longitude to 0d0.0
        parse xml file using ElementTree and find all parents and childes tags from file.
        calculate approximate a geographical position, latitude and longitude. write calculation in text file with
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
        self.errorString = ""
        try:
            self.calculate(sightings)
            self.txtFile.close()
            return (approximateLatitude, approximateLongitude)

        except:
            self.raisedException("Fix.getSightings:  Some Tag are Missing.")

    def calculate(self,sightings):
        """calculate approximate a geographical position using xml file data. validate tag values and set default
        value if some tags are empty.calculate latitude and longitude using stars file and aries file.store all data
        in dictionary like tag name as key and tag value as value.

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

                newAngle.setDegreesAndMinutes( dataDict["observation"])

                if newAngle.degrees < 0 or newAngle.degrees > 90:
                    raise (ValueError("observation:  Degrees are invalid"))
                elif newAngle.minutes < 0 or newAngle.minutes > 60:
                    raise (ValueError("observation:  Minutes are invalid"))

                dip = 0.0
                if  dataDict["horizon"].strip() == "Natural":
                    dip = (-0.97 * sqrt(float( dataDict["height"].strip()))) / 60.0

                celcius = ( dataDict["temperature"] - 32) * 5.0 / 9.0
                newAngle.setDegreesAndMinutes( dataDict["observation"].strip())
                altitude = newAngle.degrees + (newAngle.minutes / 60) % 360

                refraction = -0.00452 * float(dataDict["pressure"].strip()) / float(273 + celcius) / tan(radians(altitude))

                adjustedAltitude = altitude + dip + refraction
                newAngle.setDegrees(adjustedAltitude)

                hours = dataDict["time"].split(":")[0]
                minutes = dataDict["time"].split(":")[1]
                seconds = dataDict["time"].split(":")[2]

                s = (int(minutes) * 60) + int(seconds)
                formatedDate = datetime.datetime.strptime(dataDict["dt"], '%Y-%m-%d').strftime('%m/%d/%y')

                angleObj = Angle.Angle()
                flag = False
                with open(self.starFile, 'r+') as starFile:
                    for line in starFile:
                        name = line.split("\t")[0]
                        tempDt = line.split("\t")[1]
                        if name == dataDict["body"] and tempDt == formatedDate:
                            self.SHAstar = angleObj.setDegreesAndMinutes(line.split("\t")[2])
                            self.latitude = (line.split("\t")[3]).strip()
                            flag = True

                    if(not flag):
                        self.errors += 1
                        self.errorString += "Name or date not Found"
                        continue

                angleObj1 = Angle.Angle()
                angleObj2 = Angle.Angle()

                with open(self.ariesFile, 'r+') as ariesFile:
                    for line in ariesFile:
                        tempDate = line.split("\t")[0]
                        tempHour = line.split("\t")[1]

                        hours = int(hours)
                        tempHour = int(tempHour)
                        if tempDate == formatedDate and tempHour == hours:
                            self.GHAaries1 = angleObj1.setDegreesAndMinutes(line.split("\t")[2])
                            nextObj = next(ariesFile).split("\t")[2]
                            self.GHAaries2 = angleObj2.setDegreesAndMinutes(nextObj)


                self.GHAaries = self.GHAaries1 + (self.GHAaries2 - self.GHAaries1) * (s / 3600)
                self.GHAobservation = self.GHAaries + self.SHAstar

                angle = Angle.Angle()
                angle.setDegrees(self.GHAobservation)
                self.GHAobservation = angle.getString()

                dataDict['dttim'] = datetime.datetime.strptime(dataDict["dt"] + " " + dataDict["time"], "%Y-%m-%d %H:%M:%S")
                dataDict['degrees'] = newAngle.getString()
                dataDict['latitude'] = self.latitude
                dataDict['longitude'] = self.GHAobservation
                dataList.append(dataDict)

            dataList.sort(key=lambda k: k['body'])
            dataList.sort(key=lambda k: k['dttim'])

            for dataDict in dataList:
                timestamp = time.time()
                tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
                tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
                tmp3 = tmp2.astimezone()
                local = tmp3.replace(microsecond=0)

                self.txtFile.write("LOG: " + str(local) + " " + dataDict["body"] + "\t" +  dataDict["dt"] + "\t" +  dataDict["time"] + "\t" + dataDict['degrees'] + "\t" + dataDict['latitude'] + "\t" + dataDict['longitude'] + "\n")
        except:
            self.raisedException("Fix.calculate:  Mandatory tag is missing or the information associated with a tag is invalid.")

        finally:
            timestamp = time.time()
            tmp1 = datetime.datetime.utcfromtimestamp(timestamp)
            tmp2 = tmp1.replace(tzinfo=datetime.timezone.utc)
            tmp3 = tmp2.astimezone()
            local = tmp3.replace(microsecond=0)
            print(self.errorString)
            self.txtFile.write("LOG: " + str(local) + " Sighting errors:" + "\t" + str(self.errors) + "\n")
            self.txtFile.close()



if __name__ == "__main__":
    f = Fix()
    f.setSightingFile("sight.xml")
    f.setAriesFile("aries.txt")
    f.setStarFile("stars.txt")
    f.getSightings()
