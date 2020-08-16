import json, os, genGeneric

def getLatex(jsonData):
    texOut = ""
    texOut += genGeneric.autogenWarnStart("EEPROM Layouts", os.path.abspath(__file__))
    
    texOut += "\section{EEPROM Layouts}\n"
    texOut += genLayoutVersionIDs(jsonData['EEPROMLAYOUT'])

    for layout in jsonData['EEPROMLAYOUT']:
        texOut += genEEPROMTex(layout)
    
    texOut += genGeneric.autogenWarnEnd("EEPROM Layouts", os.path.abspath(__file__))
    return texOut

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
                if (i+j*(BytesPerColumn) >= NumBytesPerPage*(1+page)):
                    texOut += " & & "
                else:
                    texOut += data[i+j*(BytesPerColumn)][0] + " & "
            texOut = texOut[:-3]
            texOut += " \\\\ "
            for j in range(NumColumns):
                if (i+j*(BytesPerColumn) >= NumBytesPerPage*(1+page)):
                    continue
                if (i+j*(BytesPerColumn) == NumBytesPerPage*(1+page)-1):
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

def genEEPROMHEADER(jsonData):
    headerOut = ""
    headerOut += genGeneric.autogenWarnStart("EEPROM Layout Config", os.path.abspath(__file__), commentChar="//")
    headerOut += "\n#ifndef EEPROM_LAYOUT_HEADER_H_\n"
    headerOut += "#define EEPROM_LAYOUT_HEADER_H_\n\n"
    headerOut += "#include <stdint.h>\n\n"

    layoutVersionIDs = {}
    # Create struct definitions
    for layout in jsonData['EEPROMLAYOUT']:
        layoutVersionIDs[int(layout['VersionID'])] = layout['VersionName'].lower().replace(" ", "_")

        headerOut += "// EEPROM Layout Version ID " + layout['VersionID'] + "\n"
        headerOut += "struct " + genGeneric.makeCName(layout['VersionName'], "variable") + " {\n"
        for memLoc in layout['Data']:
            # Create variable type
            if (memLoc['Data Type'] == "H" or memLoc['Data Type'] == "I" or memLoc['Data Type'] == "L" or memLoc['Data Type'] == "Q"):
                headerOut += "\tuint" + str(int(memLoc['Size'])*8) + "_t "
            elif (memLoc['Data Type'] == "h" or memLoc['Data Type'] == "i" or memLoc['Data Type'] == "l" or memLoc['Data Type'] == "q"):
                headerOut += "\tint" + str(int(memLoc['Size'])*8) + "_t "
            elif (memLoc['Data Type'] == "f"):
                headerOut += "\tfloat "
            elif (memLoc['Data Type'] == "d"):
                headerOut += "\tdouble "
            elif (memLoc['Data Type'] == "c"):
                headerOut += "\tchar "
            elif (memLoc['Data Type'] == "s" or memLoc['Data Type'] == "p"):
                headerOut += "\tchar[] "
            elif (memLoc['Data Type'] == "P"):
                headerOut += "\tvoid *"
            # Add name after variable type
            headerOut += memLoc['Name'].replace(" ", "_") + ";\n"
        headerOut += "}" + " __attribute((aligned (1)))" + "; // " + genGeneric.makeCName(layout['VersionName'], "variable") + "\n\n"

    # Create enum of versionIDs
    headerOut += "enum layoutVersionIDs {\n"
    for ID in layoutVersionIDs:
        headerOut += "\t" + genGeneric.makeCName(layoutVersionIDs[ID], "#define") + ", \t // " + str(ID) + "\n"
    headerOut += "\tMAX_LAYOUT_VERSION_IDS\n"
    headerOut += "};\n\n"

    headerOut += "\n#endif // EEPROM_LAYOUT_HEADER_H_\n\n"
    headerOut += genGeneric.autogenWarnEnd("EEPROM Layout Config", os.path.abspath(__file__), commentChar="//")
    return headerOut

if __name__ == "__main__":
    pass