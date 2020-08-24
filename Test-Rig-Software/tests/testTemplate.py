

class testTemplate():
    def __init__(self):
        statesEndTimes = {}
        statesStartTimes = {}
        statesLengthTimes = {}

        self.statesEnd = statesEndTimes
        self.statesStart = statesStartTimes
        self.statesLength = statesLengthTimes

        self.HeliumPressurePtTolerance = 10
        self.LoxPressurePtTolerance = 10
        self.EthanolPressurePtTolerance = 10
        self.ChamberPressurePtTolerance = 10
        self.HeliumFillValveHallEffectTolerance = 10
        self.LoxFillValveHallEffectTolerance = 10
        self.EthanolFillValveHallEffectTolerance = 10
        self.LoxTankLiquidLevelTolerance = 10
        self.EthanolTankLiquidLevelTolerance = 10
        self.LoxTankTemperatureTolerance = 10
        self.EthanolTankTemperatureTolerance = 10
        self.NozzleTemperatureTolerance = 10
        self.HeliumPressurePtCurrent = 10
        self.LoxPressurePtCurrent = 10
        self.EthanolPressurePtCurrent = 10
        self.ChamberPressurePtCurrent = 10
        self.HeliumFillValveHallEffectCurrent = 10
        self.LoxFillValveHallEffectCurrent = 10
        self.EthanolFillValveHallEffectCurrent = 10

    def getSensorValue(self, sensor, time):
        value = 0
        if sensor == "Helium Pressure Pt Data":
            value = self.getHeliumPressurePtData(time)
        elif sensor == "Lox Pressure Pt Data":
            value = self.getLoxPressurePtData(time)
        elif sensor == "Ethanol Pressure Pt Data":
            value = self.getEthanolPressurePtData(time)
        elif sensor == "Chamber Pressure Pt Data":
            value = self.getChamberPressurePtData(time)
        elif sensor == "Helium Fill Valve Hall Effect State":
            value = self.getHeliumFillValveHallEffectState(time)
        elif sensor == "Lox Fill Valve Hall Effect State":
            value = self.getLoxFillValveHallEffectState(time)
        elif sensor == "Ethanol Fill Valve Hall Effect State":
            value = self.getEthanolFillValveHallEffectState(time)
        elif sensor == "Lox Tank Liquid Level Data":
            value = self.getLoxTankLiquidLevelData(time)
        elif sensor == "Ethanol Tank Liquid Level Data":
            value = self.getEthanolTankLiquidLevelData(time)
        elif sensor == "Lox Tank Temperature Data":
            value = self.getLoxTankTemperatureData(time)
        elif sensor == "Ethanol Tank Temperature Data":
            value = self.getEthanolTankTemperatureData(time)
        elif sensor == "Nozzle Temperature Data":
            value = self.getNozzleTemperatureData(time)
        else:
            value = 0
        return value

    def verifySensorValue(self, sensor, time, measurement):
        isValid = False
        if sensor == "Helium Pressure Pt Data":
            isValid = verifyHeliumPressurePtData(time, measurement)
        elif sensor == "Lox Pressure Pt Data":
            isValid = verifyLoxPressurePtData(time, measurement)
        elif sensor == "Ethanol Pressure Pt Data":
            isValid = verifyEthanolPressurePtData(time, measurement)
        elif sensor == "Chamber Pressure Pt Data":
            isValid = verifyChamberPressurePtData(time, measurement)
        elif sensor == "Helium Fill Valve Hall Effect State":
            isValid = verifyHeliumFillValveHallEffectState(time, measurement)
        elif sensor == "Lox Fill Valve Hall Effect State":
            isValid = verifyLoxFillValveHallEffectState(time, measurement)
        elif sensor == "Ethanol Fill Valve Hall Effect State":
            isValid = verifyEthanolFillValveHallEffectState(time, measurement)
        elif sensor == "Lox Tank Liquid Level Data":
            isValid = verifyLoxTankLiquidLevelData(time, measurement)
        elif sensor == "Ethanol Tank Liquid Level Data":
            isValid = verifyEthanolTankLiquidLevelData(time, measurement)
        elif sensor == "Lox Tank Temperature Data":
            isValid = verifyLoxTankTemperatureData(time, measurement)
        elif sensor == "Ethanol Tank Temperature Data":
            isValid = verifyEthanolTankTemperatureData(time, measurement)
        elif sensor == "Nozzle Temperature Data":
            isValid = verifyNozzleTemperatureData(time, measurement)
        elif sensor == "Helium Pressure Pt Current":
            isValid = verifyHeliumPressurePtCurrent(time, measurement)
        elif sensor == "Lox Pressure Pt Current":
            isValid = verifyLoxPressurePtCurrent(time, measurement)
        elif sensor == "Ethanol Pressure Pt Current":
            isValid = verifyEthanolPressurePtCurrent(time, measurement)
        elif sensor == "Chamber Pressure Pt Current":
            isValid = verifyChamberPressurePtCurrent(time, measurement)
        elif sensor == "Helium Fill Valve Hall Effect Current":
            isValid = verifyHeliumFillValveHallEffectCurrent(time, measurement)
        elif sensor == "Lox Fill Valve Hall Effect Current":
            isValid = verifyLoxFillValveHallEffectCurrent(time, measurement)
        elif sensor == "Ethanol Fill Valve Hall Effect Current":
            isValid = verifyEthanolFillValveHallEffectCurrent(time, measurement)
        return isValid

    def getHeliumPressurePtData(self, time):
        return 0
    def verifyHeliumPressurePtData(self, time, measurement):
        if (abs(measurement - getHeliumPressurePtData(time)) < self.HeliumPressurePtTolerance):
            return True
        return False

    def getLoxPressurePtData(self, time):
        return 0
    def verifyLoxPressurePtData(self, time, measurement):
        if (abs(measurement - getLoxPressurePtData(time)) < self.LoxPressurePtTolerance):
            return True
        return False

    def getEthanolPressurePtData(self, time):
        return 0
    def verifyEthanolPressurePtData(self, time, measurement):
        if (abs(measurement - getEthanolPressurePtData(time)) < self.EthanolPressurePtTolerance):
            return True
        return False

    def getChamberPressurePtData(self, time):
        return 0
    def verifyChamberPressurePtData(self, time, measurement):
        if (abs(measurement - getChamberPressurePtData(time)) < self.ChamberPressurePtTolerance):
            return True
        return False

    def getHeliumFillValveHallEffectState(self, time):
        return False
    def verifyHeliumFillValveHallEffectState(self, time, measurement):
        if (abs(measurement - getHeliumFillValveHallEffectState(time)) == True):
            return True
        # Give some slack time for the system
        elif (abs(measurement - getHeliumFillValveHallEffectState(time - self.HeliumFillValveHallEffectTolerance)) == True):
            return True
        return False

    def getLoxFillValveHallEffectState(self, time):
        return False
    def verifyLoxFillValveHallEffectState(self, time, measurement):
        if (abs(measurement - getLoxFillValveHallEffectState(time)) == True):
            return True
        # Give some slack time for the system
        elif (abs(measurement - getLoxFillValveHallEffectState(time - self.LoxFillValveHallEffectTolerance)) == True):
            return True
        return False

    def getEthanolFillValveHallEffectState(self, time):
        return False
    def verifyEthanolFillValveHallEffectState(self, time, measurement):
        if (abs(measurement - getEthanolFillValveHallEffectState(time)) == True):
            return True
        # Give some slack time for the system
        elif (abs(measurement - getEthanolFillValveHallEffectState(time - self.EthanolFillValveHallEffectTolerance)) == True):
            return True
        return False

    def getLoxTankLiquidLevelData(self, time):
        return 0.0
    def verifyLoxTankLiquidLevelData(self, time, measurement):
        if (abs(measurement - getLoxTankLiquidLevelData(time)) < self.LoxTankLiquidLevelTolerance):
            return True
        return False

    def getEthanolTankLiquidLevelData(self, time):
        return 0.0
    def verifyEthanolTankLiquidLevelData(self, time, measurement):
        if (abs(measurement - getEthanolTankLiquidLevelData(time)) < self.EthanolTankLiquidLevelTolerance):
            return True
        return False

    def getLoxTankTemperatureData(self, time):
        return 0
    def verifyLoxTankTemperatureData(self, time, measurement):
        if (abs(measurement - getLoxTankTemperatureData(time)) < self.LoxTankTemperatureTolerance):
            return True
        return False

    def getEthanolTankTemperatureData(self, time):
        return 0
    def verifyEthanolTankTemperatureData(self, time, measurement):
        if (abs(measurement - getEthanolTankTemperatureData(time)) < self.EthanolTankTemperatureTolerance):
            return True
        return False

    def getNozzleTemperatureData(self, time):
        return 0
    def verifyNozzleTemperatureData(self, time, measurement):
        if (abs(measurement - getNozzleTemperatureData(time)) < self.NozzleTemperatureTolerance):
            return True
        return False

    def verifyHeliumPressurePtCurrent(self, time, measurement):
        if (abs(measurement - 15) < self.HeliumPressurePtCurrent):
            return True
        return False

    def verifyLoxPressurePtCurrent(self, time, measurement):
        if (abs(measurement - 15) < self.LoxPressurePtCurrent):
            return True
        return False

    def verifyEthanolPressurePtCurrent(self, time, measurement):
        if (abs(measurement - 15) < self.EthanolPressurePtCurrent):
            return True
        return False

    def verifyChamberPressurePtCurrent(self, time, measurement):
        if (abs(measurement - 15) < self.ChamberPressurePtCurrent):
            return True
        return False

    def verifyHeliumFillValveHallEffectCurrent(self, time, measurement):
        if (abs(measurement - 5) < self.HeliumFillValveHallEffectCurrent):
            return True
        return False
    def verifyLoxFillValveHallEffectCurrent(self, time, measurement):
        if (abs(measurement - 5) < self.LoxFillValveHallEffectCurrent):
            return True
        return False
    def verifyEthanolFillValveHallEffectCurrent(self, time, measurement):
        if (abs(measurement - 5) < self.EthanolFillValveHallEffectCurrent):
            return True
        return False
