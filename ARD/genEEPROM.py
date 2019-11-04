import genGeneric, os, re

def genEEPROM(eepromConfigPath):
	latexOut = ""
	config = ""
	with open(eepromConfigPath, 'r') as EEPROM_CONFIG:
		for line in EEPROM_CONFIG:
			if (line.lstrip() == ""):
				continue
			if (line.lstrip()[0] == "#"):
				continue
			config += line


	configLayouts = config.split("\\beginLayout\n")
	
	layout = ""
	layouts = []
	VersionID = ""
	VersionIDs = []
	VersionName = ""
	VersionNames = []
	for configLayout in configLayouts:
		if (configLayout != ""):
			layout, VersionID, VersionName = genLayout3(configLayout)
			layouts.append(layout)
			VersionIDs.append(VersionID)
			VersionNames.append(VersionName)
	

	latexOut += genGeneric.autogenWarnStart("EEPROM Config", os.path.abspath(__file__))
	latexOut += "\section{EEPROM}\n"
	latexOut += "\subsection{Layout Version IDs}\n"
	latexOut += "\\begin{tabular}{ |l|l| }\n"
	latexOut += "\hline\n"
	latexOut += "VersionID & Version Name \\\\\hline\n"
	for i in range(len(VersionIDs)):
		latexOut += VersionIDs[i] + " & " + VersionNames[i] + " \\\\\hline\n"
	latexOut += "\end{tabular}\n"
	for layout in layouts:
		latexOut += layout
	latexOut += genGeneric.autogenWarnEnd("EEPROM Config", os.path.abspath(__file__))
	latexOut += "\pagebreak"
	return latexOut

def genLayout(layoutConfig):
	layout = ""

	params = re.findall(r'param (.*)=\"(.*)\"', layoutConfig)
	locations = re.findall(r'location (\d) \"(.*)\"', layoutConfig)

	paramDict = {}
	for param in params:
		paramDict[param[0]] = param[1]
	
	if "VersionID" not in paramDict:
		# Error
		pass
	if "VersionName" not in paramDict:
		# Error
		pass

	layout += "\subsection{Layout " + paramDict["VersionName"] + "}\n"
	layout += "\\begin{tabular}{ |l|l| }\n"
	layout += "\hline\n"
	layout += "Byte \# & Usage \\\\\n"
	layout += "\hline\n"
	layout += "0 & \multirow{4}{*}{Layout Version ID (" + paramDict["VersionID"] + ")} \\\\\n"
	layout += "1 & \\\\\n"
	layout += "2 & \\\\\n"
	layout += "3 & \\\\\n"
	layout += "\hline\n"
	byteCounter = 4
	
	tableNum = 1
	for location in locations:
		# Check if adding new location will write past end of the current table
		if (int(location[0])+byteCounter > tableNum*48):
			tableNum = tableNum + 1
			layout += "\end{tabular}\n"
			layout += "\\begin{tabular}{ |l|l| }\n"
			layout += "\hline\n"
			layout += "Byte \# & Usage \\\\\n"
			layout += "\hline\n"
		layout += str(byteCounter) + " & \multirow{" + location[0] + "}{*}{" + location[1] + "} \\\\\n"
		byteCounter = byteCounter + 1
		for i in range(int(location[0]) - 1):
			layout += str(byteCounter) + " & \\\\\n"
			byteCounter = byteCounter + 1
		layout += "\hline\n"
	
	# Fill remaining bytes in page with reserved
	for i in range(byteCounter, 128+byteCounter-(byteCounter % 128)):
		# Check if adding new location will write past end of the current table
		if (1+i > tableNum*48):
			tableNum = tableNum + 1
			layout += "\end{tabular}\n"
			layout += "\\begin{tabular}{ |l|l| }\n"
			layout += "\hline\n"
			layout += "Byte \# & Usage \\\\\n"
			layout += "\hline\n"
		layout += str(i) + " & Reserved \\\\\n"
		layout += "\hline\n"
	layout += "\end{tabular}\n"
	return layout

def genLayout2(layoutConfig):
	layout = ""

	params = re.findall(r'param (.*)=\"(.*)\"', layoutConfig)
	locations = re.findall(r'location (\d) \"(.*)\"', layoutConfig)
	
	paramDict = {}
	for param in params:
		paramDict[param[0]] = param[1]

	if "VersionID" not in paramDict:
		# Error
		pass
	if "VersionName" not in paramDict:
		# Error
		pass

	locations.insert(0, ("4", "Layout Version ID (" + hex(int(paramDict["VersionID"])) + ")"))

	totalBytes = 0
	# calculate the total number of bytes in config
	for location in locations:
		totalBytes += int(location[0])
	totalPages = int(totalBytes / 128)+1
	for i in range(128 - (totalBytes % 128)):
		locations += [("1", "Reserved")]
	layout += "\subsection{Layout " + paramDict["VersionName"] + "}\n"	
	
	byteCounter = 0
	bytesLeftInMultirow = 0
	locationCounter = -1 # Will be incremented to 0 on first row
	bytesThisPage = 0
	for page in range(totalPages):
		# 48 rows per page
		pageLayout = ["" for i in range(48)]
		bytesThisPage = bytesThisPage + 128
		# 3 columns per page
		for columns in range(3):
			for row in range(len(pageLayout)):
				if (byteCounter >= bytesThisPage):
					pageLayout[row] += "& & "
					continue
				if (bytesLeftInMultirow == 0):
					locationCounter = locationCounter + 1
					pageLayout[row] += str(byteCounter) + " & \multirow{" + locations[locationCounter][0] + "}{*}{" + locations[locationCounter][1] + "} & "
					byteCounter = byteCounter + 1
					bytesLeftInMultirow = int(locations[locationCounter][0])-1
				else:
					pageLayout[row] += str(byteCounter) + " & & "
					byteCounter = byteCounter + 1
					bytesLeftInMultirow = bytesLeftInMultirow - 1
		layout += "\\begin{tabular}{ |l|l||l|l||l|l| }\n"
		layout += "\hline\n"
		layout += "Byte \# & Usage & Byte \# & Usage & Byte \# & Usage \\\\\n"
		layout += "\hline\n"
		i = 0
		for row in pageLayout:
			# Remove redundant "& " on each row
			layout += row[:-2] + "\\\\\n"
			i = i + 1
			if (i == 4):
				layout += "\hline \n"
				i = 0
	layout += "\end{tabular}\n"
	return layout

