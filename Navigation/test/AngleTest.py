import unittest
import Navigation.prod.Angle as Angle


class AngleTest(unittest.TestCase):

    def setUp(self):
        self.delta = 0.002      # accuracy within 1/10 minute
        self.className = "Angle."
    def tearDown(self):
        pass

#    Acceptance Test: 100
#        Analysis - Contructor
#            inputs
#                none
#            outputs
#                instance of Angle
#            state change
#                value is set to 0d0
#
#            Happy path
#                nominal case:  Angle()
#            Sad path
#                none*
#
#               *if we _really_ wanted to be complete, we would test for presence of a parm
#
#    Happy path
    def test100_010_ShouldCreateInstanceOfAngle(self):
        self.assertIsInstance(Angle.Angle(), Angle.Angle)
        # note:   At this point, we don't any way of verifying the value of the angle.
        #         We'll be able to so when we construct tests for the getters

#-----------------------------------------------------------------
#    Acceptance Test: 200
#        Analysis - setDegrees
#            inputs
#                degrees expressed as an integer or float.  Optional
#            outputs
#                a floating point number representing degrees, modulo 360
#            state change
#                the value is stored in the instance
#
#            Happy path
#                nominal case for float:  setDegrees(10 + 32.5/60)  10d32.5
#                nominal case for int:  setDegrees(10)
#                nominal case for positive modulo:  setDegrees(400)
#                nominal case for negative modulo:  setDegrees(-400.1)
#                nominal case for default:  setDegrees()
#            Sad path
#                degrees
#                    not (int or float):  setDegrees("abc")
#
#    Happy path
    def test200_010_ShouldReturnFloat(self):
        anAngle = Angle.Angle()
        self.assertIsInstance(anAngle.setDegrees(10), float)
        
    def test200_010_ShouldSetAngleUsingDegreesDefault(self):
        anAngle = Angle.Angle()
        self.assertAlmostEquals(0.0, anAngle.setDegrees(), delta=self.delta)
        
    def test200_020_ShouldSetAngleUsingDegreesNominalInt(self):
        anAngle = Angle.Angle()
        self.assertAlmostEquals(10.0, anAngle.setDegrees(10), delta = self.delta)
        
    def test200_030_ShouldSetAngleUsingDegreesNominalFloat(self):
        anAngle = Angle.Angle()
        self.assertAlmostEquals(10.5416667, anAngle.setDegrees(10.0 + 32.5/60), delta=self.delta)
        
    def test200_040_ShouldSetAngleUsingDegreesNominalPositiveModulo(self):
        anAngle = Angle.Angle()
        self.assertAlmostEquals(40.0, anAngle.setDegrees(400), delta=self.delta)
        
    def test200_050_ShouldSetAngleUsingDegreesNominalNegativeModulo(self):
        anAngle = Angle.Angle()
        self.assertAlmostEquals(319.9, anAngle.setDegrees(-400.1), delta=self.delta)
        
#     SadPath
    def test200_910_ShouldRaiseExceptionOnNonIntNonFloatDegrees(self):
        expectedDiag = self.className + "setDegrees:"
        anAngle = Angle.Angle()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegrees("abc")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 

#-----------------------------------------------------------------
#    Acceptance Test: 300
#        Analysis - getDegrees
#            inputs
#                none
#            outputs
#                a floating point number representing degrees, modulo 360, rounded to nearest 1/10 minute.
#            state change
#                none
#
#            Happy path
#                nominal case: getDegrees() for an angle within 360 degrees, no rounding
#                nominal case: getDegrees() for an angle within 360 degrees, rounded
#                nominal case: getDegrees() for >360 angle, rounded
#                nominal case: getDegrees() for negative angle rounded
#                nominal case: getDegrees() for 360 angle.
#            Sad path
#                none*
#
#    Happy path
    def test300_010_ShouldReturnFloat(self):
        anAngle = Angle.Angle()
        anAngle.setDegrees(5)
        self.assertIsInstance(anAngle.getDegrees(), float)
        
    def test300_020_ShouldReturnDegreesWithNoRounding(self):
        anAngle = Angle.Angle()
        anAngle.setDegrees(30.5)
        self.assertEquals(30.5, anAngle.getDegrees())
        
    def test300_030_ShouldReturnDegreesWithRounding(self):
        anAngle = Angle.Angle()
        anAngle.setDegrees(0 + 10.46/60.0)
        self.assertAlmostEquals(10.5/60.0, anAngle.getDegrees(),places=4)  
        
    def test300_040_ShouldReturnModuloDegreesWithRounding(self):         
        anAngle = Angle.Angle()
        anAngle.setDegrees(360 + 10.46/60.0)
        self.assertAlmostEquals(10.5/60.0, anAngle.getDegrees(),places=4) 
        
    def test300_050_ShouldReturnModuloNegativeDegreesWithRounding(self):         
        anAngle = Angle.Angle()
        anAngle.setDegrees(-10.44/60.0)    #359d49.56 = 359d49.6 = 359.826667
        self.assertAlmostEquals(359.826667, anAngle.getDegrees(),places=4)  
           
    def test300_060_ShouldReturnModuloOfBoundaryCase(self):         
        anAngle = Angle.Angle()
        anAngle.setDegrees(360.0*2)
        self.assertEquals(0, anAngle.getDegrees())      

