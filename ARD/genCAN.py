import json, os, genGeneric, math

def getLatex(jsonData):
    texOut = ""
    texOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__))
    
    texOut += "\section{CAN IDs}\n"

    texOut += "\subsection{CAN Bus Load Calculations}\n"
    canBusFrequencies = [100000, 250000, 500000, 1000000]
    bestCase, worstCase = getCANBusLoad(jsonData['CAN'])
    texOut += "The current CAN Bus config requires between " + str(bestCase) + " bits and " + str(worstCase) + " bits to be sent on the CAN bus every second.\n\n"
    texOut += "\\begin{flushleft}"
    texOut += "\\begin{tabular}{|c|c|c|}\hline\n"
    texOut += "\tFrequency & Best Case & Worst Case \\\\\hline\n"
    for frequency in canBusFrequencies:
        texOut += "\t"
        if (frequency >= 1000000):
            texOut += str(int(frequency/1000000)) + "MHz"
        elif (frequency >= 1000):
            texOut += str(int(frequency/1000)) + "KHz"
        else:
            texOut += str(int(frequency)) + "Hz"
        
        texOut += " & " + str(round(bestCase / frequency, 2)*100) + "\% & " + str(round(worstCase / frequency, 2)*100) + "\%\\\\\hline\n"
    texOut += "\end{tabular}\n"
    texOut += "\end{flushleft}"
    for ID in jsonData['CAN']:
        texOut += genCANTex(ID)


    
    texOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__))
    
    return texOut

def getHeader(jsonData):
    headerOut = ""
    headerOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__), commentChar="//")

    headerOut += genCANHeader(jsonData['CAN'], jsonData['STATES'])

    headerOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__), commentChar="//")
    return headerOut

def genCANTex(config):
    texOut = ""

    texOut += "\subsection{ID " + config["CANID"] + " - " + config["CANID_NAME"] +"}\n"
    texOut += "Frequency: " + config["CANID_FREQUENCY"] + "Hz\\\\\n"
    texOut += "\\begin{tabular}{ |p{0.05\linewidth}|p{0.05\linewidth}|p{0.1\linewidth}|p{0.15\linewidth}|p{0.2\linewidth}|p{0.3\linewidth}| }\hline\n"
    texOut += "Byte & Bit & Signed & Range & Units & Description\\\\\hline\n"
    
    byteIdxLow = 0
    byteIdxHigh = 0
    ByteStr = ""
    BitStr = ""
    SignedStr = ""
    UnitsStr = ""
    DescriptionStr = ""
    for byteDef in config["bytes"]:
        byteIdxHigh = byteIdxLow+byteDef["Size"]-1
        if (byteIdxHigh == byteIdxLow):
            texOut += str(byteIdxHigh) + " & "
        else:
            texOut += str(byteIdxLow) + "-" + str(byteIdxHigh) + " & "
        byteIdxLow = byteIdxLow+byteDef["Size"]
        
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
        texOut += byteDef["Name"]

        texOut += "\\\\\hline\n"
        if ("bits" in byteDef):
            for bitDef in byteDef["bits"]:
                for i in bitDef:
                    texOut += " & " + i + " & & & & " + bitDef[i] + "\\\\\hline\n"
        
    
    texOut += "\end{tabular}\n"
    return texOut

def genCANHeader(config, states):
    headerOut = ""
    headerOut += "#ifndef CANIDS_H_\n"
    headerOut += "#define CANIDS_H_\n\n"

    headerOut += "#include <linux/can.h>\n"
    headerOut += "#include <stdint.h>\n\n"

    headerOut += "enum STATES {\n"
    for state in states:
        headerOut += "\t" + genGeneric.makeCName(state, "#define") + ",\n"
    headerOut += "\tSTATE_MAX_STATES\n"
    headerOut += "};\n\n"

    headerOut += "enum CANIDs : uint32_t {\n"
    for CANID in config:
        headerOut += "\tCANIDS_" + genGeneric.makeCName(CANID["CANID_NAME"], "#define") + " = " + CANID["CANID"] + "UL,\n"
    headerOut += "\tCANIDS_QUIT,\n"
    headerOut += "\tCANIDS_MAX_CANID\n"
    headerOut += "};\n\n"

    for CANID in config:
        headerOut += "struct " + genGeneric.makeCName(CANID["CANID_NAME"], "variable") + " {\n"
        for byteDef in CANID["bytes"]:
            headerOut += "\t" + canIDByteToStdInt(byteDef) + " " + genGeneric.makeCName(byteDef["Name"], "variable") + ";\n"
        headerOut += "};\n\n"

    headerOut += "#endif // CANIDS_H_\n"
    return headerOut

def getCANBusLoad(canIDs):
    # Calculate the total number of bits that need to be transmitted per second
    minimumBits = 0
    maximumBits = 0
    for ID in canIDs:
        minimumBits = minimumBits + 1 # Start bit
        minimumBits = minimumBits + 11 # Identifier
        minimumBits = minimumBits + 1 # RTR bit
        minimumBits = minimumBits + 6 # Control Field

        # Calculate the number of bits in the message to send
        IDbitsPerSecond = 0
        for dataField in ID['bytes']:
            IDbitsPerSecond = IDbitsPerSecond + int(dataField['Size'])*8
        # Multiple by the number of times this ID will be sent per second
        IDbitsPerSecond = IDbitsPerSecond*int(ID['CANID_FREQUENCY'])

        minimumBits = minimumBits + IDbitsPerSecond # Payload
        minimumBits = minimumBits + 15 # CRC

        maximumBits = minimumBits + math.floor(minimumBits*0.2) # Worst case bit stuffing

        minimumBits = minimumBits + 1 # CRC delimiter
        minimumBits = minimumBits + 1 # ACK Slot
        minimumBits = minimumBits + 1 # ACK delimiter
        minimumBits = minimumBits + 7 # End of Frame

        maximumBits = maximumBits + 1 # CRC delimiter
        maximumBits = maximumBits + 1 # ACK Slot
        maximumBits = maximumBits + 1 # ACK delimiter
        maximumBits = maximumBits + 7 # End of Frame
    
    return (minimumBits, maximumBits)

# Go from byte definition to standard stdint.h value (ie unsigned 4 byte in -> uint32_t)
def canIDByteToStdInt(byteDef):
    valOut = ""
    if (byteDef["Signed"] == "False"):
        valOut += "u"
    valOut += "int" + str(byteDef["Size"]*8) + "_t"
    return valOut

if __name__ == "__main__":
    pass