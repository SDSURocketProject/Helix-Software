import json, genGeneric, re, math

CANfile = ""
EEPROMfile = ""
EEPROMLAYOUTfile = ""
FILTERSfile = ""
HARDWAREfile = ""
STATESfile = ""

def verifyJSON(jsonData, jsonFileLocations):
    global CANfile
    global EEPROMfile
    global EEPROMLAYOUTfile
    global FILTERSfile
    global HARDWAREfile
    global STATESfile

    CANfile = jsonFileLocations['--can-file']
    EEPROMfile = jsonFileLocations['--eeprom-file']
    EEPROMLAYOUTfile = jsonFileLocations['--eepromlayout-file']
    FILTERSfile = jsonFileLocations['--filters-file']
    HARDWAREfile = jsonFileLocations['--hardware-file']
    STATESfile = jsonFileLocations['--states-file']

    warningCount = 0
    warningCount += verifyCAN(jsonData['CAN'])
    warningCount += verifyEEPROM(jsonData['EEPROM'], jsonData['HARDWARE'])
    warningCount += verifyEEPROMLAYOUT(jsonData['EEPROMLAYOUT'])
    warningCount += verifyFILTERS()
    warningCount += verifyHARDWARE(jsonData['HARDWARE'])
    warningCount += verifySTATES(jsonData['STATES'])

    if warningCount > 0:
        if warningCount == 1:
            print(f"\n{warningCount} warning was found.")
        else:
            print(f"\n{warningCount} warnings were found.")
        genGeneric.error("JSON files are not valid, see above warnings for more information.\n")
    
    return True

#############################################################################################################
# verifyCAN
#############################################################################################################

validCANParameters = [
    "CANID",
    "CANID_NAME",
    "CANID_FREQUENCY",
    "bytes",
]

validCANBytesParameters = [
    "Size",
    "Name",
    "Signed",
    "MinValue",
    "MaxValue",
    "Units",
    "bits"
]

