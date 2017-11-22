import os
import pandas as pd

def getTotals():
	# getTotals.py
	# Lists and sum frame counts in all .txt/.csv files present in /path/
	# Frame count files should follow .csv formatting
	#
	
	path = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\database-maker\\csv\\Totals\\"

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