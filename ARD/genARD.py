import os
import sys
import json
import genEEPROMLAYOUT
import genEEPROM
import genCAN
import genHARDWARE
import parseOBCDocs
import verifyJSON

defaultFileLocations = {
    "--can-file":"config/CAN.json",
    "--eeprom-file":"config/EEPROM.json",
    "--eepromlayout-file":"config/EEPROMLAYOUT.json",
    "--filters-file":"config/FILTERS.json",
    "--hardware-file":"config/HARDWARE.json",
    "--states-file":"config/STATES.json",
    "--CANIDs-header":"../Helix-OBC-Firmware/inc/CANIDs.h",
    "--eepromlayout-header":"../Helix-OBC-Firmware/inc/EEPROM_Layout.h"
}

jsonData = {
    "CAN":[],
    "EEPROM":[],
    "EEPROMLAYOUT":[],
    "FILTERS":[],
    "HARDWARE":[],
    "STATES":[]
}

if __name__ == "__main__":
    
    # If script is being run from top level directory we need to cd to the ARD directory    
    if (os.getcwd().split('/')[-1] != "ARD"):
        os.chdir("ARD/")

    # Override default file locations if specified in command line args
    for location in defaultFileLocations:
        if location in sys.argv:
            defaultFileLocations[location] = sys.argv[sys.argv.find(location)+1]

    # Load config files
    openingFile = defaultFileLocations['--can-file']
    try:
        CAN =          open(defaultFileLocations['--can-file'], 'r')
        openingFile = defaultFileLocations['--eeprom-file']
        EEPROM =       open(defaultFileLocations['--eeprom-file'], 'r')
        openingFile = defaultFileLocations['--eepromlayout-file']
        EEPROMLAYOUT = open(defaultFileLocations['--eepromlayout-file'], 'r')
        openingFile = defaultFileLocations['--filters-file']
        FILTERS =      open(defaultFileLocations['--filters-file'], 'r')
        openingFile = defaultFileLocations['--hardware-file']
        HARDWARE =     open(defaultFileLocations['--hardware-file'], 'r')
        openingFile = defaultFileLocations['--states-file']
        STATES =       open(defaultFileLocations['--states-file'], 'r')
    except:
        genGeneric.error(f"File {openingFile} does not exist.")
    
    # Load json data from config files
    openingFile = defaultFileLocations['--can-file']
    try:
        jsonData['CAN'] =          json.load(CAN)
        openingFile = defaultFileLocations['--eeprom-file']
        jsonData['EEPROM'] =       json.load(EEPROM)
        openingFile = defaultFileLocations['--eepromlayout-file']
        jsonData['EEPROMLAYOUT'] = json.load(EEPROMLAYOUT)
        openingFile = defaultFileLocations['--filters-file']
        jsonData['FILTERS'] =      json.load(FILTERS)
        openingFile = defaultFileLocations['--hardware-file']
        jsonData['HARDWARE'] =     json.load(HARDWARE)
        openingFile = defaultFileLocations['--states-file']
        jsonData['STATES'] =       json.load(STATES)
    except json.decoder.JSONDecodeError:
        genGeneric.error(f"{openingFile} is not a valid JSON file, check for syntax errors.")

    if ("--skip-verify" not in sys.argv):
        print("Verifying JSON files are valid")
        verifyJSON.verifyJSON(jsonData, defaultFileLocations)
        # verifyJSON will call exit() if it fails

    # Generate C/C++ Files
    print("Generating \"CANIDs.h\" for Helix-OBC-Firmware")
    newCANIDsHeader = genCAN.getHeader(jsonData)
    with open(defaultFileLocations['--CANIDs-header'], 'r') as CAN_HEADER:
        existingCANIDsHeader = CAN_HEADER.read()
        if (existingCANIDsHeader == newCANIDsHeader):
            newCANIDsHeader = ""

    # if newCANIDsHeader gets set to "" that means that we should not write out the file
    if newCANIDsHeader != "":
        with open (defaultFileLocations['--CANIDs-header'], "w") as CAN_HEADER:
            CAN_HEADER.write(newCANIDsHeader)

    print("Generating \"EEPROM_Layout.h\" for Helix-OBC-Firmware")
    newEEPROMLAYOUTHeader = genEEPROMLAYOUT.genEEPROMHEADER(jsonData)
    with open(defaultFileLocations['--eepromlayout-header'], 'r') as EEPROM_LAYOUT_HEADER:
        existingEEPROMLAYOUTHeader = EEPROM_LAYOUT_HEADER.read()
        if (existingEEPROMLAYOUTHeader == newEEPROMLAYOUTHeader):
            newEEPROMLAYOUTHeader = ""

    # if newEEPROMLAYOUTHeader gets set to "" that means that we should not write out the file
    if newEEPROMLAYOUTHeader != "":
        with open (defaultFileLocations['--eepromlayout-header'], "w") as EEPROM_LAYOUT_HEADER:
            EEPROM_LAYOUT_HEADER.write(newEEPROMLAYOUTHeader)

    #headerEEPROMLAYOUT = genEEPROMLAYOUT.genEEPROMHEADER(jsonData)
    #with open ("../Helix-OBC-Firmware/inc/EEPROM_Layout.h", "w") as EEPROM_LAYOUT_HEADER:
    #    EEPROM_LAYOUT_HEADER.write(headerEEPROMLAYOUT)

    if ("--headers-only" in sys.argv):
        exit(0)
    
    # Create tex directory if it doesn't already exist
    try:
        os.mkdir("tex")
    except FileExistsError:
        pass

    # HARDWARE
    print("Generating \"tex/HARDWARE.tex\"")
    latexHARDWARE = genHARDWARE.getLatex(jsonData)
    if (latexHARDWARE == ""):
        print("Failed to generate HARDWARE.tex, exiting...")
        quit()
    with open ("tex/HARDWARE.tex", "w") as HARDWARE_TEX:
        HARDWARE_TEX.write(latexHARDWARE)

    # STATES
    print("Generating \"tex/STATES.tex\"")
    latexSTATES = parseOBCDocs.getLatex(jsonData)
    if (latexSTATES == ""):
        print("Failed to get documentation from Helix-OBC-Firmware documentation, exiting...")
        quit()
    with open ("tex/STATES.tex", "w") as STATES_TEX:
        STATES_TEX.write(latexSTATES)

    # CAN
    print("Generating \"tex/CANIDs.tex\"")
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(genCAN.getLatex(jsonData))

    # EEPROM
    print("Generating \"tex/EEPROMLAYOUT.tex\"")
    with open ("tex/EEPROMLAYOUT.tex", "w") as EEPROMLAYOUT_TEX:
        EEPROMLAYOUT_TEX.write(genEEPROMLAYOUT.getLatex(jsonData))

    # Generate Tex
    print("Generating \"ARD.pdf\"")

    xelatexArgs = ""
    if ("--verbose" not in sys.argv):
        xelatexArgs += "> /dev/null"

    if (os.system("xelatex --halt-on-error ARD.tex" + xelatexArgs) != 0):
        print("Failed to create ARD.pdf.")
    else:
        print("ARD.pdf successfully written.")

    # Create memory directory if it doesn't already exist
    try:
        os.mkdir("memory")
    except FileExistsError:
        pass

    # Generate Binary Files
    print("Generating EEPROM memory files")
    genEEPROM.genEEPROMBIN(jsonData)
    
