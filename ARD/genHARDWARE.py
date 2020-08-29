import json, os, genGeneric

def getLatex(jsonData):
    """
    This function uses the HARDWARE config file to generate a latex file that
    can later be compiled into the ARD as the "Hardware" section.

    :param jsonData: Contains the json data loaded in from the config files
    :type  jsonData: Dict between the the config file and the JSON data that it contains

    :return: Latex file contents
    :rtype: string
    """
    # Sort hardware based on hardware type
    PTs = []
    TCs = []
    RTDs = []
    HEs = []
    for ID in jsonData['HARDWARE']:
        try:
            if (ID['Hardware Type'] == "Pressure Transducer"):
                PTs.append(ID)
            elif (ID['Hardware Type'] == "Thermocouple"):
                TCs.append(ID)
            elif (ID['Hardware Type'] == "RTD"):
                RTDs.append(ID)
            elif (ID['Hardware Type'] == "Hall Effect Sensor"):
                HEs.append(ID)
            else:
                print(f"Invalid ID Hardware Type: \"{ID['Hardware Type']}\"")
                return ""
        except KeyError:
            print("Invalid Key 'Hardware Type' in :")
            print(ID)
            return ""
    # Parse hardware configs to latex
    texHARDWARE = genHARDWARETex(PTs, TCs, RTDs, HEs, jsonData['EEPROM'])
    # Check for error in latex generation
    if (texHARDWARE == ""):
        return ""
    
    # Create latex
    texOut = ""
    texOut += genGeneric.autogenWarnStart("Hardware Config", os.path.abspath(__file__))
    texOut += "\section{Hardware}\n"
    texOut += texHARDWARE
    texOut += "\\newpage\n"
    texOut += genGeneric.autogenWarnEnd("Hardware Config", os.path.abspath(__file__))
    return texOut

