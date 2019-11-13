import json, os, genGeneric

def genEEPROM(filePath):
    texOut = ""
    texOut += genGeneric.autogenWarnStart("EEPROM Config", os.path.abspath(__file__))
	
    with open(filePath) as EEPROMConfigs:
        EEPROMLayouts = json.load(EEPROMConfigs)
    
    texOut += "\section{EEPROM Layouts}\n"
    texOut += genLayoutVersionIDs(EEPROMLayouts)

    for layout in EEPROMLayouts:
        texOut += genEEPROMTex(layout)
    
    
    texOut += genGeneric.autogenWarnEnd("EEPROM Config", os.path.abspath(__file__))
    return (texOut)

def genLayoutVersionIDs(layouts):
    texOut = ""
    texOut += "\subsection{Layout Version IDs}\n"
    texOut += "\\begin{tabular}{ |l|l| }\n"
    texOut += "\\hline\n"
    texOut += "VersionID & Version Name \\\\\\hline\n"
    for layout in layouts:
        texOut += layout["VersionID"] + " & " + layout["VersionName"] + " \\\\\\hline\n"
    texOut += "\end{tabular}\n"
    texOut += "\\newpage\n\n"
    return texOut

def genEEPROMTex(layout):
    texOut = ""
    texOut += "\subsection{" + layout["VersionName"] + "}\n"

    # data is a list of lists
    # data[x] references each line in table
    # data[x][0] is the text that goes into that table
    # data[x][1] specifies if \cline needs to be added for the latex
    data = []
    byteCounter = 0
    for index in layout["Data"]:
        if (index["Size"] == 1):
            data.append([f"{byteCounter} & " + index["Name"], True])
            byteCounter = byteCounter + byteCounter
        else:
            data.append([str(byteCounter) + " & \multirow{" + str(index["Size"]) + "}{0.9\linewidth}{\centering " + index["Name"] + "}", False])
            byteCounter = byteCounter + 1
            # Loop through rest of multirow
            for i in range(index["Size"]-2, -1, -1):
                data.append([f"{byteCounter} & ", (i == 0)])
                byteCounter = byteCounter + 1

    NumBytesPerPage = 128
    NumColumns = 3
    BytesPerColumn = 0
    if (NumColumns == 2):
        BytesPerColumn = 64
    elif (NumColumns == 3):
        BytesPerColumn = 48

    totalPages = int(len(data)/NumBytesPerPage) + 1
    while (len(data) < NumBytesPerPage*totalPages):
        data.append([f"{byteCounter} & ", False])
        byteCounter = byteCounter + 1
    
    for page in range(totalPages):
        texOut += "{\\tiny\n"
        texOut += "\\begin{adjustbox}{width=1\\textwidth}\n"
        if (NumColumns == 2):
            texOut += "\\begin{tabular}{ |l|l||l|l| }\n"
        elif (NumColumns == 3):
            texOut += "\\begin{tabular}{ |p{0.05\linewidth}|p{0.15\linewidth}||p{0.05\linewidth}|p{0.15\linewidth}||p{0.05\linewidth}|p{0.15\linewidth}| }\n"
        texOut += "\hline\n"
        texOut += "\multicolumn{" + str(NumColumns*2) + "}{|c|}{" + layout["VersionName"] + " Page \#" + str(page) + "} \\\\\hline\n"
        texOut += "Byte \# & Usage & "*NumColumns
        texOut = texOut[:-3]
        texOut += " \\\\\hline\n"
        for i in range(NumBytesPerPage*page, (BytesPerColumn)+NumBytesPerPage*page):
            for j in range(NumColumns):
                if (i+j*(BytesPerColumn) >= NumBytesPerPage):
                    texOut += " & & "
                else:
                    texOut += data[i+j*(BytesPerColumn)][0] + " & "
            texOut = texOut[:-3]
            texOut += " \\\\ "
            for j in range(NumColumns):
                if (i+j*(BytesPerColumn) >= NumBytesPerPage):
                    continue
                if (i+j*(BytesPerColumn) == NumBytesPerPage-1):
                    texOut += "\cline{" + str(1+j*2) + "-" + str(2+j*2) + "} "
                elif (data[i+j*(BytesPerColumn)][1]):
                    texOut += "\cline{" + str(1+j*2) + "-" + str(2+j*2) + "} "
            texOut += "\n"
        texOut += "\hline\n"
        texOut += "\end{tabular}\\\\\n"
        texOut += "\\end{adjustbox}\n"
        texOut += "} % end tiny\n"
        texOut += "\\newpage\n\n"
    return texOut

if __name__ == "__main__":
    pass