import math

class Angle():
    # Default constructor of Angle Class.
    # It initializes all the attributes.
    def __init__(self):
        # Set degrees and minutes to 0
        self.degrees = 0.0
        self.minutes = 0.0


    # setDegrees method receives parameter degrees as number.
    # It divides received degree into degrees and minutes.
    def setDegrees(self, degrees=0):
        try:
            # Check is degrees presented is in float or not
            degrees = float(degrees)
            # divide degrees and minutes using math.modf function
            frac, whole = math.modf(degrees)
            # set degrees
            self.degrees = whole
            # set minutes
            self.minutes = 60 * frac
            # return converted degrees and minutes with mod 360
            return (self.degrees + (self.minutes / 60)) % 360

        # handle error if value error raised
        except ValueError as raisedException:
            try:
                # convert degree presented in int
                degrees = int(degrees)
                # set degrees
                self.degrees = degrees
                # set minutes
                self.minutes = 0
                # return converted degrees and minutes with mod 360
                return (self.degrees) % 360

            # handle error if value error raised
            except ValueError as raisedException:
                raise (ValueError("Angle.setDegrees:  Received degrees is not a valid number"))
    
    # setDegreesAndMinutes method receives angleString of type string.
    # It splits string with separator "d" and sets degrees and minutes.
    def setDegreesAndMinutes(self, angleString):
        beforeD = None
        afterD = None
        # check received string is blank or not
        if angleString == "":
            raise ValueError("Angle.setDegreesAndMinutes:  angleString is blank.")

        # check separator exists or not
        elif "d" not in angleString:
            raise ValueError("Angle.setDegreesAndMinutes:  Seperator 'd' not found.")

        # string is valid then
        else:
            # spit string with separator
            angleString = angleString.split("d")
            # set variables by string parts
            beforeD = angleString[0]
            afterD = angleString[1]

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
            # if not convert
        except Exception as e:
            raise ValueError("Angle.setDegreesAndMinutes:  Invalid Minute part.")
        if afterD < 0:
            raise ValueError("Angle.setDegreesAndMinutes:  Negative Minute part.")

        # set variables
        self.degrees = beforeD
        self.minutes = afterD % 60
        # return degrees and minutes
        return self.degrees + (self.minutes / 60)

    # add method receives angle object.
    # It adds degrees and minutes to current angle.
    def add(self, angle):
        if not isinstance(angle, Angle):
            raise ValueError("Angle.add:  received angle is invalid.")
            
        # store string in data
        data = angle.getString()
        # split string with separator d
        data = data.split("d")
        # add degrees
        self.degrees += int(data[0])
        # add minutes
        self.minutes += float(data[1])
        # return degrees and minutes
        return (self.degrees + (self.minutes / 60)) % 360

    # subtract method receives angle object.
    # It subtracts degrees and minutes from current angle.
    def subtract(self, angle):
        if not isinstance (angle, Angle):
            raise ValueError("Angle.subtract:  received angle is invalid.")
            
        # store string in data
        data = angle.getString()
        # split string with separator d
        data = data.split("d")
        # subtract degrees
        self.degrees -= int(data[0])
        # subtract minutes
        self.minutes -= float(data[1])
        # return degrees and minutes
        return (self.degrees + (self.minutes / 60)) % 360

    # compare method compares received angle object with another.
    def compare(self, angle):
        if not isinstance (angle, Angle):
            raise ValueError("Angle.compare:  received angle is invalid.")

        if self.getDegrees() > angle.getDegrees():
            return 1
        elif self.getDegrees() < angle.getDegrees():
            return -1
        else:
            return 0
            
    # getString returns the string representation for this object.
    def getString(self):
        # convert degrees and minutes in string and return it
        self.degrees = int(self.degrees)
        return (str(self.degrees % 360) + "d" + str(round(self.minutes,1)))

    # getDegrees method returns degrees and minutes.
    def getDegrees(self):
        return (self.degrees + (round(self.minutes / 60,1))) % 360
