import json, os, genGeneric, struct, time

eepromLayoutFilePath = "config/EEPROMLAYOUT.json"

def genEEPROMBIN():
    with open("config/EEPROM.json", 'r') as EEPROMConfigs:
        EBconfigs = json.load(EEPROMConfigs)
    with open(eepromLayoutFilePath, 'r') as EEPROMConfigs:
        layouts = json.load(EEPROMConfigs)
    with open("config/CAN.json", 'r') as CANFile:
        CANIDs = json.load(CANFile)

    for EBconfig in EBconfigs:
        binOut = getBin(EBconfig, layouts, CANIDs)
        if (binOut == ""):
            return ""
        # Create a new file based on the EB Name and write the binary to it
        with open("memory/" + EBconfig['EB Name'].replace(' ', '_') + "_EB.mem", 'wb') as binFile:
            binFile.write(binOut)

    return "Success"

# Generates the proper binary for the given EBconfig
def getBin(EBconfig, layouts, CANIDs):    
    # Find the proper layout for the given EEPROM file
    configLayout = ""
    for layout in layouts:
        if (layout['VersionName'] == EBconfig['Layout Version Name']):
            configLayout = layout
            break
    if (configLayout == ""):
        print(f"Unable to find layout verion: \"{EBconfig['Layout Version Name']}\"")
        return ""

    # Get Layout Rev Number which should always be the first 4 bytes of a EBconfig
    if (configLayout['Data'][0]['Name'] != "Layout Rev Number"):
        print(f"Error in EEPROM EBconfig \"{configLayout['Layout Version Name']}\"")
        print("\"Layout Rev Number\" must be the the first 4 bytes of all memory layouts")
        return ""
    binOut = packMemoryLocation(configLayout['Data'][0]['Data Type'], int(configLayout['VersionID']))

    # Generate the binary for each memory location the the layout
    # These come from EEPROMLAYOUT.json
    for memoryLocation in configLayout['Data']:
        if (memoryLocation['Name'] == "Layout Rev Number"):
            continue
        elif (memoryLocation['Name'] == "EEPROM Layout Compile Time"):
            # Initialize with current epoch time
            binOut += packMemoryLocation(memoryLocation['Data Type'], time.time())
        elif (memoryLocation['Name'] == "Board Status"):
            # Initialize with null
            binOut += packMemoryLocation(memoryLocation['Data Type'], 0)
        elif (memoryLocation['Name'] == "Board VIN Voltage CanID"):
            memoryLocationFullName = "Board VIN Voltage CanID".replace("Board", EBconfig['EB Name'])
            for ID in CANIDs:
                if (memoryLocationFullName.find(ID['CANID_NAME']) != -1):
                    binOut += packMemoryLocation(memoryLocation['Data Type'], int(ID['CANID']))
        elif (memoryLocation['Name'] == "Board VIN Current CanID"):
            memoryLocationFullName = "Board VIN Current CanID".replace("Board", EBconfig['EB Name'])
            for ID in CANIDs:
                if (memoryLocationFullName.find(ID['CANID_NAME']) != -1):
                    binOut += packMemoryLocation(memoryLocation['Data Type'], int(ID['CANID']))

        # Check if the memory location is for a sensor
        # The first word in a sensor location will be a generic sensor name like PT0 or TC1 etc
        elif (memoryLocation['Name'].split(' ')[0] in EBconfig):
            binOut += sensorMemLocationToBin(memoryLocation, EBconfig, CANIDs)
        # Default to null initialized
        else:
            binOut += packMemoryLocation(memoryLocation['Data Type'], 0)
    return binOut