def verifyCAN(canIDs):
    usedIDs = []
    usedNames = []
    warningCount = 0
    for ID in canIDs:
        if "CANID" not in ID:
            warningCount += verifyWarning(f"CANID field is required for ID \"{ID}\" in \"{CANfile}\".")
            # Other checks require CANID to be defined, must continue
            continue
        for param in ID:
            if param not in validCANParameters:
                warningCount += verifyWarning(f"Unrecognized parameter \"{param}\" found in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        if int(ID['CANID']) < 0 or int(ID['CANID']) >= 2**11:
            warningCount += verifyWarning(f"CANID \"{ID['CANID']}\" is outside allowable range [0, 2047]. CANID \"{ID['CANID']}\" in \"{CANfile}\".")

        if (ID['CANID'] in usedIDs):
            warningCount += verifyWarning(f"Duplicate CANID \"{ID['CANID']}\" found in \"{CANfile}\".")
        else:
            usedIDs.append(ID['CANID'])
            
        if "CANID_NAME" not in ID:
            warningCount += verifyWarning(f"CANID_NAME field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        else:
            if not isValidC(ID['CANID_NAME'].replace(' ', '_'), "variable"):
                warningCount += verifyWarning(f"CANID_NAME \"{ID['CANID_NAME']}\" cannot be converted to a valid C/C++ variable name. CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            if ID['CANID_NAME'] in usedNames:
                warningCount += verifyWarning(f"Duplicate CANID_NAME \"{ID['CANID_NAME']}\" found in \"{CANfile}\".")
            else:
                usedNames.append(ID['CANID_NAME'])

        if "CANID_FREQUENCY" not in ID:
            warningCount += verifyWarning(f"CANID_FREQUENCY field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        if int(ID['CANID']) < 0 :
            warningCount += verifyWarning(f"CANID_FREQUENCY \"{ID['CANID_FREQUENCY']}\"Hz is outside allowable range [0, infinity). CANID \"{ID['CANID']}\" in \"{CANfile}\".")

        if "bytes" not in ID:
            warningCount += verifyWarning(f"bytes field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        else:
            warningCount += verifyCANBytes(ID)


    return warningCount

def verifyCANBytes(ID):
    warningCount = 0
    byteDefCount = 1
    byteCount = 0
    for byteDef in ID['bytes']:
        for param in byteDef:
            if param not in validCANBytesParameters:
                warningCount += verifyWarning(f"Unrecognized parameter \"{param}\" found in byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        if "Size" not in byteDef:
            warningCount += verifyWarning(f"Size field is required for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        else:
            byteCount = byteCount + int(byteDef['Size'])

        if "Name" not in byteDef:
            warningCount += verifyWarning(f"Name field is required for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        elif not isValidC(byteDef['Name'].replace(' ', '_'), "variable"):
            warningCount += verifyWarning(f"\"{byteDef['Name']}\" cannot be converted to a valid C/C++ variable name. Byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")

        # Check optional parameters
        if "Signed" in byteDef:
            if byteDef['Signed'] != "True" and byteDef['Signed'] != "False":
                warningCount += verifyWarning(f"\"Signed\" parameter in byte definition must be either \"True\" or \"False\". Byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        bitCount = 0
        if "bits" in byteDef:
            for bitDef in byteDef['bits'][0]:
                if not isValidC(byteDef['bits'][0][bitDef].replace(' ', '_'), "#define"):
                    warningCount += verifyWarning(f"\"{byteDef['bits'][0][bitDef]}\" cannot be converted to a valid C/C++ macro name. Bit definition in byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
                if '-' in bitDef:
                    bitCount += 1 + int(bitDef.split('-')[1]) - int(bitDef.split('-')[0])
                else:
                    bitCount += 1
        byteDefCount += 1
        if (bitCount > 8*int(byteDef['Size'])):
            warningCount += verifyWarning(f"\"Too many bits defined for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
    if (byteCount > 8):
        warningCount += verifyWarning(f"Up to 8 bytes are allowed for a CAN message, {byteCount} bytes were specified in CANID \"{ID['CANID']}\" in \"{CANfile}\".")

    return warningCount

#############################################################################################################
# verifyEEPROM
#############################################################################################################

def verifyEEPROM(eepromConfigs, hardware):
    warningCount = 0

    for boardConfig in eepromConfigs:
        if "EB Name" not in boardConfig:
            warningCount += verifyWarning(f"\"EB Name\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")
        elif not isValidC(boardConfig['EB Name'].replace(' ', '_'), "variable"):
            warningCount += verifyWarning(f"EB Name \"{boardConfig['EB Name']}\" cannot be converted to a valid C/C++ variable name. Board config \"{boardConfig['EB Name']}\" in \"{EEPROMfile}\"..")

        if "Layout Version Name" not in boardConfig:
            warningCount += verifyWarning(f"\"Layout Version Name\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")

        if "VIN_CANID" not in boardConfig:
            warningCount += verifyWarning(f"\"VIN_CANID\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")

        if "VIN_CURRENT_CANID" not in boardConfig:
            warningCount += verifyWarning(f"\"VIN_CURRENT_CANID\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")

    return warningCount

#############################################################################################################
# verifyEEPROMLAYOUT
#############################################################################################################

validEEPROMLAYOUTParameters = [
    "VersionID",
    "VersionName",
    "Data"
]

def verifyEEPROMLAYOUT(eepromLayouts):
    warningCount = 0
    versionIDs = []
    versionNames = []
    for layout in eepromLayouts:
        if "VersionID" not in layout:
            warningCount += verifyWarning(f"\"VersionID\" field is required for EEPROM Layout config. Config \"{layout}\" in \"{EEPROMLAYOUTfile}\".")
            # Other warnings rely on the VersionID field
            continue
        else:
            if not layout['VersionID'].isnumeric():
                warningCount += verifyWarning(f"VersionID \"{layout['VersionID']}\" must be a number encoded as a string. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            if layout['VersionID'] in versionIDs:
                warningCount += verifyWarning(f"Duplicate VersionID \"{layout['VersionID']}\" found in EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            else:
                versionIDs.append(layout['VersionID'])
        
        if "VersionName" not in layout:
            warningCount += verifyWarning(f"\"VersionName\" field is required for EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            if not isValidC(layout['VersionName'].replace(' ', '_'), "variable"):
                warningCount += verifyWarning(f"VersionName \"{layout['VersionName']}\" cannot be converted to a valid C/C++ variable name. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            if layout['VersionName'] in versionNames:
                warningCount += verifyWarning(f"Duplicate VersionName \"{layout['VersionName']}\" found in EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            else:
                versionIDs.append(layout['VersionName'])

        if "Data" not in layout:
            warningCount += verifyWarning(f"\"Data\" field is required for EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            warningCount += verifyEEPROMLAYOUTData(layout)

        for item in layout:
            if item not in validEEPROMLAYOUTParameters:
                warningCount += verifyWarning(f"Unrecognized field \"{item}\" found in EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
    return warningCount

validDataTypes = [
    "H",
    "I",
    "L",
    "Q",
    "h",
    "i",
    "l",
    "q",
    "f",
    "d",
    "c",
    "s",
    "p",
    "P"
]

validEEPROMLAYOUTDataParameters = [
    "Name",
    "Size",
    "Data Type"
]

def verifyEEPROMLAYOUTData(layout):
    warningCount = 0
    for dataDef in layout['Data']:
        defNames = []
        if "Name" not in dataDef:
            warningCount += verifyWarning(f"\"Name\" field is required for Data definition. Definition \"{dataDef}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            # Other warnings rely on the Name field
            continue
        if not isValidC(dataDef['Name'].replace(' ', '_'), "variable"):
            warningCount += verifyWarning(f"Name \"{dataDef['Name']}\" cannot be converted to a valid C/C++ variable name. Definition \"{dataDef}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        if dataDef['Name'] in defNames:
            warningCount += verifyWarning(f"Duplicate VersionName \"{layout['VersionName']}\" found in EEPROM Layout config. Definition \"{dataDef}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            defNames.append(dataDef['Name'])
        
        if "Data Type" not in dataDef:
            warningCount += verifyWarning(f"\"Data Type\" field is required for Data definition. Definition name \"{dataDef['Name']}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            if dataDef['Data Type'] not in validDataTypes:
                warningCount += verifyWarning(f"\"Data Type\" \"{dataDef['Data Type']}\" is not a valid type. Definition name \"{dataDef['Name']}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        
        for item in dataDef:
            if item not in validEEPROMLAYOUTDataParameters:
                warningCount += verifyWarning(f"Unrecognized field \"{item}\" found in Data definition. Definition name \"{dataDef['Name']}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")

    return warningCount

#############################################################################################################
# verifyFILTERS
#############################################################################################################

def verifyFILTERS():
    return 0

#############################################################################################################
# verifyHARDWARE
#############################################################################################################
validHardwarePTParameters = {
    "Model Number":"string",
    "Serial Number":"string",
    "Datasheet Link":"string",
    "Sensing Units":"string",
    "Pressure Port Type":"string",
    "Accuracy":"string",
    "Min Pressure":"float",
    "Max Pressure":"float",
    "Sample Rate":"int",
    "Min Output Voltage":"float",
    "Max Output Voltage":"float",
    "Min Input Voltage":"string",
    "Max Input Voltage":"string",
    "Min Temperature":"string",
    "Max Temperature":"string",
    "Calibration Polyfit p1":"float",
    "Calibration Polyfit p2":"float",
    "Calibration Polyfit p3":"float",
    "Calibration Polyfit p4":"float",
    "Calibration Polyfit p5":"float",
    "Calibration Polyfit p6":"float",
    "Calibration Polyfit p7":"float"
}

validHardwareTCParameters = {
    "Hardware Type":"string",
    "Model Number":"string",
    "Serial Number":"string",
    "Datasheet Link":"string",
    "Type":"string",
    "Sensing Units":"string",
    "Sample Rate":"int",
    "Min Temperature":"string",
    "Max Temperature":"string"
}

validHardwareRTDParameters = {
    "Hardware Type":"string",
    "Model Number":"string",
    "Serial Number":"string",
    "Datasheet Link":"string",
    "Type":"string",
    "Sensing Units":"string",
    "Sample Rate":"int",
    "Min Temperature":"string",
    "Max Temperature":"string"
}

validHardwareHALLParameters = {
    "Hardware Type":"string",
    "Model Number":"string",
    "Serial Number":"string",
    "Datasheet Link":"string",
    "Sensing Units":"string",
    "Trip":"string",
    "Release":"string",
    "Output Type":"string",
    "Min Input Voltage":"string",
    "Max Input Voltage":"string",
    "Sample Rate":"int",
    "Min Temperature":"string",
    "Max Temperature":"string"
}

def verifyHARDWARE(hardwareDefinitions):
    warningCount = 0 
    modelNumbers = []
    for hardware in hardwareDefinitions:
        if "Serial Number" not in hardware:
            warningCount += verifyWarning(f"\"Serial Number\" field is required. Hardware \"{hardware}\" in \"{EEPROMLAYOUTfile}\".")
            continue
        
        if hardware['Serial Number'] not in modelNumbers:
            modelNumbers.append(hardware['Serial Number'])
        else:
            warningCount += verifyWarning(f"Duplicate Serial Number found. Serial Number \"{hardware['Serial Number']}\" in \"{EEPROMLAYOUTfile}\".")

        if "Hardware Type" not in hardware:
            warningCount += verifyWarning(f"\"Hardware Type\" field is required. Serial Number \"{hardware['Serial Number']}\" in \"{EEPROMLAYOUTfile}\".")
        elif hardware['Hardware Type'] == "Pressure Transducer":
            warningCount += verifyHARDWAREParameters(hardware, validHardwarePTParameters)
        elif hardware['Hardware Type'] == "Thermocouple":
            warningCount += verifyHARDWAREParameters(hardware, validHardwareTCParameters)
        elif hardware['Hardware Type'] == "RTD":
            warningCount += verifyHARDWAREParameters(hardware, validHardwareRTDParameters)
        elif hardware['Hardware Type'] == "Hall Effect Sensor":
            warningCount += verifyHARDWAREParameters(hardware, validHardwareHALLParameters)
        elif hardware['Hardware Type'] == "Capacitance Sensor":
            pass
        else:
            warningCount += verifyWarning(f"Unrecognized hardware type \"{hardware}\" found in \"{EEPROMLAYOUTfile}\".")
        
    return warningCount

def verifyHARDWAREParameters(hardware, validParameters):
    warningCount = 0
    parameterList = []
    for parameter in hardware:
        if parameter == "Hardware Type":
            continue

        if parameter not in validParameters:
            warningCount += verifyWarning(f"Unrecognized parameter {parameter}. Serial Number \"{hardware['Serial Number']}\" in \"{EEPROMLAYOUTfile}\".")
            continue
        if parameter not in parameterList:
            parameterList.append(parameter)
        else:
            warningCount += verifyWarning(f"Duplicate parameter {parameter}. Serial Number \"{hardware['Serial Number']}\" in \"{EEPROMLAYOUTfile}\".")

        if not canConvert(hardware[parameter], validParameters[parameter]):
            warningCount += verifyWarning(f"Unable convert \"{hardware[parameter]}\" to \"{validParameters[parameter]}\". Serial Number \"{hardware['Serial Number']}\" in \"{EEPROMLAYOUTfile}\".")
        
    return warningCount

#############################################################################################################
# verifySTATES
#############################################################################################################

def verifySTATES(states):
    warningCount = 0
    for state in states:
        if not isValidC(state.replace(' ', '_'), "variable"):
            warningCount += verifyWarning(f"State \"{state}\" cannot be converted to a valid C/C++ variable name. Defined in \"{STATESfile}\"")
    return warningCount

#############################################################################################################
# Helper Functions
#############################################################################################################

cppKeywords = [
    "alignas"
    "alignof"
    "and"
    "and_eq"
    "asm"
    "atomic_cancel"
    "atomic_commit"
    "atomic_noexcept"
    "auto"
    "bitand"
    "bitor"
    "bool"
    "break"
    "case"
    "catch"
    "char"
    "char8_t"
    "char16_t"
    "char32_t"
    "class"
    "compl"
    "concept"
    "const"
    "consteval"
    "constexpr"
    "constinit"
    "const_cast"
    "continue"
    "co_await"
    "co_return"
    "co_yield"
    "decltype"
    "default"
    "delete"
    "do"
    "double"
    "dynamic_cast"
    "else"
    "enum"
    "explicit"
    "export"
    "extern"
    "false"
    "float"
    "for"
    "friend"
    "goto"
    "if"
    "inline"
    "int"
    "long"
    "mutable"
    "namespace"
    "new"
    "noexcept"
    "not"
    "not_eq"
    "nullptr"
    "operator"
    "or"
    "or_eq"
    "private"
    "protected"
    "public"
    "reflexpr"
    "register"
    "reinterpret_cast"
    "requires"
    "return"
    "short"
    "signed"
    "sizeof"
    "static"
    "static_assert"
    "static_cast"
    "struct"
    "switch"
    "synchronized"
    "template"
    "this"
    "thread_local"
    "throw"
    "true"
    "try"
    "typedef"
    "typeid"
    "typename"
    "union"
    "unsigned"
    "using"
    "virtual"
    "void"
    "volatile"
    "wchar_t"
    "while"
    "xor"
    "xor_eq"
    # C only keywords
    "_Far32"
    "__far32"
    "_Inline"
    "__inline"
    "_Packed"
    "__packed"
    "_Pascal"
    "_Far32 _Pascal"
    "_Far16 _Cdecl"
    "_Far16 _Pascal"
    "_Far16 _Fastcall"
    "__except"
    "__finally"
    "__leave"
    "__try"
    "_inline"
]

def isValidC(value, cType):
    if value in cppKeywords:
        return False

    if cType == "#define":
        if not re.match(r'[a-zA-Z_][a-zA-Z0-9_]+$', value):
            return False

    elif cType == "variable":
        if len(value) > 255:
            return False # Name too long
        if not re.match(r'[a-zA-Z_][a-zA-Z0-9_]+$', value):
            return False
    else:
        return False

    return True

# Check if the given value can be converted to the specified python type
def canConvert(value, toType):
    if toType == "string":
        try:
            str(value)
        except ValueError:
            return False
    elif toType == "int":
        try:
            int(value)
        except ValueError:
            return False
    elif toType == "float":
        try:
            float(value)
        except ValueError:
            return False
    else:
        raise ValueError(f"Unrecognized python type \"{toType}\".")
    
    return True

# calls genGeneric warning and returns false for setting warningCount
def verifyWarning(message):
    genGeneric.warning(message)
    return 1

if __name__ == "__main__":
    pass