def genLayout3(layoutConfig):
	layout = ""

	params = re.findall(r'param (.*)=\"(.*)\"', layoutConfig)
	locations = re.findall(r'location (\d+) \"(.*)\"', layoutConfig)
	
	paramDict = {}
	for param in params:
		paramDict[param[0]] = param[1]

	if "VersionID" not in paramDict:
		print("Missing VersionID in layout\n")
		raise Exception()
	if "VersionName" not in paramDict:
		print("Missing VersionName in layout\n")
		raise Exception()
	locations.insert(0, ("4", "Layout Version ID (" + hex(int(paramDict["VersionID"])) + ")"))

	totalBytes = 0
	# calculate the total number of bytes in config
	for location in locations:
		totalBytes += int(location[0])
	totalPages = int(totalBytes / 128)+1
	for i in range(128 - (totalBytes % 128)):
		locations += [("1", "Reserved")]
	layout += "\subsection{Layout " + paramDict["VersionName"] + "}\n"	
	
	byteCounter = 0
	bytesLeftInMultirow = 0
	locationCounter = -1 # Will be incremented to 0 on first row
	bytesThisPage = 0
	spanColumns = False # A location spans from one table column to another, maybe even across tables
	rewriteMultirow = False # Need to write multirow value at top of new column
	# GLHF
	for page in range(totalPages):
		# 48 rows per page
		pageLayout = ["" for i in range(48)]
		pageLines = ["" for i in range(48)]
		bytesThisPage = bytesThisPage + 128
		# 3 columns per page
		for column in range(3):
			if (spanColumns):
				rewriteMultirow = True
				spanColumns = False
			for row in range(len(pageLayout)):
				if (byteCounter >= bytesThisPage):
					pageLayout[row] += "& & "
					pageLines[row-1] += "\cline{" + str(column*2+1) + "-" + str(column*2+2) + "} "
					continue
				if (bytesLeftInMultirow == 0):
					locationCounter = locationCounter + 1
					bytesLeftInMultirow = int(locations[locationCounter][0])
					# If location is split across columns in table
					if (bytesLeftInMultirow + row > 48):
						pageLayout[row] += str(byteCounter) + " & \multirow{" + str(48-row) + "}{*}{" + locations[locationCounter][1] + "...} & "
						spanColumns = True
					elif (bytesLeftInMultirow + byteCounter > bytesThisPage):
						pageLayout[row] += str(byteCounter) + " & \multirow{" + str(bytesThisPage-byteCounter) + "}{*}{" + locations[locationCounter][1] + "...} & "
						spanColumns = True
					else:
						pageLayout[row] += str(byteCounter) + " & \multirow{" + str(bytesLeftInMultirow) + "}{*}{" + locations[locationCounter][1] + "} & "
					pageLines[row-1] += "\cline{" + str(column*2+1) + "-" + str(column*2+2) + "} "
					byteCounter = byteCounter + 1
				else:
					if (rewriteMultirow):
						pageLayout[row] += str(byteCounter) + " & \multirow{" + str(bytesLeftInMultirow) + "}{*}{..." + locations[locationCounter][1] + "} & "
						rewriteMultirow = False
					else:
						pageLayout[row] += str(byteCounter) + " & & "
					byteCounter = byteCounter + 1
				bytesLeftInMultirow = bytesLeftInMultirow - 1
		layout += "\\begin{tabular}{ |l|l||l|l||l|l| }\n"
		layout += "\hline\n"
		layout += "\multicolumn{6}{|c|}{" + "Layout " + paramDict["VersionName"] + " Page \#" + str(page) + "} \\\\"
		layout += "\hline\n"
		layout += "Byte \# & Usage & Byte \# & Usage & Byte \# & Usage \\\\\n"
		layout += "\hline\n"
		for row in range(len(pageLayout)-1):
			# Use [:-2] to remove redundant "& " on each row
			layout += pageLayout[row][:-2] + "\\\\ " + pageLines[row] + "\n"
		# Manually write last line so we can manually write the line at the bottom of the table
		layout += pageLayout[48-1][:-2] + "\\\\ \n"
		layout += "\hline\n"
		layout += "\end{tabular}\\\\\n"
	return layout, paramDict["VersionID"], paramDict["VersionName"]

# I think it might be easier to rewrite the locations list rather than trying to detect cross-column jumps in the loop
if __name__ == "__main__":
	pass
