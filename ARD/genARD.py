import os
import genEEPROMLAYOUT
import genEEPROM
import genCAN
import genHARDWARE
import parseOBCDocs

if __name__ == "__main__":
    #os.chdir("ARD/")
    
    # HARDWARE
    latexHARDWARE = genHARDWARE.getLatex()
    if (latexHARDWARE == ""):
        print("Failed to generate HARDWARE.tex, exiting...")
        quit()
    with open ("tex/HARDWARE.tex", "w") as HARDWARE_TEX:
        HARDWARE_TEX.write(latexHARDWARE)

    # STATES
    latexSTATES = parseOBCDocs.getLatex()
    if (latexSTATES == ""):
        print("Failed to get documentation from Helix-OBC-Firmware documentation, exiting...")
        quit()
    with open ("tex/STATES.tex", "w") as STATES_TEX:
        STATES_TEX.write(latexSTATES)

    # CAN
    latexCAN = genCAN.getLatex()
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(latexCAN)

    # EEPROM
    latexEEPROMLAYOUT = genEEPROMLAYOUT.getLatex()
    with open ("tex/EEPROMLAYOUT.tex", "w") as EEPROMLAYOUT_TEX:
        EEPROMLAYOUT_TEX.write(latexEEPROMLAYOUT)

    # Generate Tex
    if (os.system("xelatex --halt-on-error ARD.tex") != 0):
        print("Failed to create ARD.pdf.")
    else:
        print("ARD.pdf successfully written.")
    with open ("tex/EEPROMLAYOUT.tex", 'w') as EEPROMLAYOUT_TEX:
        EEPROMLAYOUT_TEX.write(genEEPROMLAYOUT.getLatex())

    # Generate Binary Files
    genEEPROM.genEEPROMBIN()

    # Generate C/C++ Files
    headerCAN = genCAN.getHeader()
    with open ("../include/CANIDs.h", "w") as CAN_HEADER:
        CAN_HEADER.write(headerCAN)

    headerEEPROMLAYOUT = genEEPROMLAYOUT.genEEPROMHEADER()
    with open ("../include/EEPROM_Layout.h", "w") as EEPROM_LAYOUT_HEADER:
        EEPROM_LAYOUT_HEADER.write(headerEEPROMLAYOUT)
    