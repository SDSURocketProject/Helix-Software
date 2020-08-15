import os
import sys
import json
import genEEPROMLAYOUT
import genEEPROM
import genCAN
import genHARDWARE
import parseOBCDocs
import verifyJSON

jsonDefaultFileLocations = {
    "--can-file":"config/CAN.json",
    "--eeprom-file":"config/EEPROM.json",
    "--eepromlayout-file":"config/EEPROMLAYOUT.json",
    "--filters-file":"config/FILTERS.json",
    "--hardware-file":"config/HARDWARE.json",
    "--states-file":"config/STATES.json"
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
    for location in jsonDefaultFileLocations:
        if location in sys.argv:
            jsonDefaultFileLocations[location] = sys.argv[sys.argv.find(location)+1]

    # Load config files
    openingFile = jsonDefaultFileLocations['--can-file']
    try:
        CAN =          open(jsonDefaultFileLocations['--can-file'], 'r')
        openingFile = jsonDefaultFileLocations['--eeprom-file']
        EEPROM =       open(jsonDefaultFileLocations['--eeprom-file'], 'r')
        openingFile = jsonDefaultFileLocations['--eepromlayout-file']
        EEPROMLAYOUT = open(jsonDefaultFileLocations['--eepromlayout-file'], 'r')
        openingFile = jsonDefaultFileLocations['--filters-file']
        FILTERS =      open(jsonDefaultFileLocations['--filters-file'], 'r')
        openingFile = jsonDefaultFileLocations['--hardware-file']
        HARDWARE =     open(jsonDefaultFileLocations['--hardware-file'], 'r')
        openingFile = jsonDefaultFileLocations['--states-file']
        STATES =       open(jsonDefaultFileLocations['--states-file'], 'r')
    except:
        genGeneric.error(f"File {openingFile} does not exist.")
    
    # Load json data from config files
    openingFile = jsonDefaultFileLocations['--can-file']
    try:
        jsonData['CAN'] =          json.load(CAN)
        openingFile = jsonDefaultFileLocations['--eeprom-file']
        jsonData['EEPROM'] =       json.load(EEPROM)
        openingFile = jsonDefaultFileLocations['--eepromlayout-file']
        jsonData['EEPROMLAYOUT'] = json.load(EEPROMLAYOUT)
        openingFile = jsonDefaultFileLocations['--filters-file']
        jsonData['FILTERS'] =      json.load(FILTERS)
        openingFile = jsonDefaultFileLocations['--hardware-file']
        jsonData['HARDWARE'] =     json.load(HARDWARE)
        openingFile = jsonDefaultFileLocations['--states-file']
        jsonData['STATES'] =       json.load(STATES)
    except json.decoder.JSONDecodeError:
        genGeneric.error(f"{openingFile} is not a valid JSON file, check for syntax errors.")

    if ("--skip-verify" not in sys.argv):
        print("Verifying JSON files are valid")
        verifyJSON.verifyJSON(jsonData, jsonDefaultFileLocations)
        # verifyJSON will call exit() if it fails

    # Generate C/C++ Files
    print("Generating \"CANIDs.h\" for Helix-OBC-Firmware")
    with open ("../Helix-OBC-Firmware/inc/CANIDs.h", "w") as CAN_HEADER:
        CAN_HEADER.write(genCAN.getHeader(jsonData))

    print("Generating \"EEPROM_Layout.h\" for Helix-OBC-Firmware")
    headerEEPROMLAYOUT = genEEPROMLAYOUT.genEEPROMHEADER(jsonData)
    with open ("../Helix-OBC-Firmware/inc/EEPROM_Layout.h", "w") as EEPROM_LAYOUT_HEADER:
        EEPROM_LAYOUT_HEADER.write(headerEEPROMLAYOUT)

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
    
