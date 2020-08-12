import json, genGeneric, re

CANfile = ""
EEPROMfile = ""
EEPROMLAYOUTfile = ""
FILTERSfile = ""
HARDWAREfile = ""
STATESfile = ""

def verifyJSON(jsonFileLocations):
    global CANfile
    global EEPROMfile
    global EEPROMLAYOUTfile
    global FILTERSfile
    global HARDWAREfile
    global STATESfile

    CANfile = jsonFileLocations['CAN_FILE']
    EEPROMfile = jsonFileLocations['EEPROM_FILE']
    EEPROMLAYOUTfile = jsonFileLocations['EEPROMLAYOUT_FILE']
    FILTERSfile = jsonFileLocations['FILTERS_FILE']
    HARDWAREfile = jsonFileLocations['HARDWARE_FILE']
    STATESfile = jsonFileLocations['STATES_FILE']

    openingFile = CANfile
    try:
        CAN =          open(CANfile, 'r')
        openingFile = EEPROMfile
        EEPROM =       open(EEPROMfile, 'r')
        openingFile = EEPROMLAYOUTfile
        EEPROMLAYOUT = open(EEPROMLAYOUTfile, 'r')
        openingFile = FILTERSfile
        FILTERS =      open(FILTERSfile, 'r')
        openingFile = HARDWAREfile
        HARDWARE =     open(HARDWAREfile, 'r')
        openingFile = STATESfile
        STATES =       open(STATESfile, 'r')
    except:
        genGeneric.error(f"File {openingFile} does not exist.")
    
    openingFile = CANfile
    try:
        CAN =          json.load(CAN)
        openingFile = EEPROMfile
        EEPROM =       json.load(EEPROM)
        openingFile = EEPROMLAYOUTfile
        EEPROMLAYOUT = json.load(EEPROMLAYOUT)
        openingFile = FILTERSfile
        FILTERS =      json.load(FILTERS)
        openingFile = HARDWAREfile
        HARDWARE =     json.load(HARDWARE)
        openingFile = STATESfile
        STATES =       json.load(STATES)
    except json.decoder.JSONDecodeError:
        genGeneric.error(f"{openingFile} is not a valid JSON file, check for syntax errors.")

    isValid = True
    if not verifyCAN(CAN):
        isValid = False
    if not verifyEEPROM():
        isValid = False
    if not verifyEEPROMLAYOUT():
        isValid = False
    if not verifyFILTERS():
        isValid = False
    if not verifyHARDWARE():
        isValid = False
    if not verifySTATES():
        isValid = False

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
    isValid = True
    for ID in canIDs:
        if "CANID" not in ID:
            genGeneric.warning(f"CANID field is required for ID \"{ID}\" in \"{CANfile}\".")
            isValid = False
            # Other checks require CANID to be defined, must continue
            continue
        for param in ID:
            if param not in validCANParameters:
                genGeneric.warning(f"Unrecognized parameter \"{param}\" found in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
                isValid = False

        if "CANID_NAME" not in ID:
            genGeneric.warning(f"CANID_NAME field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False
        elif not isValidC(ID['CANID_NAME'].replace(' ', '_'), "variable"):
            genGeneric.warning(f"CANID_NAME \"{ID['CANID_NAME']}\" cannot be converted to a valid C/C++ variable name. CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False

        if "CANID_FREQUENCY" not in ID:
            genGeneric.warning(f"CANID_FREQUENCY field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False
        if "bytes" not in ID:
            genGeneric.warning(f"bytes field is required for CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False
        elif not verifyCANBytes(ID):
            isValid = False

        if (ID['CANID'] in usedIDs):
            genGeneric.warning(f"Duplicate CANID \"{ID['CANID']}\" found in \"{CANfile}\".")
            isValid = False
        else:
            usedIDs.append(ID['CANID'])


    return isValid

def verifyCANBytes(ID):
    isValid = True
    byteDefCount = 1
    byteCount = 0
    for byteDef in ID['bytes']:
        for param in byteDef:
            if param not in validCANBytesParameters:
                genGeneric.warning(f"Unrecognized parameter \"{param}\" found in byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
                isValid = False
        if "Size" not in byteDef:
            genGeneric.warning(f"Size field is required for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False
        else:
            byteCount = byteCount + int(byteDef['Size'])

        if "Name" not in byteDef:
            genGeneric.warning(f"Name field is required for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False
        elif not isValidC(byteDef['Name'].replace(' ', '_'), "variable"):
            genGeneric.warning(f"\"{byteDef['Name']}\" cannot be converted to a valid C/C++ variable name. Byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        
        # Check optional parameters
        bitCount = 0
        if "bits" in byteDef:
            for bitDef in byteDef['bits'][0]:
                if not isValidC(byteDef['bits'][0][bitDef].replace(' ', '_'), "#define"):
                    genGeneric.warning(f"\"{byteDef['bits'][0][bitDef]}\" cannot be converted to a valid C/C++ macro name. Bit definition in byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
                    isValid = False
                if '-' in bitDef:
                    bitCount += 1 + int(bitDef.split('-')[1]) - int(bitDef.split('-')[0])
                else:
                    bitCount += 1
        byteDefCount += 1
        if (bitCount > 8*int(byteDef['Size'])):
            genGeneric.warning(f"\"Too many bits defined for byte definition #{byteDefCount} in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
            isValid = False
    if (byteCount > 8):
        genGeneric.warning(f"Up to 8 bytes are allowed for a CAN message, {byteCount} bytes were specified in CANID \"{ID['CANID']}\" in \"{CANfile}\".")
        isValid = False

    return isValid

def verifyEEPROM():
    return True

def verifyEEPROMLAYOUT():
    return True

def verifyFILTERS():
    return True

def verifyHARDWARE():
    return True

def verifySTATES():
    return True

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
