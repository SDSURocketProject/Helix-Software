import tests.testTemplate as testTemplate
import numpy as np
import warnings

class leakCheckSuccess(testTemplate.testTemplate):
    def __init__(self):
        statesEndTimes = {
            "PRE_TEST":10,
            "PRESSURIZE":20,
            "LEAK_CHECKING":40,
            "DE_PRESSURIZE":50,
            "POST_TEST":60
        }
        statesStartTimes = {
            "PRE_TEST":0,
            "PRESSURIZE":statesEndTimes['PRE_TEST'],
            "LEAK_CHECKING":statesEndTimes['PRESSURIZE'],
            "DE_PRESSURIZE":statesEndTimes['LEAK_CHECKING'],
            "POST_TEST":statesEndTimes['DE_PRESSURIZE']
        }
        statesLengthTimes = {
            "PRE_TEST":statesEndTimes['PRE_TEST'] - statesStartTimes['PRE_TEST'],
            "PRESSURIZE":statesEndTimes['PRESSURIZE'] - statesStartTimes['PRESSURIZE'],
            "LEAK_CHECKING":statesEndTimes['LEAK_CHECKING'] - statesStartTimes['LEAK_CHECKING'],
            "DE_PRESSURIZE":statesEndTimes['DE_PRESSURIZE'] - statesStartTimes['DE_PRESSURIZE'],
            "POST_TEST":statesEndTimes['POST_TEST'] - statesStartTimes['POST_TEST']
        }

        self.statesEnd = statesEndTimes
        self.statesStart = statesStartTimes
        self.statesLength = statesLengthTimes
        self.maxHeliumPressure = 100
        self.maxLOXPressure = 100
        self.maxEthanolPressure = 100
        self.minLOXTemperature = -180
        self.minEthanolTemperature = 0
        warnings.simplefilter('ignore', np.RankWarning)

    def testName(self):
        return "Leak Check Success"

    def getTestTime(self):
        return self.statesEnd['POST_TEST']

    def isTestFinished(self, time):
        if (self.isTestFinished or getState(time) == "FINISHED"):
            return True
        return False

    def getState(self, time):
        if (time < 0):
            return "NOT_STARTED"
        elif (time < self.statesEnd['PRE_TEST']):
            return "PRE_TEST"
        elif (time < self.statesEnd['PRESSURIZE']):
            return "PRESSURIZE"
        elif (time < self.statesEnd['LEAK_CHECKING']):
            return "LEAK_CHECKING"
        elif (time < self.statesEnd['DE_PRESSURIZE']):
            return "DE_PRESSURIZE"
        elif (time < self.statesEnd['POST_TEST']):
            return "POST_TEST"
        else:
            return "FINISHED"

    def getHeliumPressurePtData(self, time):
        pressure = 0
        if (self.getState(time) == "PRE_TEST"):
            pressure = 0
        elif (self.getState(time) == "PRESSURIZE"):
            x = [
                self.statesStart['PRESSURIZE'],
                self.statesEnd['PRESSURIZE'],
                self.statesLength['PRESSURIZE']*0.5 + self.statesStart['PRESSURIZE']
            ]
            y = [0, self.maxHeliumPressure, self.maxHeliumPressure*.75]
            poly = np.polyfit(x, y, 2)
            pressure = round(np.polyval(poly, time))
        elif (self.getState(time) == "LEAK_CHECKING"):
            pressure = self.maxHeliumPressure
        elif (self.getState(time) == "DE_PRESSURIZE"):
            x = [
                self.statesStart['DE_PRESSURIZE'],
                self.statesEnd['DE_PRESSURIZE'],
                self.statesLength['DE_PRESSURIZE']*0.5 + self.statesStart['DE_PRESSURIZE']
            ]
            y = [self.maxHeliumPressure, 0, self.maxHeliumPressure*.25]
            poly = np.polyfit(x, y, 2)
            pressure = round(np.polyval(poly, time))
        elif (self.getState(time) == "POST_TEST"):
            pressure = 0
        
        if pressure > self.maxHeliumPressure:
            pressure = self.maxHeliumPressure
        return pressure

    def getLoxPressurePtData(self, time):
        pressure = 0
        if (self.getState(time) == "PRE_TEST"):
            pressure = 0
        elif (self.getState(time) == "PRESSURIZE"):
            x = [
                self.statesStart['PRESSURIZE'],
                self.statesEnd['PRESSURIZE'],
                self.statesLength['PRESSURIZE']*0.5 + self.statesStart['PRESSURIZE']
            ]
            y = [0, self.maxLOXPressure, self.maxLOXPressure*.75]
            poly = np.polyfit(x, y, 2)
            pressure = round(np.polyval(poly, time))
        elif (self.getState(time) == "LEAK_CHECKING"):
            pressure = self.maxLOXPressure
        elif (self.getState(time) == "DE_PRESSURIZE"):
            x = [
                self.statesStart['DE_PRESSURIZE'],
                self.statesEnd['DE_PRESSURIZE'],
                self.statesLength['DE_PRESSURIZE']*0.5 + self.statesStart['DE_PRESSURIZE']
            ]
            y = [self.maxLOXPressure, 0, self.maxLOXPressure*.25]
            poly = np.polyfit(x, y, 2)
            pressure = round(np.polyval(poly, time))
        elif (self.getState(time) == "POST_TEST"):
            pressure = 0
        
        if pressure > self.maxLOXPressure:
            pressure = self.maxLOXPressure
        return pressure

    def getEthanolPressurePtData(self, time):
        pressure = 0
        if (self.getState(time) == "PRE_TEST"):
            pressure = 0
        elif (self.getState(time) == "PRESSURIZE"):
            x = [
                self.statesStart['PRESSURIZE'],
                self.statesEnd['PRESSURIZE'],
                self.statesLength['PRESSURIZE']*0.5 + self.statesStart['PRESSURIZE']
            ]
            y = [0, self.maxEthanolPressure, self.maxEthanolPressure*.75]
            poly = np.polyfit(x, y, 2)
            pressure = round(np.polyval(poly, time))
        elif (self.getState(time) == "LEAK_CHECKING"):
            pressure = self.maxEthanolPressure
        elif (self.getState(time) == "DE_PRESSURIZE"):
            x = [
                self.statesStart['DE_PRESSURIZE'],
                self.statesEnd['DE_PRESSURIZE'],
                self.statesLength['DE_PRESSURIZE']*0.5 + self.statesStart['DE_PRESSURIZE']
            ]
            y = [self.maxEthanolPressure, 0, self.maxEthanolPressure*.25]
            poly = np.polyfit(x, y, 2)
            pressure = round(np.polyval(poly, time))
        elif (self.getState(time) == "POST_TEST"):
            pressure = 0
        
        if pressure > self.maxEthanolPressure:
            pressure = self.maxEthanolPressure
        return pressure

    def getHeliumFillValveHallEffectState(self, time):
        if (time > self.statesStart['DE_PRESSURIZE'] and time < self.statesEnd['DE_PRESSURIZE']):
            return 1
        return 0

    def getLoxFillValveHallEffectState(self, time):
        if (time > self.statesStart['DE_PRESSURIZE'] and time < self.statesEnd['DE_PRESSURIZE']):
            return 1
        return 0

    def getEthanolFillValveHallEffectState(self, time):
        if (time > self.statesStart['DE_PRESSURIZE'] and time < self.statesEnd['DE_PRESSURIZE']):
            return 1
        return 0

    def getLoxTankLiquidLevelData(self, time):
        level = 0
        if (self.getState(time) == "PRE_TEST"):
            level = 0
        elif (self.getState(time) == "PRESSURIZE"):
             level = 90.0*(time - self.statesStart['PRESSURIZE'])/self.statesLength['PRESSURIZE']
        elif (self.getState(time) == "LEAK_CHECKING"):
            level = 90
        elif (self.getState(time) == "DE_PRESSURIZE"):
            level = 90.0*(1-(time - self.statesStart['DE_PRESSURIZE'])/self.statesLength['DE_PRESSURIZE'])
        else:
            level = 0
        return round(level)
    def getEthanolTankLiquidLevelData(self, time):
        level = 0
        if (self.getState(time) == "PRE_TEST"):
            level = 0
        elif (self.getState(time) == "PRESSURIZE"):
            level = 90.0*(time - self.statesStart['PRESSURIZE'])/self.statesLength['PRESSURIZE']
        elif (self.getState(time) == "LEAK_CHECKING"):
            level = 90
        elif (self.getState(time) == "DE_PRESSURIZE"):
            level = 90.0*(1-(time - self.statesStart['DE_PRESSURIZE'])/self.statesLength['DE_PRESSURIZE'])
        else:
            level = 0
        return round(level)

    def getLoxTankTemperatureData(self, time):
        temperature = 0
        if (time < self.statesEnd['PRESSURIZE']):
            temperature = 30
        elif (time < self.statesStart['DE_PRESSURIZE']):
            x = [
                self.statesLength['PRESSURIZE'],
                self.statesStart['DE_PRESSURIZE'],
                (self.statesLength['PRESSURIZE'] - self.statesStart['DE_PRESSURIZE'])*0.5 + self.statesLength['PRESSURIZE']
            ]
            y = [
                30,
                self.minLOXTemperature,
                self.minLOXTemperature*0.5
            ]
            poly = np.polyfit(x, y, 2)
            temperature = np.polyval(poly, time)
        else:
            x = [
                self.statesStart['DE_PRESSURIZE'],
                self.statesEnd['POST_TEST'],
                (self.statesStart['DE_PRESSURIZE'] - self.statesEnd['POST_TEST'])*0.5 + self.statesStart['DE_PRESSURIZE']
            ]
            y = [
                self.minLOXTemperature,
                self.minLOXTemperature*0.5,
                self.minLOXTemperature*0.75
            ]
            poly = np.polyfit(x, y, 2)
            temperature = np.polyval(poly, time)
        
        if temperature > 30:
            temperature = 30
        return temperature

    def getEthanolTankTemperatureData(self, time):
        temperature = 0
        if (time < self.statesEnd['PRESSURIZE']):
            temperature = 30
        elif (time < self.statesStart['DE_PRESSURIZE']):
            x = [
                self.statesLength['PRESSURIZE'],
                self.statesStart['DE_PRESSURIZE'],
                (self.statesLength['PRESSURIZE'] - self.statesStart['DE_PRESSURIZE'])*0.5 + self.statesLength['PRESSURIZE']
            ]
            y = [
                30,
                self.minEthanolTemperature,
                self.minEthanolTemperature*0.5
            ]
            poly = np.polyfit(x, y, 2)
            temperature = np.polyval(poly, time)
        else:
            x = [
                self.statesStart['DE_PRESSURIZE'],
                self.statesEnd['POST_TEST'],
                (self.statesStart['DE_PRESSURIZE'] - self.statesEnd['POST_TEST'])*0.5 + self.statesStart['DE_PRESSURIZE']
            ]
            y = [
                self.minEthanolTemperature,
                self.minEthanolTemperature*0.5,
                self.minEthanolTemperature*0.75
            ]
            poly = np.polyfit(x, y, 2)
            temperature = np.polyval(poly, time)
        
        if temperature > 30:
            temperature = 30
        return temperature

    def getNozzleTemperatureData(self, time):
        return 30
