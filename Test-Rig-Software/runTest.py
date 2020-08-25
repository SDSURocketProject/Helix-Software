import tests.leakCheckSuccess as leakCheckSuccess
import tests.leakCheckFailure as leakCheckFailure
import numpy as np
import matplotlib.pyplot as plt
import time

sensors = [
    "Helium Pressure Pt Data",
    "Lox Pressure Pt Data",
    "Ethanol Pressure Pt Data",
    "Chamber Pressure Pt Data",
    "Helium Fill Valve Hall Effect State",
    "Lox Fill Valve Hall Effect State",
    "Ethanol Fill Valve Hall Effect State",
    "Lox Tank Liquid Level Data",
    "Ethanol Tank Liquid Level Data",
    "Lox Tank Temperature Data",
    "Ethanol Tank Temperature Data",
    "Nozzle Temperature Data",
    "Helium Pressure Pt Current",
    "Lox Pressure Pt Current",
    "Ethanol Pressure Pt Current",
    "Chamber Pressure Pt Current",
    "Helium Fill Valve Hall Effect Current",
    "Lox Fill Valve Hall Effect Current",
    "Ethanol Fill Valve Hall Effect Current"
]

verifySensors = [
    "Helium Pressure Pt Data",
    "Lox Pressure Pt Data",
    "Ethanol Pressure Pt Data",
    "Chamber Pressure Pt Data",
    "Helium Fill Valve Hall Effect State",
    "Lox Fill Valve Hall Effect State",
    "Ethanol Fill Valve Hall Effect State",
    "Lox Tank Liquid Level Data",
    "Ethanol Tank Liquid Level Data",
    "Lox Tank Temperature Data",
    "Ethanol Tank Temperature Data",
    "Nozzle Temperature Data"
]

def sendCommand(sensor, value):
    pass

def runTest(testCase, outputsLogFile):
    start = time.time()
    value = 0
    for timePoint in np.linspace(0, testCase.getTestTime(), round(testCase.getTestTime()/0.1)):
        startLoopTime = time.time()
        logLine = ""
        
        for sensor in sensors:
            value = testCase.getSensorValue(sensor, timePoint)
            logLine += str(value) + ', '
            sendCommand(sensor, value)

        outputsLogFile.write(logLine[:-2])

        endLoopTime = time.time()
        sleepTime = 0.1 - (endLoopTime - startLoopTime)
        if (sleepTime < 0):
            print("Missed loop timing in runTest")
        else:
            time.sleep(sleepTime)

    return time.time()-start

def runTestCases(testCases, testName):
    with open(f"testLogs/{testName}.log") as logFile:
        print(f"Starting test {testName}")
        for testCase in testCases:
            print(f"Starting test case {testCase.testName()}")
            runTest(testCase, logFile)

def plotTest(testCase, value, title="", interval=0.1):
    x = []
    y = []
    for timePoint in np.linspace(0, testCase.getTestTime(), round(testCase.getTestTime()/interval)):
        x.append(round(timePoint, 3))
        y.append(testCase.getSensorValue(value, round(timePoint, 3)))
    plt.plot(x, y)
    plt.ylabel(value)
    plt.xlabel("Time")
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    testCase = leakCheckSuccess.leakCheckSuccess()
    testCase2 = leakCheckFailure.leakCheckOverpressHelium()

    plotTest(testCase, "Helium Pressure Pt Data", "Leak check success")
    plotTest(testCase2, "Helium Pressure Pt Data", "Leak check with helium overpressurization")
