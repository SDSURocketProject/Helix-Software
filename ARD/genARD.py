import os
import genEEPROM
import genCAN
import genHARDWARE

if __name__ == "__main__":
    os.chdir("ARD/")
    
    # HARDWARE
    latexHARDWARE = genHARDWARE.getLatex()
    if (latexHARDWARE == ""):
        print("Failed to generate HARDWARE.tex, exiting...")
        quit()
    with open ("tex/HARDWARE.tex", "w") as HARDWARE_TEX:
        HARDWARE_TEX.write(latexHARDWARE)

    # CAN
    latexCAN = genCAN.getLatex()
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(latexCAN)
    
    headerCAN = genCAN.getHeader()
    with open ("../include/CANIDs.h", "w") as CAN_HEADER:
        CAN_HEADER.write(headerCAN)

    # EEPROM
    latexEEPROM = genEEPROM.getLatex()
    with open ("tex/EEPROM.tex", "w") as EEPROM_TEX:
        EEPROM_TEX.write(latexEEPROM)

    # Generate Tex
    if (os.system("xelatex --halt-on-error ARD.tex") != 0):
        print("Failed to create ARD.pdf.")
    else:
        print("ARD.pdf successfully written.")
    with open ("tex/EEPROM.tex", 'w') as EEPROM_TEX:
        EEPROM_TEX.write(genEEPROM.getLatex())