#-----------------------------------------------------------------
#    Acceptance Test: 400
#        Analysis - setDegreesAndMinutes
#            inputs
#                angleString: string in form of xdy.y
#                    x is integer  
#                    d is a literal
#                    y.y can be either integer or float with one decimal
#            outputs
#                a floating point number representing degrees, modulo 360
#            state change
#                value is stored
#
#            Happy path
#                nominal case for xdy.y:  setDegreesAndMinutes("10d5.5")
#                nominal case for xdy:    setDegreesAndMinutes("10d30")
#                nominal case for x>360:    setDegreesAndMinutes("400d0.0")
#                nominal case for x<0:    setDegreesAndMinutes("-20d10.5")
#                nominal case for x<-360:    setDegreesAndMinutes("-700d0.0")
#                nominal case for boundary:    setDegreesAndMinutes("360d0.0")
#                nominal case for y.y > 60:    setDegreesAndMinutes("0d61")
#            Sad path
#                x portion
#                    missing x:    setDegressAndMinutes("d10.0")
#                    non-integer x:  setDegreesAndMinutes("1.1d0.0")
#                d portion
#                    missing d:  setDegreesAndMinutes("10")
#                y.y
#                    too many decimals y:  setDegreesAndMinutes("10d5.55")
#                    negative y:  setDegreesAndMinutes("10d-10.0")
#                    non-integer y:  setDegreesAndMinutes("10da")
#                    missing y:    setDegreesAndMinutes("10d")
#    Happy path 
    def test400_010_ShouldReturnFloat(self):
        anAngle = Angle.Angle()
        self.assertIsInstance(anAngle.setDegreesAndMinutes("0d0"), float)  
        
    def test400_020_ShouldSetAngleWithValidXDYY(self):
        anAngle = Angle.Angle()
        inputOutput = ["10d5.5", 10 + 5.5/60]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1])    
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees())     
            
    def test400_030_ShouldSetAngleWithValidXDY(self):
        anAngle = Angle.Angle()
        inputOutput = ["10d5", 10 + 5.0/60]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1]) 
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees())  
        
    def test400_040_ShouldSetAngleWithValidXYYOver360(self):
        anAngle = Angle.Angle()
        inputOutput = ["400d0.0", 400.0%360.0]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1])   
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees())                           
         
    def test400_050_ShouldSetAngleWithValidNegXYY(self):
        anAngle = Angle.Angle()
        inputOutput = ["-20d10.5", 360.0-(20.0 + 10.5/60.0)]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1]) 
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees()) 
        
    def test400_060_ShouldSetAngleWithValidNegXYYOver360(self):
        anAngle = Angle.Angle()
        inputOutput = ["-700d0.0",-700.0%360.0]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1])   
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees())  
        
    def test400_070_ShouldSetAngleOnBoundary(self):
        anAngle = Angle.Angle()
        inputOutput = ["360d0.0",0.0]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1]) 
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees())    
        
    def test400_070_ShouldSetAngleWithValid0YY(self):
        anAngle = Angle.Angle()
        inputOutput = ["0d10.5",10.5/60.0]
        self.assertAlmostEquals(anAngle.setDegreesAndMinutes(inputOutput[0]), inputOutput[1])  
        self.assertAlmostEquals(inputOutput[1], anAngle.getDegrees())    
        
