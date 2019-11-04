import json, os, genGeneric

def getConfig(filePath):
    texOut = ""
    headerOut = ""
    texOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__))
    headerOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__), commentChar="//")
	
    with open(filePath) as canIDs:
        data = json.load(canIDs)
    
    texOut += "\section{CAN IDs}\n"
    for ID in data:
        texOut += genCANTex(ID)
    
    
    texOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__))
    headerOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__), commentChar="//")
    return (texOut, headerOut)

def genCANTex(config):
    texOut = ""

    texOut += "\subsection{ID " + config["CANID"] + " - " + config["CANID_NAME"] +"}\n"
    texOut += "Frequency: " + config["CANID_FREQUENCY"] + "Hz\\\\\n"
    texOut += "\\begin{tabular}{ |l|l|l|l|l|l| }\hline\n"
    texOut += "Byte & Bit & Signed & Range & Units & Description\\\\\hline\n"
    
    byteIdxLow = 0
    byteIdxHigh = 0
    ByteStr = ""
    BitStr = ""
    SignedStr = ""
    UnitsStr = ""
    DescriptionStr = ""
    for byteDef in config["bytes"]:
        if ("Size" in byteDef):
            byteIdxHigh = byteIdxLow+byteDef["Size"]-1
            if (byteIdxHigh == byteIdxLow):
                texOut += str(byteIdxHigh) + " & "
            else:
                texOut += str(byteIdxLow) + "-" + str(byteIdxHigh) + " & "
            byteIdxLow = byteIdxLow+byteDef["Size"]
        else:
            texOut += " & "
        texOut += " & " # Bit
        if ("Signed" in byteDef):
            texOut += byteDef["Signed"] + " & "
        else:
            texOut += " & "
        if ("MinValue" in byteDef and "MaxValue" in byteDef):
            texOut += str(byteDef["MinValue"]) + " to " + str(byteDef["MaxValue"]) + " & "
        else:
            texOut += " & "
        if ("Units" in byteDef):
            texOut += byteDef["Units"] + " & "
        else:
            texOut += " & "
        if ("Name" in byteDef):
            texOut += byteDef["Name"]
        else:
            texOut += " & "

        texOut += "\\\\\hline\n"
        if ("bits" in byteDef):
            for bitDef in byteDef["bits"]:
                for i in bitDef:
                    texOut += " & " + i + " & & & & " + bitDef[i] + "\\\\\hline\n"
        
    
    texOut += "\end{tabular}\n"
    return texOut

def genCANHeader(config):
    headerOut = ""
    return headerOut

if __name__ == "__main__":
    pass