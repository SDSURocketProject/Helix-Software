import genGeneric, os, re

paramsIdx = 0
CANBytesIdx = 1
CANBitsIdx = 2

def getConfig(filePath):
	config = ""
	with open(filePath, 'r') as canConfig:
		config = canConfig.readlines()
	# Filter out lines that start with "#" as first non whitespace character
	config = [value for value in config if value.lstrip() == "" or value.lstrip()[0] != "#"]
	# Combine all lines into one string
	config = "".join(config)
	# Separate CANIDs by beginID tag
	IDConfigs = config.split("\\beginID")
	# Remove trailing endID tag
	IDConfigs = [value.split("\endID")[0] for value in IDConfigs]
	# Remove empty strings
	IDConfigs = [value for value in IDConfigs if value != '']
	# Parse all configs into basic components
	IDConfigs = [parseConfig(value) for value in IDConfigs]
	
	latexOut = ""
	headerOut = ""
	latexOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__))
	headerOut += genGeneric.autogenWarnStart("CAN Config", os.path.abspath(__file__), commentChar="//")
	for ID in IDConfigs:
		#latexOut += genCANTex(ID)
		headerOut += genCANHeader(ID)
	latexOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__))
	headerOut += genGeneric.autogenWarnEnd("CAN Config", os.path.abspath(__file__), commentChar="//")
	return (latexOut, headerOut)

def parseConfig(config):
	params = re.findall(r'param\s+(.*)=\"(.*)\"', config)
	CANBytes = re.findall(r'bytes\s+(.*)\s+\"(.*)\"\s+Units=\"(.*)\"', config)
	CANBits = re.findall(r'bits\s+(\d+)\s+BYTE=\"(.*)\"\s+NAME=\"(.*)\"\s+DESCRIPTION=\"(.*)\"\s+VALUES=\"(.*)\"', config)
	CANBitDefs = re.findall(r'bitdef\s+(.*)=\"(.*)\"', config)

	paramDict = {}
	for param in params:
		paramDict[param[0]] = param[1]
	
	if "CANID" not in paramDict:
		print("Missing CANID in layout\n")
		raise Exception()
	if "CANID_NAME" not in paramDict:
		print("Missing CANID_NAME in layout\n")
		raise Exception()
	if "CANID_FREQUENCY" not in paramDict:
		print("Missing CANID_FREQUENCY in layout\n")
		raise Exception()
	
	for byteDef in CANBytes:
		if byteDef[2] == "BITDEF":
			pass

	return (paramDict, CANBytes, CANBits)

def genCANTex(config):
	texOut = ""
	texOut += "\subsection{ID " + config[paramsIdx]["CANID"] + " - " + config[paramsIdx]["CANID_NAME"] +"}\n"
	texOut += "Frequency: " + config[paramsIdx]["CANID_FREQUENCY"] + "Hz\n"
	texOut += "\setlength{\LTleft}{0pt}\n"
	texOut += "    \\begin{longtable}{|c|c|c|} \\hline\n"
	texOut += "    bytes & Units & Description \\\\ \hline\n"
	byteCounterLow = 0
	byteCounterHigh = -1
	for CANBytes in config[CANBytesIdx]:
		byteCounterHigh = byteCounterHigh+int(CANBytes[0])
		texOut += f"    [{byteCounterHigh}:{byteCounterLow}] & {CANBytes[1]} & {CANBytes[2]} \\\\ \hline\n"
		byteCounterLow = byteCounterHigh+1
	texOut += "\end{longtable}\n"
	texOut += "\pagebreak\n"

	return texOut

def genCANHeader(config):
	headerOut = ""

	return headerOut

if __name__ == "__main__":
	pass