#   Sad path
    def test400_910_ShouldRaiseExceptionOnMissingDegrees(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("d10.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())    
   
    def test400_920_ShouldRaiseExceptionOnNonintegerDegrees(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("1.1d10.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())   
   
    def test400_930_ShouldRaiseExceptionOnMissingD(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("11.5")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())                   
    
    def test400_940_ShouldRaiseExceptionOn2DecimalY(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("10d5.55")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())  
    
    def test400_950_ShouldRaiseExceptionOnNegativeY(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("10d-10.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())  
                      
    def test400_960_ShouldRaiseExceptionOnNonintegerY(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("10da")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())  
    
    def test400_970_ShouldRaiseExceptionOnMissingY(self):
        expectedDiag = self.className + "setDegreesAndMinutes:"
        anAngle = Angle.Angle()
        originalValue = anAngle.getDegrees()
        with self.assertRaises(ValueError) as context:
            anAngle.setDegreesAndMinutes("10d")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        self.assertAlmostEquals(originalValue, anAngle.getDegrees())  


#-----------------------------------------------------------------
#    Acceptance Test: 500
#        Analysis - add
#            inputs
#                instance of angle
#            outputs
#                a floating point number representing degrees, modulo 360
#            state change
#                sum is stored in instance
#            Happy path
#                nominal case:  add(istanceOfAngle) returns angle <360
#                nominal case:  add(instanceOfAngle) returns angle = 360
#                nominal case:  add(instanceOfAngle) returns an
#            Sad path
#                missing parm:   add()
#                non-angle parm: add(notAnInstanceOfAngle)  retains state
#
#    Happy path 

    def test500_010_ShouldReturnFloat(self):
        angle1 = Angle.Angle()
        angle2 = Angle.Angle()
        angle2.setDegrees(10)
        self.assertIsInstance(angle1.add(angle2), float)  

    def test500_020_ShouldReturnTotalLessThan360(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(10)
        angle2 = Angle.Angle()
        angle2.setDegrees(10)
        self.assertEquals(20.0, angle1.add(angle2))
        self.assertEquals(20.0, angle1.getDegrees())         

    def test500_030_ShouldReturnTotalEqual0(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(359.5)
        angle2 = Angle.Angle()
        angle2.setDegrees(0.5)
        self.assertEquals(0.0, angle1.add(angle2))
        self.assertEquals(0.0, angle1.getDegrees())
        
    def test500_040_ShouldReturnModulo360(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(200)
        angle2 = Angle.Angle()
        angle2.setDegrees(180)
        self.assertEquals(20.0, angle1.add(angle2))
        self.assertEquals(20.0, angle1.getDegrees())       

#   Sad path
    def test500_910_ShouldRaiseExceptionOnMissingPam(self):
        expectedDiag = self.className + "add:"
        anAngle = Angle.Angle()
        anAngle.setDegrees(42.0)
        with self.assertRaises(ValueError) as context:
            anAngle.add()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        self.assertEquals(42.0, anAngle.getDegrees())
   
    def test500_920_ShouldRaiseExceptionOnNonangleParm(self):
        expectedDiag = self.className + "add:"
        anAngle = Angle.Angle()
        anAngle.setDegrees(100.0)
        with self.assertRaises(ValueError) as context:
            anAngle.add(5)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        self.assertEquals(100.0, anAngle.getDegrees())



#-----------------------------------------------------------------
#    Acceptance Test: 600
#        Analysis - subtract
#            inputs
#                instance of angle
#            outputs
#                a floating point number representing degrees, modulo 360
#            state change
#                difference is stored in instance
#
#            Happy path
#                nominal case:  subtract(istanceOfAngle) returns angle >0 and < 360
#                nominal case:  subtract(instanceOfAngle) returns angle = 0 
#                nominal case:  add(instanceOfAngle) returns angle < 0
#            Sad path
#                missing parm:   subtract()
#                nonAngle parm:  subtract(notAnInstanceOfAngle)
#    Happy path 

    def test600_010_ShouldReturnFloat(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(30.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(20.0)
        self.assertIsInstance(angle1.subtract(angle2), float)  

    def test600_020_ShouldReturnTotalBetween0And360(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(30.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(20.0)
        self.assertEquals(10.0, angle1.subtract(angle2))
        self.assertEquals(10.0, angle1.getDegrees())         

    def test600_030_ShouldReturnTotalEqual0(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(540.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(180.0)
        self.assertEquals(0.0, angle1.subtract(angle2))
        self.assertEquals(0.0, angle1.getDegrees())
        
    def test600_040_ShouldReturnModulo360WhenNegative(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(0.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(0.5)
        self.assertEquals(359.5, angle1.subtract(angle2))
        self.assertEquals(359.5, angle1.getDegrees())       

#   Sad path
    def test600_910_ShouldRaiseExceptionOnMissingPam(self):
        expectedDiag = self.className + "subtract:"
        originalValue = 42.0
        anAngle = Angle.Angle()
        anAngle.setDegrees(originalValue)
        with self.assertRaises(ValueError) as context:
            anAngle.subtract()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        self.assertEquals(originalValue, anAngle.getDegrees())
   
    def test600_920_ShouldRaiseExceptionOnNonangleParm(self):
        expectedDiag = self.className + "subtract:"
        originalValue = 100.0
        anAngle = Angle.Angle()
        anAngle.setDegrees(originalValue)
        with self.assertRaises(ValueError) as context:
            anAngle.subtract(5)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        self.assertEquals(originalValue, anAngle.getDegrees())


#-----------------------------------------------------------------
#    Acceptance Test: 700
#        Analysis - compare
#            inputs
#                instance of angle
#            outputs
#                an integer
#
#            Happy path
#                nominal case:  compare one angle to another and return integer
#                nominal case:  compare one instance with smaller angle and return 1
#                nominal case:  compare one instance with an equal angle and return 0 
#                nominal case:  acompare one instance with a larger angle and return -1
#            Sad path
#                missing parm:   compare()
#                nonAngle parm:  compare(notAnInstanceOfAngle)
#                

#    Happy path 

    def test700_010_ShouldReturnInteger(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(30.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(20.0)
        self.assertIsInstance(angle1.compare(angle2), int)  

    def test700_020_ShouldCompareWithSmallerAngle(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(30.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(20.0)
        self.assertEquals(1, angle1.compare(angle2))       

    def test700_030_ShouldCompareWithEqualAngle(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(-10.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(350.0)
        self.assertEquals(0, angle1.compare(angle2))
        
    def test700_040_ShouldCompareWithLargerAngle(self):
        angle1 = Angle.Angle()
        angle1.setDegrees(0.0)
        angle2 = Angle.Angle()
        angle2.setDegrees(0.5)
        self.assertEquals(-1, angle1.compare(angle2))     

#   Sad path
    def test700_910_ShouldRaiseExceptionOnMissingPam(self):
        expectedDiag = self.className + "compare:"
        originalValue = 42.0
        anAngle = Angle.Angle()
        anAngle.setDegrees(originalValue)
        with self.assertRaises(ValueError) as context:
            anAngle.compare()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        self.assertEquals(originalValue, anAngle.getDegrees())
   
    def test700_920_ShouldRaiseExceptionOnNonangleParm(self):
        expectedDiag = self.className + "compare:"
        originalValue = 100.0
        anAngle = Angle.Angle()
        anAngle.setDegrees(originalValue)
        with self.assertRaises(ValueError) as context:
            anAngle.compare(5)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        self.assertEquals(originalValue, anAngle.getDegrees())


#-----------------------------------------------------------------
#    Acceptance Test: 800
#        Analysis - getString
#            inputs
#                instance of angle
#            outputs
#                a string
#
#            Happy path
#                nominal case:  return a string
#                nominal case:  return a string in format xdyy.y for a valid angle, no rounding
#                noninal case:  return a string in format xdyy.y for a valid angle, with rounding
#            Sad path
#                none*
#                
#    Happy path 

    def test800_010_ShouldReturnString(self):
        anAngle = Angle.Angle()
        self.assertIsInstance(anAngle.getString(), str)  

    def test700_020_ShouldReturnMDYYYNoRounding(self):
        anAngle = Angle.Angle()
        anAngle.setDegrees(30.5)
        self.assertEquals("30d30.0", anAngle.getString()) 

    def test700_030_ShouldReturnMDYYYRounded(self):
        anAngle = Angle.Angle()
        anAngle.setDegrees(10.46/60.0)
        self.assertEquals("0d10.5", anAngle.getString()) 





