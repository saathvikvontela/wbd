import math

class Angle():
    """Angle class to handle an angle representing degrees and minutes."""
    
    def __init__(self):
        """Constructor"""

        self.degrees = 0.0
        self.minutes = 0.0
        self.originalDegree = 0

    def setDegrees(self, degrees=0.0):
        """Sets degrees and minutes using received float value"""
        try:
            self.minutes, self.degrees = math.modf(float(degrees))
        except Exception as e:
            try:
                self.degrees, self.minutes = int(degrees), 0
            except Exception as e:
                raise ValueError("Angle.setDegrees:  Invalid degrees.")

        temp = float((self.degrees % 360) + self.minutes) % 360
        self.minutes, self.degrees = math.modf(temp)
        return temp
        
    # setDegreesAndMinutes method receives angleString of type string.
    # It splits string with separator "d" and sets degrees and minutes.
    def setDegreesAndMinutes(self, angleString):
        """Sets degrees and minutes using received string value"""
        
        beforeD = None
        afterD = None
        self.originalDegree = 0
        self.isMinus = False
        
        # check received string is blank or not
        if angleString == "":
            raise ValueError("Angle.setDegreesAndMinutes:  angleString is blank.")

        # check separator exists or not
        elif "d" not in angleString:
            raise ValueError("Angle.setDegreesAndMinutes:  Seperator 'd' not found.")

        # spit string with separator
        degreesAndMinutes = angleString.split("d")

        if len(degreesAndMinutes) != 2:
            raise ValueError("Angle.setDegreesAndMinutes:  Invalid angleString.")

        elif "." in degreesAndMinutes[0]:
            raise ValueError("Angle.setDegreesAndMinutes:  Invalid Degrees in angleString.")

        # string is valid then
        else:
            # set variables by string parts
            beforeD = degreesAndMinutes[0]
            afterD = degreesAndMinutes[1]

        # Validate beforeD part.
        try:
            # convert variable to integer
            beforeD = int(beforeD)
        except Exception as e:
            raise ValueError("Angle.setDegreesAndMinutes:  Invalid Degree part.")

        # Validate afterD part.
        try:
            # convert variable to float
            afterD = float(afterD)
        except Exception as e:
            raise ValueError("Angle.setDegreesAndMinutes:  Invalid Minute part.")

        if afterD < 0:
            raise ValueError("Angle.setDegreesAndMinutes:  Negative Minute part.")

        if len(str(afterD).split(".")[1]) > 1:
            raise ValueError("Angle.setDegreesAndMinutes:  Invalid Minutes part.")

        self.originalDegree = beforeD
        if beforeD < 0:
            beforeD = 360 - beforeD - (int(afterD % 60) if afterD > 60 else 0)

        self.degrees = (beforeD + (int(afterD % 60) if afterD > 60 else 0)) % 360
        self.minutes = (afterD % 60) / 60

        temp = float(self.degrees + self.minutes)
        if self.originalDegree < 0:
            return (360 - temp)
        else:
            return temp


    def add(self, angle=None):
        """Adds degrees and minutes to current object from received object"""
        
        if not isinstance(angle, Angle):
            raise ValueError("Angle.add:  received angle is invalid.")

        if angle.originalDegree < 0:
            data = (float(self.degrees + self.minutes) - float(angle.degrees + angle.minutes)) % 360
        else:
            data = (float(self.degrees + self.minutes) + float(angle.degrees + angle.minutes)) % 360

        self.minutes, self.degrees = math.modf(data)
        return data

    def subtract(self, angle=None):
        """Subtracts degrees and minutes from current object from received object"""
        
        if not isinstance (angle, Angle):
            raise ValueError("Angle.subtract:  received angle is invalid.")

        if angle.originalDegree < 0:
            data = (float(self.degrees + self.minutes) + float(angle.degrees + angle.minutes)) % 360
        else:
            data = (float(self.degrees + self.minutes) - float(angle.degrees + angle.minutes)) % 360

        self.minutes, self.degrees = math.modf(data)
        return data

    # compare method compares received angle object with another.
    def compare(self, angle=None):
        """Compares current object with received object"""
        
        if not isinstance (angle, Angle):
            raise ValueError("Angle.compare:  received angle is invalid.")

        if self.getDegrees() > angle.getDegrees():
            return 1
        elif self.getDegrees() < angle.getDegrees():
            return -1
        else:
            return 0
            
    def getString(self):
        """Returns string representation of this object"""
        
        self.degrees = int(self.degrees)
        return str(self.degrees) + "d" + str(round(self.minutes * 60, 1))

    def getDegrees(self):
        """Returns degrees as a floating point number"""
        
        degreesAndMinutes = (float(self.degrees + round(self.minutes * 60.0, 1) / 60.0)) % 360
        
        return ((360 - degreesAndMinutes) if self.originalDegree < 0 else degreesAndMinutes)
        
