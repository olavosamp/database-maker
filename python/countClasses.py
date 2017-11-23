import os

def countClasses(rootPath):
	# List and save each file inside rootPath
	# Identify each file as belonging to one of three classes
	#	 Tubo, Nada, Conf
	# Creates one txt file for each class and saves the filepaths accordingly
	#
	# Returns the full paths of the txt files created
	#

	# rootPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\database-maker\\images"
	tuboPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\database-maker\\images\\tubo.txt"
	nadaPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\database-maker\\images\\nada.txt"
	confPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\database-maker\\images\\conf.txt"
	
	listTubo = open(tuboPath, 'w')
	listNada = open(nadaPath, 'w')
	listConf = open(confPath, 'w')

	totCount = 0
	tuboCount = 0
	nadaCount = 0
	confCount = 0
	# Finde every file in the root path
	for path, dirs, files in os.walk(rootPath):
		for file in files:
			filePath = os.path.join(path, file)
			
			# Save each file path in a class txt
			if filePath.find("tubo") > 0:
				tuboCount = tuboCount +1
				listTubo.writelines("{}\n".format(filePath))

			elif filePath.find("nada") > 0:
				nadaCount = nadaCount +1
				listNada.writelines("{}\n".format(filePath))

			elif filePath.find("conf") > 0:
				confCount = confCount +1
				listConf.writelines("{}\n".format(filePath))			

			else:
				print("\nError: Unidentified class\n{}\n".format(filePath))


			# listTubo.writelines("{},,\n".format(filePath))
			totCount = totCount + 1
			
			# print("{}".format(os.path.join(path, file)))

	# print("Tubo:  {}".format(tuboCount))
	# print("Nada:  {}".format(nadaCount))
	# print("Conf:  {}".format(confCount))
	# print("Total: {}".format(totCount))
	# print("\nTotal files found: {}".format(count))

	listTubo.close()
	listNada.close()
	listConf.close()
	# return tuboCount, nadaCount, confCount, totCount
	return tuboPath, nadaPath, confPath