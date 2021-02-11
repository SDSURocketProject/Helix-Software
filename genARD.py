import os
import sys
import json
import genEEPROMLAYOUT
import genEEPROM
import genCAN
import genHARDWARE
import parseOBCDocs
import verifyJSON

def loadJSONFiles(defaultFileLocations):
    """Loads the JSON data in from the config files.

    :param defaultFileLocations: Contains the file locations that the outputs should be written to
    :type  defaultFileLocations: Dict between the command line argument for the file and the path to the file

    :return: The json data loaded in from the config files
    :rtype: Dict between the the config file and the JSON data that it contains
    """

    jsonData = {
        "CAN":[],
        "EEPROM":[],
        "EEPROMLAYOUT":[],
        "FILTERS":[],
        "HARDWARE":[],
        "STATES":[]
    }
    fileLocToJson = {
        "--can-file":"CAN",
        "--eeprom-file":"EEPROM",
        "--eepromlayout-file":"EEPROMLAYOUT",
        "--filters-file":"FILTERS",
        "--hardware-file":"HARDWARE",
        "--states-file":"STATES"
    }
    try:
        for key in defaultFileLocations:
            if key not in fileLocToJson:
                continue
            openingFile = defaultFileLocations[key]
            data = open(defaultFileLocations[key], 'r')
            jsonData[fileLocToJson[key]] = json.load(data)
            data.close()
    except:
        print(f"File {openingFile} does not exist.")
    
    return jsonData


def genC(defaultFileLocations, jsonData):
    """Generates the C/C++ header files that are needed by the flight software
    projects.

    :param defaultFileLocations: Contains the file locations that the outputs should be written to
    :type  defaultFileLocations: Dict between the command line argument for the file and the path to the file
    :param jsonData: Contains the json data loaded in from the config files
    :type  jsonData: Dict between the the config file and the JSON data that it contains

    :return: Returns nothing
    """
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


def genTex(defaultFileLocations, jsonData):
    """Generates the latex files that are needed by xelatex to generate ARD.pdf.

    :param defaultFileLocations: Contains the file locations that the outputs should be written to
    :type  defaultFileLocations: Dict between the command line argument for the file and the path to the file
    :param jsonData: Contains the json data loaded in from the config files
    :type  jsonData: Dict between the the config file and the JSON data that it contains

    :return: Returns nothing
    """

    # HARDWARE
    print("Generating \"tex/HARDWARE.tex\"")
    latexHARDWARE = genHARDWARE.getLatex(jsonData)
    if (latexHARDWARE == ""):
        print("Failed to generate HARDWARE.tex, exiting...")
        quit()
    with open ("tex/HARDWARE.tex", "w") as HARDWARE_TEX:
        HARDWARE_TEX.write(latexHARDWARE)

    # CAN
    print("Generating \"tex/CANIDs.tex\"")
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(genCAN.getLatex(jsonData))

    # EEPROM
    print("Generating \"tex/EEPROMLAYOUT.tex\"")
    with open ("tex/EEPROMLAYOUT.tex", "w") as EEPROMLAYOUT_TEX:
        EEPROMLAYOUT_TEX.write(genEEPROMLAYOUT.getLatex(jsonData))


def genARD():
    """This is the "main" function for generating the Avionics Reference
    Document (ARD). This gets all of the config data and calls functions for
    generating the ARD outputs.

    :return: Returns nothing
    """
    defaultFileLocations = {
        "--can-file":"config/CAN.json",
        "--eeprom-file":"config/EEPROM.json",
        "--eepromlayout-file":"config/EEPROMLAYOUT.json",
        "--filters-file":"config/FILTERS.json",
        "--hardware-file":"config/HARDWARE.json",
        "--states-file":"config/STATES.json",
        "--CANIDs-header":"headers/CANIDs.h",
        "--eepromlayout-header":"headers/EEPROM_Layout.h"
    }

    # Override default file locations if specified in command line args
    for location in defaultFileLocations:
        if location in sys.argv:
            defaultFileLocations[location] = sys.argv[sys.argv.find(location)+1]

    jsonData = loadJSONFiles(defaultFileLocations)

    if ("--skip-verify" not in sys.argv):
        print("Verifying JSON files are valid")
        verifyJSON.verifyJSON(jsonData, defaultFileLocations)
        # verifyJSON will call exit() if it fails

    genC(defaultFileLocations, jsonData)

    if ("--headers-only" in sys.argv):
        exit(0)
    
    # Create tex directory if it doesn't already exist
    try:
        os.mkdir("tex")
    except FileExistsError:
        pass

    genTex(defaultFileLocations, jsonData)

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

    print()
    

if __name__ == "__main__":
    genARD()