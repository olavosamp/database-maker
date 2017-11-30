import os
import pandas as pd
import dirs

def countCsv():
	# Lists and sum frame counts in all .txt/.csv files present in /path/
	# Frame count files should follow .csv formatting
	#
	# Returns a string with totals by class

	path = dirs.totals

	nameList = os.listdir(path)

	count = pd.DataFrame()
	for name in nameList:
		if not(name == "Totals.txt"):
			csvPath = "{}{}".format(path, name)
			data = pd.read_csv(csvPath)

			if count.empty:
				count = data
			else:
				count = pd.concat([count, data], axis=0, ignore_index=True)

	count = count.append(count.sum(numeric_only=True), ignore_index=True)

	# Save frame totals
	logPath = "..\\csv\\Totals\\Totals.txt"
	count.tail(1).to_csv(logPath, index=False)
	return count.tail(1).to_string(index=False)

def listImages():
	# Counts all existing images by class
	# Lists and saves each file path inside targetPath
	#
	# Identify each file as belonging to one of three classes
	#	 Tubo, Nada, Conf
	# Creates one txt file for each class with corresponding filepath
	#
	# Returns the full paths of the txt files created
	#
	import dirs

	targetPath = dirs.images

	tuboPath = dirs.images+"tubo.txt"
	nadaPath = dirs.images+"nada.txt"
	confPath = dirs.images+"conf.txt"

	fileTubo = open(tuboPath, 'w')
	fileNada = open(nadaPath, 'w')
	fileConf = open(confPath, 'w')

	totCount = 0
	tuboCount = 0
	nadaCount = 0
	confCount = 0
	# Finde every file in the root path
	for path, dirs, files in os.walk(targetPath):
		for fileTemp in files:
			filePath = os.path.join(path, fileTemp)
			# Replace backslashes with <other symbol?> for compatibility
			# filePath = filePath.replace("\\", "\\\\")

			# Save each file path in a class txt
			if filePath.find("tubo") > 0:
				tuboCount = tuboCount +1
				fileTubo.writelines("{}\n".format(filePath))

			elif filePath.find("nada") > 0:
				nadaCount = nadaCount +1
				fileNada.writelines("{}\n".format(filePath))

			elif filePath.find("conf") > 0:
				confCount = confCount +1
				fileConf.writelines("{}\n".format(filePath))

			else:
				print("\nError: Unidentified class\n{}\n".format(filePath))

			totCount = totCount + 1

			# print("{}".format(os.path.join(path, file)))

	print("Tubo:  {}".format(tuboCount))
	print("Nada:  {}".format(nadaCount))
	print("Conf:  {}".format(confCount))
	print("Total: {}".format(totCount))

	fileTubo.close()
	fileNada.close()
	fileConf.close()

	# Change first line of class files with class count
	with open(tuboPath, 'r+') as tempFile:
		tempList = list(tempFile)
		tempList[0] = str(tuboCount)#+"\n"
		tempFile.writelines(tempList)
	# listTubo = list(fileTubo)
	# listNada = fileNada.readlines()
	# listConf = fileConf.readlines()
    #
	# listTubo[0] = tuboCount
	# listNada[0] = nadaCount
	# listConf[0] = confCount

	# fileTubo.writelines(listTubo)
	# fileNada.writelines(listNada)
	# fileConf.writelines(listConf)
    #
	# fileTubo.close()
	# fileNada.close()
	# fileConf.close()
	return tuboPath, nadaPath, confPath

def countImages():
	tuboPath, nadaPath, confPath = listImages()
	fileTubo = open(tuboPath, 'r')
	fileNada = open(nadaPath, 'r')
	fileConf = open(confPath, 'r')

	countTubo = list(fileTubo)[0]
	countNada = list(fileNada)[0]
	countConf = list(fileConf)[0]

	countTot = countTubo + countNada + countConf
	return countTubo, countNada, countConf, countTot