def genHARDWARETex(PTs, TCs, RTDs, HEs, SEBconfigs):
    """
    Geneates the latex table for each of the given sensor.

    :param PTs: The pressure transducer definitions that should be converted into latex
    :type  PTs: dict
    :param TCs: The thermocouple definitions that should be converted into latex
    :type  TCs: dict
    :param RTDs: The RTD definitions that should be converted into latex
    :type  RTDs: dict
    :param HEs: The hall effect sensor definitions that should be converted into latex
    :type  HEs: dict
    :param SEBconfigs: List of all the extionsion board configs
    :type  SEBconfigs: list

    :return: Returns the latex for all of the sensors
    :rtype: string
    """
    texOut = ""

    # Parse pressure transducers
    texOut += "\subsection{Pressure Transducers}\n"
    for PT in PTs:
        try:
            texOut += "\\begin{adjustbox}{width=0.75\linewidth}\n"
            texOut += "\\begin{tabular}{|p{0.3\linewidth}|p{0.5\linewidth}|}\n\hline\n"
            texOut += "Model Number & " + PT['Model Number'] + "\\\\\hline\n"
            texOut += "Serial Number & " + PT['Serial Number'] + "\\\\\hline\n"
            
            # Check if hardware is used in SEBconfigs
            Usage = ""
            for config in SEBconfigs:
                for item in config:
                    if (item.find("PT") != -1):
                        if (config[item]['Serial Number'] == PT['Serial Number']):
                            Usage += "Usage & " + config[item]['Usage'] + "\\\\\hline\n"
            if (Usage == ""):
                texOut += "Usage & Unused\\\\\hline\n"
            else:
                texOut += Usage
                
            texOut += "Datasheet Link & \href{" + PT['Datasheet Link'] + "}{Link}\\\\\hline\n"
            texOut += "Sensing Units & " + PT['Sensing Units'] + "\\\\\hline\n"
            texOut += "Pressure Port Type & " + PT['Pressure Port Type'] + "\\\\\hline\n"
            texOut += "Accuracy & $" + PT['Accuracy'].replace("+-", "\pm").replace("%", "\%") + "$\\\\\hline\n"
            texOut += "Pressure Range & " + PT['Min Pressure'] + PT['Sensing Units'] + " to " + PT['Max Pressure'] + PT['Sensing Units'] + "\\\\\hline\n"
            texOut += "Sample Rate & " + PT['Sample Rate'] + "Hz\\\\\hline\n"
            texOut += "Output Voltage Range & " + PT['Min Output Voltage'] + " to " + PT['Max Output Voltage'] + " Volts\\\\\hline\n"
            texOut += "Input Voltage Range & " + PT['Min Input Voltage'] + " to " + PT['Max Input Voltage'] + " Volts\\\\\hline\n"
            texOut += "Temperature Range & " + PT['Min Temperature'] + "\degree to " + PT['Max Temperature'] + "\degree Celcius\\\\\hline\n"
            texOut += "\end{tabular}\n"
            texOut += "\end{adjustbox}\n"
            texOut += "\\newline\n\\vspace*{1em}\n\\newline\n"
        except KeyError as error:
            print("Missing required Key " + str(error) + " in hardware:")
            print(PT)
            return ""

    # Parse thermocouples
    texOut += "\subsection{Thermocouples}\n"
    for TC in TCs:
        try:
            texOut += "\\begin{adjustbox}{width=0.75\linewidth}\n"
            texOut += "\\begin{tabular}{|p{0.3\linewidth}|p{0.5\linewidth}|}\n\hline\n"
            texOut += "Model Number & " + TC['Model Number'] + "\\\\\hline\n"
            texOut += "Serial Number & " + TC['Serial Number'] + "\\\\\hline\n"
            
            # Check if hardware is used in SEBconfigs
            Usage = ""
            for config in SEBconfigs:
                for item in config:
                    if (item.find("TC") != -1):
                        if (config[item]['Serial Number'] == TC['Serial Number']):
                            Usage += "Usage & " + config[item]['Usage'] + "\\\\\hline\n"
            if (Usage == ""):
                texOut += "Usage & Unused\\\\\hline\n"
            else:
                texOut += Usage
            
            texOut += "Datasheet Link & \href{" + TC['Datasheet Link'] + "}{Link}\\\\\hline\n"
            texOut += "Type & " + TC['Type'] + "\\\\\hline\n"
            texOut += "Sensing Units & " + TC['Sensing Units'] + "\\\\\hline\n"
            texOut += "Sample Rate & " + TC['Sample Rate'] + "Hz\\\\\hline\n"
            texOut += "Temperature Range & " + TC['Min Temperature'] + "\degree to " + PT['Max Temperature'] + "\degree Celcius\\\\\hline\n"
            texOut += "\end{tabular}\n"
            texOut += "\end{adjustbox}\n"
            texOut += "\\newline\n\\vspace*{1em}\n\\newline\n"
        except KeyError as error:
            print("Missing required Key " + str(error) + " in hardware:")
            print(TC)
            return ""

    # Parse RTDs
    texOut += "\subsection{RTDs}\n"
    for RTD in RTDs:
        try:
            texOut += "\\begin{adjustbox}{width=0.75\linewidth}\n"
            texOut += "\\begin{tabular}{|p{0.3\linewidth}|p{0.5\linewidth}|}\n\hline\n"
            texOut += "Model Number & " + RTD['Model Number'] + "\\\\\hline\n"
            texOut += "Serial Number & " + RTD['Serial Number'] + "\\\\\hline\n"

            # Check if hardware is used in SEBconfigs
            Usage = ""
            for config in SEBconfigs:
                for item in config:
                    if (item.find("RTD") != -1):
                        if (config[item]['Serial Number'] == RTD['Serial Number']):
                            Usage += "Usage & " + config[item]['Usage'] + "\\\\\hline\n"
            if (Usage == ""):
                texOut += "Usage & Unused\\\\\hline\n"
            else:
                texOut += Usage

            texOut += "Datasheet Link & \href{" + RTD['Datasheet Link'] + "}{Link}\\\\\hline\n"
            texOut += "Type & " + RTD['Type'] + "\\\\\hline\n"
            texOut += "Sensing Units & " + RTD['Sensing Units'] + "\\\\\hline\n"
            texOut += "Sample Rate & " + RTD['Sample Rate'] + "Hz\\\\\hline\n"
            texOut += "Temperature Range & " + RTD['Min Temperature'] + "\degree to " + PT['Max Temperature'] + "\degree Celcius\\\\\hline\n"
            texOut += "\end{tabular}\n"
            texOut += "\end{adjustbox}\n"
            texOut += "\\newline\n\\vspace*{1em}\n\\newline\n"
        except KeyError as error:
            print("Missing required Key " + str(error) + " in hardware:")
            print(RTD)
            return ""

    # Parse hall effect sensors
    texOut += "\subsection{Hall Effect Sensors}\n"
    for HE in HEs:
        try:
            texOut += "\\begin{adjustbox}{width=0.75\linewidth}\n"
            texOut += "\\begin{tabular}{|p{0.3\linewidth}|p{0.5\linewidth}|}\n\hline\n"
            texOut += "Model Number & " + HE['Model Number'] + "\\\\\hline\n"
            texOut += "Serial Number & " + HE['Serial Number'] + "\\\\\hline\n"

            # Check if hardware is used in SEBconfigs
            Usage = ""
            for config in SEBconfigs:
                for item in config:
                    if (item.find("HE") != -1):
                        if (config[item]['Serial Number'] == HE['Serial Number']):
                            Usage += "Usage & " + config[item]['Usage'] + "\\\\\hline\n"
            if (Usage == ""):
                texOut += "Usage & Unused\\\\\hline\n"
            else:
                texOut += Usage
            texOut += "Datasheet Link & \href{" + HE['Datasheet Link'] + "}{Link}\\\\\hline\n"
            texOut += "Sensing Units & " + HE['Sensing Units'] + "\\\\\hline\n"
            texOut += "Output Type & " + HE['Output Type'] + "\\\\\hline\n"
            texOut += "Trip & $" + HE['Trip'].replace("+-", "\pm") + "$" + HE['Sensing Units'] + "\\\\\hline\n"
            texOut += "Release & $" + HE['Release'].replace("+-", "\pm") + "$" + HE['Sensing Units'] + "\\\\\hline\n"
            texOut += "Input Voltage Range & " + PT['Min Input Voltage'] + " to " + PT['Max Input Voltage'] + " Volts\\\\\hline\n"
            texOut += "Sample Rate & " + HE['Sample Rate'] + "Hz\\\\\hline\n"
            texOut += "Temperature Range & " + HE['Min Temperature'] + "\degree to " + PT['Max Temperature'] + "\degree Celcius\\\\\hline\n"
            texOut += "\end{tabular}\n"
            texOut += "\end{adjustbox}\n"
            texOut += "\\newline\n\\vspace*{1em}\n\\newline\n"
        except KeyError as error:
            print("Missing required Key " + str(error) + " in hardware:")
            print(HE)
            return ""

    return texOut