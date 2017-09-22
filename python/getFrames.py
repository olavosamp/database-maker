import os

import cv2
import numpy 		as np
import pandas 		as pd

from timeConverter import timeConverter

videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.mpg"
csvPath = "..\\csv\\PIDF-1 PO MRL-021_parte2.csv"

# Read the data csv and open the video file
data = pd.read_csv(csvPath, dtype=str)
video = cv2.VideoCapture(videoPath)

frameRate = np.ceil(video.get(cv2.CAP_PROP_FPS))

print("Frame rate", frameRate)

# Interval between captured frames, in ms
framePeriod = (20/frameRate)*1000

# Number of 
numEntries = data.loc[:,'Id'].count()

videoName = "testVideo1"
videoName = data.loc[0,'VideoName']
# dirPath = "..\\images\\{}".format(videoName)
dirPath = "..\\images\\{}".format(videoName)

# Create output folder
try:
	os.makedirs(dirPath)
except OSError:
	print("Directory already exists or invalid path")
	print(OSError)
	print()

tuboCount  = 0
nadaCount  = 0
confCount  = 0
frameCount = np.zeros(numEntries, dtype=np.int32)
runTime = np.zeros(numEntries)
for i in range(numEntries):
	ID 			= int(data.loc[i,'Id'])
	eventStart 	= timeConverter(data.loc[i,'StartTime'])*1000
	eventEnd   	= timeConverter(data.loc[i,'EndTime'])*1000
	frameClass 	= data.loc[i,'Class']

	runTime[i] = eventEnd - eventStart
	if runTime[i] >= 600000:		# 10 min
		framePeriod = (40/frameRate)*1000
	else:
		framePeriod = (20/frameRate)*1000

	frameTime = eventStart
	while(frameTime < eventEnd):
		# Set video time and read next frame
		errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
		errRead, frame = video.read()

		# Saved image name/path
		imgPath = "{}\\{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
		# print("\n", imgPath)

		print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
		errWrite = cv2.imwrite(imgPath, frame)

		# Error messages
		if not(errWrite) or not(errRead) or not(errSet):
			print("\n!!! Error!!! ")
			print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
			print("errWrite: {}\nerrRead: {}\nerrSet: {}".format(errWrite, errRead, errSet))

		# Advance time one framePeriod
		frameTime = frameTime + framePeriod
		frameCount[i] = frameCount[i] + 1

		# Count class occurrences
		if frameClass == 'tubo':
			tuboCount = tuboCount + 1
		elif frameClass == 'nada':
			nadaCount = nadaCount + 1
		elif frameClass == 'conf':
			confCount = confCount + 1

	print("ID{}: {} frames".format(ID, frameCount[i]))
	frameTotal = np.sum(frameCount)

## Information
print("\nFrame rate: ", frameRate)
print("Total frames acquired: ", frameTotal)
print("   Tubo: ", tuboCount)
print("   Nada: ", nadaCount)
print("   Conf: ", confCount)

runTime = np.divide(runTime, 1000)
print("\nRun time: {} (should be the same as video run time)".format(np.sum(runTime)))
print("   Mean: ", np.mean(runTime))
print("   Std: ", np.std(runTime))

video.release()