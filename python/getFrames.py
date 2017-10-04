import os

import cv2
import numpy 		as np
import pandas 		as pd

from timeConverter import timeConverter

def getFrames(videoPath, csvPath):
	# videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.mpg"
	# csvPath = "..\\csv\\PIDF-1 PO MRL-021_parte2.csv"

	# Read the data csv and open the video file
	data = pd.read_csv(csvPath, dtype=str)
	video = cv2.VideoCapture(videoPath)

	frameRate = video.get(cv2.CAP_PROP_FPS)

	print("Frame rate", frameRate)

	# Interval between captured frames, in ms
	# framePeriod = (20/frameRate)*1000

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
	errCount = {'errSet': 0, 'errRead': 0, 'errWrite': 0}
	frameCount = np.zeros(numEntries, dtype=np.int32)
	runTime = np.zeros(numEntries)

	## Perform frame capture operations
	for i in range(numEntries):	
		eventStart 	= timeConverter(data.loc[i,'StartTime'])*1000
		eventEnd   	= timeConverter(data.loc[i,'EndTime'])*1000
		runTime[i]  = eventEnd - eventStart		# In ms

	# Number of frames in video (aprox)
	maxFrames = np.sum(runTime)*frameRate
	#maxFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)

	for i in range(numEntries):
		ID 			= int(data.loc[i,'Id'])
		eventStart 	= timeConverter(data.loc[i,'StartTime'])*1000
		eventEnd   	= timeConverter(data.loc[i,'EndTime'])*1000
		frameClass 	= data.loc[i,'Class']

		# Find frame period
		framePeriod = 20*(runTime[i]*numEntries/maxFrames)*1000
		# Limit frame period
		tMax = 5000					# 5 seconds
		tMin = (10/frameRate)*1000	# 0.5 seconds
		if framePeriod > tMax:
			framePeriod = tMax
		if framePeriod < tMin:
			framePeriod = tMin
		
		print("ID{:2d} framePeriod {:.3f}".format(ID, framePeriod))
		frameTime = eventStart
		while(frameTime < eventEnd):
			# Set video time and read next frame
			errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
			errRead, frame = video.read()

			# Saved image name/path
			imgPath = "{}\\{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
			# print("\n", imgPath)

			# print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
			# TODO: Add condition: write only if frame is not empty/video.read() does not fail
			errWrite = cv2.imwrite(imgPath, frame)

			# Error handling
			if not(errWrite) or not(errRead) or not(errSet):
				print("\n!!! Error!!! ")
				print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
				print("errWrite: {}\nerrRead: {}\nerrSet: {}".format(errWrite, errRead, errSet))

			errCount['errWrite'] = errCount['errWrite'] + (not(errWrite))
			errCount['errSet']   = errCount['errSet']   + (not(errSet))
			errCount['errRead']  = errCount['errRead']  + (not(errRead))


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
	print('\nErrors during extraction:')
	print(errCount)
	# print("errWrite", errWrite)
	# print("errRead", errRead)
	# print("errSet", errSet)

	print("\nFrame rate: ", frameRate)
	print("Total frames (csv): ", maxFrames/1000)
	print("Total frames (video): ", video.get(cv2.CAP_PROP_FRAME_COUNT))
	print("Total frames acquired: ", frameTotal)
	print("   Tubo: ", tuboCount)
	print("   Nada: ", nadaCount)
	print("   Conf: ", confCount)

	runTime = np.divide(runTime, 1000)
	print("\nRun time: {} (for contiguous classification, should be the same as video run time)".format(np.sum(runTime)))
	print("   Mean: ", np.mean(runTime))
	print("   Std: ", np.std(runTime))

	video.release()
	return frameTotal