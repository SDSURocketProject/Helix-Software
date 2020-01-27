import json, os, genGeneric, struct, time

def genEEPROMBIN():
    with open("config/EEPROM.json", 'r') as EEPROMConfigs:
        SEBconfigs = json.load(EEPROMConfigs)
    with open("config/EEPROMLAYOUT.json", 'r') as EEPROMConfigs:
        layouts = json.load(EEPROMConfigs)
    with open("config/CAN.json", 'r') as CANFile:
        CANIDs = json.load(CANFile)

    for SEBconfig in SEBconfigs:
        binOut = getBin(SEBconfig, layouts, CANIDs)
        if (binOut == ""):
            return ""
        # Create a new file based on the SEB Name and write the binary to it
        with open("memory/" + SEBconfig['SEB Name'].replace(' ', '_') + "_SEB.mem", 'wb') as binFile:
            binFile.write(binOut)

    return "Success"

# Generates the proper binary for the given SEBconfig
def getBin(SEBconfig, layouts, CANIDs):    
    # Find the proper layout for the given EEPROM file
    configLayout = ""
    for layout in layouts:
        if (layout['VersionName'] == SEBconfig['Layout Version Name']):
            configLayout = layout
            break
    if (configLayout == ""):
        print(f"Unable to find layout verion: \"{SEBconfig['Layout Version Name']}\"")
        return ""

    # Get Layout Rev Number which should always be the first 4 bytes of a SEBconfig
    if (configLayout['Data'][0]['Name'] != "Layout Rev Number"):
        print(f"Error in EEPROM SEBconfig \"{configLayout['Layout Version Name']}\"")
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
            memoryLocationFullName = "Board VIN Voltage CanID".replace("Board", SEBconfig['SEB Name'])
            for ID in CANIDs:
                if (memoryLocationFullName.find(ID['CANID_NAME']) != -1):
                    binOut += packMemoryLocation(memoryLocation['Data Type'], int(ID['CANID']))
        elif (memoryLocation['Name'] == "Board VIN Current CanID"):
            memoryLocationFullName = "Board VIN Current CanID".replace("Board", SEBconfig['SEB Name'])
            for ID in CANIDs:
                if (memoryLocationFullName.find(ID['CANID_NAME']) != -1):
                    binOut += packMemoryLocation(memoryLocation['Data Type'], int(ID['CANID']))

        # Check if the memory location is for a sensor
        # The first word in a sensor location will be a generic sensor name like PT0 or TC1 etc
        elif (memoryLocation['Name'].split(' ')[0] in SEBconfig):
            binOut += sensorMemLocationToBin(memoryLocation, SEBconfig, CANIDs)
        # Default to null initialized
        else:
            binOut += packMemoryLocation(memoryLocation['Data Type'], 0)
    return binOut

# Generate the proper value for the given sensor memory location
def sensorMemLocationToBin(memoryLocation, SEBconfig, CANIDs):
    for sensor in SEBconfig:
        # Find the sensor for this memory location
        if (memoryLocation['Name'].split(' ')[0] != sensor):
            continue
        # Skip unused sensors
        if (SEBconfig[sensor]['Usage'] == "Unused"):
            return packMemoryLocation(memoryLocation['Data Type'], 0)
        # Check if memory location is for a CanID or the Data Frequency associated with a CanID
        if (memoryLocation['Name'].find("CanID") != -1 or memoryLocation['Name'].find("Data Frequency") != -1):
            # Expand full name of memory location ie "HE1 State CanID" -> "LOX Fill Valve State CanID"
            memoryLocationFullName = memoryLocation['Name'].replace(memoryLocation['Name'].split(' ')[0], SEBconfig[sensor]['Usage'])
            for canID in CANIDs:
                # If the canID name is a substring of the full memory location name then they refer to the same thing
                if (memoryLocationFullName.find(canID['CANID_NAME']) != -1):
                    if (memoryLocation['Name'].find("CanID") != -1):
                        return packMemoryLocation(memoryLocation['Data Type'], int(canID['CANID']))
                    elif (memoryLocation['Name'].find("Data Frequency") != -1):
                        return packMemoryLocation(memoryLocation['Data Type'], int(canID['CANID_FREQUENCY']))
        
        # Check if memory location is for a filter value
        if (memoryLocation['Name'].find("Filter") != -1):
            FilterValue = SEBconfig[sensor]['Filter']
            filterCoefficient = memoryLocation['Name'].split(' ')[-1]
            with open("config/FILTERS.json", 'r') as filtersJSON:
                filters = json.load(filtersJSON)
            # Only using biquad filters here
            for filterTypes in filters:
                if filterTypes['Type'] != "Biquad":
                    continue
                biquadFilters = filterTypes['Filters']
                if (FilterValue not in biquadFilters):
                    print("Could not find proper filter for memory location + \"" + memoryLocation['Name'] + "\".")
                    return packMemoryLocation(memoryLocation['Data Type'], 0)
                return packMemoryLocation(memoryLocation['Data Type'], biquadFilters[FilterValue][filterCoefficient])

        # Check if memory location is for a hardware attribute
        # Find hardware by serial number
        with open("config/HARDWARE.json", 'r') as hardwareJSON:
            hardware = json.load(hardwareJSON)
        for hardwareComponent in hardware:
            if (SEBconfig[sensor]['Serial Number'] != hardwareComponent['Serial Number']):
                continue
            # Found corresponding hardware, look for the particular parameter
            for parameter in hardwareComponent:
                if (memoryLocation['Name'].find(parameter) != -1):
                    # Found the parameter for the given memory location
                    return packMemoryLocation(memoryLocation['Data Type'], hardwareComponent[parameter])
        
    return packMemoryLocation(memoryLocation['Data Type'], 0)

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