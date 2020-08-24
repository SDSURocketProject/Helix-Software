import tests.leakCheckSuccess as leakCheckSuccess
import numpy as np

class leakCheckOverpressHelium(leakCheckSuccess.leakCheckSuccess):
    def testName(self):
        return "Leak check with helium overpressurization"

    def getTestTime(self):
        return self.statesEnd['LEAK_CHECKING']

    def isTestFinished(self, time):
        if (time > getTestTime(time)):
            return True
        return False

    def getHeliumPressurePtData(self, time):
        pressure = 0
        if (self.getState(time) == "PRE_TEST"):
            pressure = 0
        elif (self.getState(time) == "PRESSURIZE"):
            x = [
                self.statesStart['PRESSURIZE'],
                self.statesEnd['PRESSURIZE'],
                self.statesLength['PRESSURIZE']*.5 + self.statesStart['PRESSURIZE']
            ]
            y = [0, self.maxHeliumPressure, self.maxHeliumPressure*.75]
            poly = np.polyfit(x, y, 5)
            pressure = round(np.polyval(poly, time))
            if pressure > self.maxHeliumPressure:
                pressure = self.maxHeliumPressure
        elif (self.getState(time) == "LEAK_CHECKING"):
            x = [
                self.statesStart['LEAK_CHECKING'],
                self.statesEnd['LEAK_CHECKING'],
                (self.statesEnd['LEAK_CHECKING'] - self.statesStart['LEAK_CHECKING'])/2 + self.statesStart['LEAK_CHECKING']
            ]
            y = [self.maxHeliumPressure, self.maxHeliumPressure*1.5, self.maxHeliumPressure*1.5*.75]
            poly = np.polyfit(x, y, 5)
            pressure = round(np.polyval(poly, time))
        else:
            pressure = self.maxHeliumPressure*1.5
        return pressure
