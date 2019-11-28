import os
import genEEPROM as genEEPROM
import genCAN as genCAN
import genHARDWARE

if __name__ == "__main__":
    os.chdir("ARD/")
    
    # HARDWARE
    latexHARDWARE = genHARDWARE.getConfig("config/HARDWARE.json")
    with open ("tex/HARDWARE.tex", "w") as HARDWARE_TEX:
        HARDWARE_TEX.write(latexHARDWARE)

    # CAN
    latexCAN, headerCAN = genCAN.getConfig("config/CAN.json")
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(latexCAN)
    with open ("../include/CANIDs.h", "w") as CAN_HEADER:
        CAN_HEADER.write(headerCAN)

    # EEPROM
    latexEEPROM = genEEPROM.genEEPROM("config/EEPROM.json")
    with open ("tex/EEPROM.tex", "w") as EEPROM_TEX:
        EEPROM_TEX.write(latexEEPROM)

    # Generate Tex
    if (os.system("xelatex --halt-on-error ARD.tex") != 0):
        print("Failed to create ARD.pdf.")
    else:
        print("ARD.pdf successfully written.")
    with open ("tex/EEPROM.tex", 'w') as EEPROM_TEX:
        EEPROM_TEX.write(genEEPROM.genEEPROM("config/EEPROM.json"))