# Generate the proper value for the given sensor memory location
def sensorMemLocationToBin(memoryLocation, EBconfig, CANIDs):
    # Find the sensor for this memory location
    sensorConfig = ""
    sensorType = ""
    for sensor in EBconfig:
        if (memoryLocation['Name'].split(' ')[0] == sensor):
            sensorConfig = EBconfig[sensor]
            sensorType = sensor
            break
    
    # Skip over unused sensors
    if (sensorConfig['Usage'] == "Unused"):
        return packMemoryLocation(memoryLocation['Data Type'], 0)

    # CanID related memory locations
    if (memoryLocation['Name'].find("Data CanID") != -1):
        canID = findCANID('CANID', sensorConfig['CANID_DATA'], CANIDs)
        if canID == "":
            genGeneric.warning(f"Invalid CANID \"{sensorConfig['CANID_DATA']}\" for CANID_DATA for \"{sensorConfig['Usage']}\" in EB config \"{EBconfig['EB Name']}\" in  file \"{eepromLayoutFilePath}\".")
        return packMemoryLocation(memoryLocation['Data Type'], int(sensorConfig['CANID_DATA']))
    
    elif (memoryLocation['Name'].find("Current CanID") != -1):
        canID = findCANID('CANID', sensorConfig['CANID_CURRENT'], CANIDs)
        if canID == "":
            genGeneric.warning(f"Invalid CANID \"{sensorConfig['CANID_CURRENT']}\" for CANID_CURRENT for \"{sensorConfig['Usage']}\" in EB config \"{EBconfig['EB Name']}\" in  file \"{eepromLayoutFilePath}\".")
        return packMemoryLocation(memoryLocation['Data Type'], int(sensorConfig['CANID_CURRENT']))
    
    elif (memoryLocation['Name'].find("Data Frequency") != -1):
        canID = findCANID('CANID', sensorConfig['CANID_DATA'], CANIDs)
        if canID == "":
            genGeneric.warning(f"Invalid CANID \"{sensorConfig['CANID_DATA']}\" for CANID_DATA for \"{sensorConfig['Usage']}\" in EB config \"{EBconfig['EB Name']}\" in  file \"{eepromLayoutFilePath}\".")
        return packMemoryLocation(memoryLocation['Data Type'], canID['CANID_FREQUENCY'])

    # Filter related memory locations
    if (memoryLocation['Name'].find("Filter") != -1):
        with open("config/FILTERS.json", 'r') as filtersJSON:
            filters = json.load(filtersJSON)
        for filterType in filters:
            if filterType['Name'] == sensorConfig['Filter']:
                # Assume the coefficient is the last word in the name
                filterCoefficient = memoryLocation['Name'].split(' ')[-1]
                return packMemoryLocation(memoryLocation['Data Type'], filterType['Coefficients'][filterCoefficient])
        genGeneric.warning(f"Unable to find filter \"{sensorConfig['Filter']}\" for \"{sensorConfig['Usage']}\" in EB config \"{EBconfig['EB Name']}\" in  file \"{eepromLayoutFilePath}\".")
        return packMemoryLocation(memoryLocation['Data Type'], 0)
    
    # Hardware related memory locations
    with open("config/HARDWARE.json", 'r') as hardwareJSON:
        hardware = json.load(hardwareJSON)
    for hardwareComponent in hardware:
        if (sensorConfig['Serial Number'] != hardwareComponent['Serial Number']):
            continue
        # Found corresponding hardware, look for the particular parameter
        for parameter in hardwareComponent:
            if (memoryLocation['Name'].find(parameter) != -1):
                # Found the parameter for the given memory location
                return packMemoryLocation(memoryLocation['Data Type'], hardwareComponent[parameter])

    # All remaining values set to zero
    genGeneric.warning(f"Unable to find value for memory location \"{memoryLocation['Name']}\" in EB config \"{EBconfig['EB Name']}\" in  file \"{eepromLayoutFilePath}\".")
    return packMemoryLocation(memoryLocation['Data Type'], 0)

def findCANID(parameter, value, canIDs):
    for canID in canIDs:
        if (canID[parameter] == value):
            return canID
    return ""

# Pack the given value into a struct with the given datatype
def packMemoryLocation(dataType, value):
    memValue = ""
    try:
        if (dataType == "I"):
            memValue = abs(int(value))
        elif (dataType == "i"):
            memValue =  int(value)
        elif (dataType == "f"):
            memValue =  float(value)
        elif (dataType == "d"):
            memValue =  float(value)
        else:
            raise ValueError("Invalid dataType argument given.")
    except ValueError:
        print("Cannot convert " + str(value) + " to type \"" + str(dataType) + "\".\n")
        return ""
    return struct.pack("<" + dataType, memValue)