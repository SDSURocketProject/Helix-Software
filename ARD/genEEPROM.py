import json, os, genGeneric, struct, time

def genEEPROMBIN():
    with open("config/EEPROM.json", 'r') as EEPROMConfigs:
        configs = json.load(EEPROMConfigs)
    with open("config/EEPROMLAYOUT.json", 'r') as EEPROMConfigs:
        layouts = json.load(EEPROMConfigs)
    with open("config/CAN.json", 'r') as CANFile:
        CANIDs = json.load(CANFile)

    for config in configs:
        binOut = getBin(config, layouts, CANIDs)
        if (binOut == ""):
            return ""
        # Create a new file based on the SEB Name and write the binary to it
        with open("memory/" + config['SEB Name'].replace(' ', '_') + "_SEB.mem", 'wb') as binFile:
            binFile.write(binOut)

    return "Success"

# Generates the proper binary for the given config
def getBin(config, layouts, CANIDs):    
    # Find the proper layout for the given EEPROM file
    configLayout = ""
    for layout in layouts:
        if (layout['VersionName'] == config['Layout Version Name']):
            configLayout = layout
            break
    if (configLayout == ""):
        print(f"Unable to find layout verion: \"{config['Layout Version Name']}\"")
        return ""

    # Get Layout Rev Number which should always be the first 4 bytes of a config
    if (configLayout['Data'][0]['Name'] != "Layout Rev Number"):
        print(f"Error in EEPROM config \"{configLayout['Layout Version Name']}\"")
        print("\"Layout Rev Number\" must be the the first 4 bytes of all memory layouts")
        return ""
    binOut = struct.pack("<" + configLayout['Data'][0]['Data Type'], int(configLayout['VersionID']))

    # Generate the binary for each memory location the the layout
    for memoryLocation in configLayout['Data']:
        if (memoryLocation['Name'] == "Layout Rev Number"):
            continue
        elif (memoryLocation['Name'] == "EEPROM Layout Compile Time"):
            binOut += struct.pack("<" + memoryLocation['Data Type'], int(time.time()))
        # Check if the memory location is for a sensor
        elif (memoryLocation['Name'].split(' ')[0] in config):
            binOut += sensorMemLocationToBin(memoryLocation, config, CANIDs)
        # Default to null initialized
        else:
            binOut += struct.pack("<" + memoryLocation['Data Type'], 0)
    return binOut

def sensorMemLocationToBin(memoryLocation, config, CANIDs):
    for sensor in config:
        # Find the sensor for this memory location
        if (memoryLocation['Name'].split(' ')[0] != sensor):
            continue
        # Skip unused sensors
        if (config[sensor]['Usage'] == "Unused"):
            return struct.pack("<" + memoryLocation['Data Type'], 0)
        # Check if memory location is for a CanID
        if (memoryLocation['Name'].find("CanID") != -1):
            print(config[sensor]['Usage'] + memoryLocation['Name'].lstrip(sensor).rstrip("CanID").rstrip())
            for canID in CANIDs:
                if (canID['CANID_NAME'] == config[sensor]['Usage'] + memoryLocation['Name'].lstrip(sensor).rstrip("CanID").rstrip()):
                    return struct.pack("<" + memoryLocation['Data Type'], int(canID['CANID']))
    return struct.pack("<" + memoryLocation['Data Type'], 0)