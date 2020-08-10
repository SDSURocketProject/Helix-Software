
def autogenWarnStart(sectionName, filePath, commentChar="%"):
	out = commentChar + " WARNING START OF SECTION AUTOGENERATED BY PYTHON SCRIPT\n"
	out += commentChar + " THIS SECTION MAY BE AUTOMATICALLY CHANGED AT ANY TIME\n"
	out += commentChar + " Autogenerated section name: " + sectionName + "\n"
	out += commentChar + " File path of script: ARD/" + filePath.split("/ARD/")[-1] + "\n"
	return out

def autogenWarnEnd(sectionName, filePath, commentChar="%"):
	out = commentChar + " WARNING END OF SECTION AUTOGENERATED BY PYTHON SCRIPT\n"
	out += commentChar + " THIS SECTION MAY BE AUTOMATICALLY CHANGED AT ANY TIME\n"
	out += commentChar + " Autogenerated section name: " + sectionName + "\n"
	out += commentChar + " File path of script: ARD/" + filePath.split("/ARD/")[-1] + "\n"
	return out

def usage(fileName):
	pass

def error(errorMessage):
	pass

def warning(message):
	print("Warning:" + message)