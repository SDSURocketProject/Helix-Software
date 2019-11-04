import os
import genEEPROM
import genCANJSON as genCAN

if __name__ == "__main__":

    latexCAN, headerCAN = genCAN.getConfig("config/CAN.json")
    with open ("tex/CANIDs.tex", "w") as CAN_TEX:
        CAN_TEX.write(latexCAN)
    with open ("include/CANIDs.h", "w") as CAN_HEADER:
        CAN_HEADER.write(headerCAN)
    #with open ("tex/EEPROM.tex", 'w') as EEPROM_TEX:
    #    EEPROM_TEX.write(genEEPROM.genEEPROM("config/EEPROM.cfg"))