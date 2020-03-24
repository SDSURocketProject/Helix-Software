import json

NOT_IN_CANID_DEF = 0
IN_CANID_DEF = 1

def getLatex():
    texOut = ""
    texOut += "\section{States}\n"
    parseState = NOT_IN_CANID_DEF

    with open("config/STATES.json") as statesJSON:
        states = json.load(statesJSON)

    for state in states:
        try:
            with open ("../Helix-OBC-Firmware/documentation/latex/group__" + state.lower() + "_group.tex", 'r') as readFile:
                texOut += "\subsection{" + state.replace('_', ' ') + "}\n"
                # Go through every line only appending lines to texOut if they are between lines containing the CANID_DEF and END_CANID_DEF tags
                for line in readFile:
                    # Don't include the line that says END_CANID_DEF
                    if (line.find("END_CANID_DEF") != -1):
                        parseState = NOT_IN_CANID_DEF
                        continue

                    if (parseState == IN_CANID_DEF):
                        texOut += line

                    if (line.find("CANID_DEF") != -1):
                        parseState = IN_CANID_DEF
                        texOut += "\subsubsection{" + line[line.find("(")+1:line.find(")")] + "}\n"
        except FileNotFoundError:
            print("Latex for " + state + " not found... skipping")
    
    return texOut