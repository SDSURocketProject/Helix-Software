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

    isValid = True
    isValid = isValid and verifyCAN(jsonData['CAN'])
    isValid = isValid and verifyEEPROM(jsonData['EEPROM'], jsonData['HARDWARE'])
    isValid = isValid and verifyEEPROMLAYOUT(jsonData['EEPROMLAYOUT'])
    isValid = isValid and verifyFILTERS()
    isValid = isValid and verifyHARDWARE()
    isValid = isValid and verifySTATES(jsonData['STATES'])

    if not isValid:
        genGeneric.error("JSON files are not valid, see above warnings for more information.")
    
    return True

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
    isValid = True
    for ID in canIDs:
        if "CANID" not in ID:
            isValid = verifyWarning(f"CANID field is required for ID \"{ID}\" in \"{CANfile}\".")
            # Other checks require CANID to be defined, must continue
            continue
        for param in ID:
            if param not in validCANParameters:
                isValid = verifyWarning(f"Unrecognized parameter \"{param}\" found in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        if int(ID['CANID']) < 0 or int(ID['CANID']) >= 2**11:
            isValid = verifyWarning(f"CANID \"{ID['CANID']}\" is outside allowable range [0, 2047]. CANID \"{ID['CANID']}\" in \"{CANfile}\".")

        if (ID['CANID'] in usedIDs):
            isValid = verifyWarning(f"Duplicate CANID \"{ID['CANID']}\" found in \"{CANfile}\".")
        else:
            usedIDs.append(ID['CANID'])
            
        if "CANID_NAME" not in ID:
            isValid = verifyWarning(f"CANID_NAME field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        else:
            if not isValidC(ID['CANID_NAME'].replace(' ', '_'), "variable"):
                isValid = verifyWarning(f"CANID_NAME \"{ID['CANID_NAME']}\" cannot be converted to a valid C/C++ variable name. CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            if ID['CANID_NAME'] in usedNames:
                isValid = verifyWarning(f"Duplicate CANID_NAME \"{ID['CANID_NAME']}\" found in \"{CANfile}\".")
            else:
                usedNames.append(ID['CANID_NAME'])

        if "CANID_FREQUENCY" not in ID:
            isValid = verifyWarning(f"CANID_FREQUENCY field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        if int(ID['CANID']) < 0 :
            isValid = verifyWarning(f"CANID_FREQUENCY \"{ID['CANID_FREQUENCY']}\"Hz is outside allowable range [0, infinity). CANID \"{ID['CANID']}\" in \"{CANfile}\".")

        if "bytes" not in ID:
            isValid = verifyWarning(f"bytes field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        else:
            isValid = verifyCANBytes(ID)


    return isValid

def verifyCANBytes(ID):
    isValid = True
    byteDefCount = 1
    byteCount = 0
    for byteDef in ID['bytes']:
        for param in byteDef:
            if param not in validCANBytesParameters:
                isValid = verifyWarning(f"Unrecognized parameter \"{param}\" found in byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        if "Size" not in byteDef:
            isValid = verifyWarning(f"Size field is required for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        else:
            byteCount = byteCount + int(byteDef['Size'])

        if "Name" not in byteDef:
            isValid = verifyWarning(f"Name field is required for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        elif not isValidC(byteDef['Name'].replace(' ', '_'), "variable"):
            isValid = verifyWarning(f"\"{byteDef['Name']}\" cannot be converted to a valid C/C++ variable name. Byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")

        # Check optional parameters
        if "Signed" in byteDef:
            if byteDef['Signed'] != "True" and byteDef['Signed'] != "False":
                isValid = verifyWarning(f"\"Signed\" parameter in byte definition must be either \"True\" or \"False\". Byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        bitCount = 0
        if "bits" in byteDef:
            for bitDef in byteDef['bits'][0]:
                if not isValidC(byteDef['bits'][0][bitDef].replace(' ', '_'), "#define"):
                    isValid = verifyWarning(f"\"{byteDef['bits'][0][bitDef]}\" cannot be converted to a valid C/C++ macro name. Bit definition in byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
                if '-' in bitDef:
                    bitCount += 1 + int(bitDef.split('-')[1]) - int(bitDef.split('-')[0])
                else:
                    bitCount += 1
        byteDefCount += 1
        if (bitCount > 8*int(byteDef['Size'])):
            isValid = verifyWarning(f"\"Too many bits defined for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
    if (byteCount > 8):
        isValid = verifyWarning(f"Up to 8 bytes are allowed for a CAN message, {byteCount} bytes were specified in CANID \"{ID['CANID']}\" in \"{CANfile}\".")

    return isValid

def verifyEEPROM(eepromConfigs, hardware):
    isValid = True

    for boardConfig in eepromConfigs:
        if "EB Name" not in boardConfig:
            isValid = verifyWarning(f"\"EB Name\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")
        elif not isValidC(boardConfig['EB Name'].replace(' ', '_'), "variable"):
            isValid = verifyWarning(f"EB Name \"{boardConfig['EB Name']}\" cannot be converted to a valid C/C++ variable name. Board config \"{boardConfig['EB Name']}\" in \"{EEPROMfile}\"..")

        if "Layout Version Name" not in boardConfig:
            isValid = verifyWarning(f"\"Layout Version Name\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")

        if "VIN_CANID" not in boardConfig:
            isValid = verifyWarning(f"\"VIN_CANID\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")

        if "VIN_CURRENT_CANID" not in boardConfig:
            isValid = verifyWarning(f"\"VIN_CURRENT_CANID\" field is required for EEPROM config. Board config \"{boardConfig}\" in \"{EEPROMfile}\".")

    return isValid

validEEPROMLAYOUTParameters = [
    "VersionID",
    "VersionName",
    "Data"
]

def verifyEEPROMLAYOUT(eepromLayouts):
    isValid = True
    versionIDs = []
    versionNames = []
    for layout in eepromLayouts:
        if "VersionID" not in layout:
            isValid = verifyWarning(f"\"VersionID\" field is required for EEPROM Layout config. Config \"{layout}\" in \"{EEPROMLAYOUTfile}\".")
            # Other warnings rely on the VersionID field
            continue
        else:
            if not layout['VersionID'].isnumeric():
                isValid = verifyWarning(f"VersionID \"{layout['VersionID']}\" must be a number encoded as a string. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            if layout['VersionID'] in versionIDs:
                isValid = verifyWarning(f"Duplicate VersionID \"{layout['VersionID']}\" found in EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            else:
                versionIDs.append(layout['VersionID'])
        
        if "VersionName" not in layout:
            isValid = verifyWarning(f"\"VersionName\" field is required for EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            if not isValidC(layout['VersionName'].replace(' ', '_'), "variable"):
                isValid = verifyWarning(f"VersionName \"{layout['VersionName']}\" cannot be converted to a valid C/C++ variable name. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            if layout['VersionName'] in versionNames:
                isValid = verifyWarning(f"Duplicate VersionName \"{layout['VersionName']}\" found in EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            else:
                versionIDs.append(layout['VersionName'])

        if "Data" not in layout:
            isValid = verifyWarning(f"\"Data\" field is required for EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            isValid = isValid and verifyEEPROMLAYOUTData(layout)

        for item in layout:
            if item not in validEEPROMLAYOUTParameters:
                isValid = verifyWarning(f"Unrecognized field \"{item}\" found in EEPROM Layout config. Config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
    return isValid

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
    isValid = True
    for dataDef in layout['Data']:
        defNames = []
        if "Name" not in dataDef:
            isValid = verifyWarning(f"\"Name\" field is required for Data definition. Definition \"{dataDef}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
            # Other warnings rely on the Name field
            continue
        if not isValidC(dataDef['Name'].replace(' ', '_'), "variable"):
            isValid = verifyWarning(f"Name \"{dataDef['Name']}\" cannot be converted to a valid C/C++ variable name. Definition \"{dataDef}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        if dataDef['Name'] in defNames:
            isValid = verifyWarning(f"Duplicate VersionName \"{layout['VersionName']}\" found in EEPROM Layout config. Definition \"{dataDef}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            defNames.append(dataDef['Name'])
        
        if "Data Type" not in dataDef:
            isValid = verifyWarning(f"\"Data Type\" field is required for Data definition. Definition name \"{dataDef['Name']}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        else:
            if dataDef['Data Type'] not in validDataTypes:
                isValid = verifyWarning(f"\"Data Type\" \"{dataDef['Data Type']}\" is not a valid type. Definition name \"{dataDef['Name']}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")
        
        for item in dataDef:
            if item not in validEEPROMLAYOUTDataParameters:
                isValid = verifyWarning(f"Unrecognized field \"{item}\" found in Data definition. Definition name \"{dataDef['Name']}\" in config VersionID \"{layout['VersionID']}\" in \"{EEPROMLAYOUTfile}\".")

    return isValid
    
def verifyFILTERS():
    return True

def verifyHARDWARE():
    return True

def verifySTATES(states):
    isValid = True
    for state in states:
        if not isValidC(state.replace(' ', '_'), "variable"):
            isValid = verifyWarning(f"State \"{state}\" cannot be converted to a valid C/C++ variable name. Defined in \"{STATESfile}\"")
    return isValid

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

# calls genGeneric warning and returns false for setting isValid
def verifyWarning(message):
    genGeneric.warning(message)
    return False
