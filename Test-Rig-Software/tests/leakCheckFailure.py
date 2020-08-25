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
        if (time < self.statesStart['LEAK_CHECKING']):
            pressure = leakCheckSuccess.leakCheckSuccess.getHeliumPressurePtData(self, time)
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

class leakCheckOverpressLox(leakCheckSuccess.leakCheckSuccess):
    def testName(self):
        return "Leak check with Lox overpressurization"

    def getTestTime(self):
        return self.statesEnd['LEAK_CHECKING']

    def isTestFinished(self, time):
        if (time > getTestTime(time)):
            return True
        return False

    def getLoxPressurePtData(self, time):
        pressure = 0
        if (time < self.statesStart['LEAK_CHECKING']):
            pressure = leakCheckSuccess.leakCheckSuccess.getLoxPressurePtData(self, time)
        elif (self.getState(time) == "LEAK_CHECKING"):
            x = [
                self.statesStart['LEAK_CHECKING'],
                self.statesEnd['LEAK_CHECKING'],
                (self.statesEnd['LEAK_CHECKING'] - self.statesStart['LEAK_CHECKING'])/2 + self.statesStart['LEAK_CHECKING']
            ]
            y = [self.maxLOXPressure, self.maxLOXPressure*1.5, self.maxLOXPressure*1.5*.75]
            poly = np.polyfit(x, y, 5)
            pressure = round(np.polyval(poly, time))
        else:
            pressure = self.maxLOXPressure*1.5
        return pressure

class leakCheckOverpressEthanol(leakCheckSuccess.leakCheckSuccess):
    def testName(self):
        return "Leak check with Ethanol overpressurization"

    def getTestTime(self):
        return self.statesEnd['LEAK_CHECKING']

    def isTestFinished(self, time):
        if (time > getTestTime(time)):
            return True
        return False

    def getEthanolPressurePtData(self, time):
        pressure = 0
        if (time < self.statesStart['LEAK_CHECKING']):
            pressure = leakCheckSuccess.leakCheckSuccess.getEthanolPressurePtData(self, time)
        elif (self.getState(time) == "LEAK_CHECKING"):
            x = [
                self.statesStart['LEAK_CHECKING'],
                self.statesEnd['LEAK_CHECKING'],
                (self.statesEnd['LEAK_CHECKING'] - self.statesStart['LEAK_CHECKING'])/2 + self.statesStart['LEAK_CHECKING']
            ]
            y = [self.maxEthanolPressure, self.maxEthanolPressure*1.5, self.maxEthanolPressure*1.5*.75]
            poly = np.polyfit(x, y, 5)
            pressure = round(np.polyval(poly, time))
        else:
            pressure = self.maxEthanolPressure*1.5
        return pressure
