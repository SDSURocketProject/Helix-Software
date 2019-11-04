import json, os, genGeneric

def getConfig(filePath):
    latexOut = ""
    headerOut = ""
    latexOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__))
    headerOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__), commentChar="//")
	
    with open(filePath) as canIDs:
        data = json.load(canIDs)
    
    for ID in data:
        latexOut += genCANTex(ID)
    
    latexOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__))
    headerOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__), commentChar="//")
    return (latexOut, headerOut)

def genCANTex(config):
    texOut = ""

    texOut += "\subsection{ID " + config["CANID"] + " - " + config["CANID_NAME"] +"}\n"
    texOut += "Frequency: " + config["CANID_FREQUENCY"] + "Hz\n"
    texOut += "\setlength{\LTleft}{0pt}\n"

    return texOut

def genCANHeader(config):
    headerOut = ""
    return headerOut

if __name__ == "__main__":
    pass