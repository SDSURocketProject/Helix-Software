import os
import sys
import genEEPROMLAYOUT
import genEEPROM
import genCAN
import genHARDWARE
import parseOBCDocs

if __name__ == "__main__":
    #os.chdir("ARD/")

    # Generate C/C++ Files
    print("Generating \"CANIDs.h\" for Helix-OBC-Firmware")
    headerCAN = genCAN.getHeader()
    with open ("../Helix-OBC-Firmware/inc/CANIDs.h", "w") as CAN_HEADER:
        CAN_HEADER.write(headerCAN)

    print("Generating \"EEPROM_Layout.h\" for Helix-OBC-Firmware")
    headerEEPROMLAYOUT = genEEPROMLAYOUT.genEEPROMHEADER()
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
    latexHARDWARE = genHARDWARE.getLatex()
    if (latexHARDWARE == ""):
        print("Failed to generate HARDWARE.tex, exiting...")
        quit()
    with open ("tex/HARDWARE.tex", "w") as HARDWARE_TEX:
        HARDWARE_TEX.write(latexHARDWARE)

    print("Generating \"tex/STATES.tex\"")
    # STATES
    latexSTATES = parseOBCDocs.getLatex()
    if (latexSTATES == ""):
        print("Failed to get documentation from Helix-OBC-Firmware documentation, exiting...")
        quit()
    with open ("tex/STATES.tex", "w") as STATES_TEX:
        STATES_TEX.write(latexSTATES)

    # CAN
    print("Generating \"tex/CANIDs.tex\"")
    latexCAN = genCAN.getLatex()
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(latexCAN)

    # EEPROM
    print("Generating \"tex/EEPROMLAYOUT.tex\"")
    latexEEPROMLAYOUT = genEEPROMLAYOUT.getLatex()
    with open ("tex/EEPROMLAYOUT.tex", "w") as EEPROMLAYOUT_TEX:
        EEPROMLAYOUT_TEX.write(latexEEPROMLAYOUT)

    # Generate Tex
    print("Generating \"ARD.pdf\"")
    if (os.system("xelatex --halt-on-error ARD.tex") != 0):
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
    genEEPROM.genEEPROMBIN()
    