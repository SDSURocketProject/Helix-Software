import csv, time

headerValueToColumn = {
    "time" : -1,
    "TRB0-PT0" : -1,
    "TRB0-PT1" : -1,
    "TRB0-PT2" : -1,
    "TRB0-TC0" : -1,
    "TRB0-TC1" : -1,
    "TRB0-RTD0" : -1,
    "TRB0-RTD1" : -1,
    "TRB0-HE0" : -1,
    "TRB0-HE1" : -1,
    "TRB0-HE2" : -1,
    "TRB1-PT0" : -1,
    "TRB1-PT1" : -1,
    "TRB1-PT2" : -1,
    "TRB1-TC0" : -1,
    "TRB1-TC1" : -1,
    "TRB1-RTD0" : -1,
    "TRB1-RTD1" : -1,
    "TRB1-HE0" : -1,
    "TRB1-HE1" : -1,
    "TRB1-HE2" : -1
}

def runTest(filePath):
    csvTest = csv.reader(filePath, delimiter=',')
    csvHeader = csvTest.next()

    index = 0
    for item in csvHeader:
        try:
            headerValueToColumn[item] = index
        except KeyError:
            print(f"Invalid column \"{item}\" in test {filePath}")
            return -1
        index = index + 1

    for value in headerValueToColumn:
        if value == -1:
            print(f'{value} not found in test {filePath}')
            return -1

    lastLine = csvTest.next()
    timeIndex = csvHeader.index('time')

    sendCommands(csvHeader, lastLine)

    for line in csvTest:
        time.sleep()
        sendCommands(csvHeader, line)
        lastLine = line

def sendCommands(header, values):
    pass