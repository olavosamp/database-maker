import os

import cv2
import numpy 		as np
import pandas 		as pd

videoPath = "C:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\Petrobras\\PIDF-1 PO MRL-021_parte2.mpg"
csvPath = "..\\csv\\PIDF-1 PO MRL-021_parte2 TEST.csv"

data = pd.read_csv(csvPath)

video = cv2.VideoCapture(videoPath)

frameRate = np.ceil(video.get(cv2.CAP_PROP_FPS))

print("Frame rate", frameRate)

framePeriod = (20/frameRate)*1000		# Interval between captured frames, in ms

eventStart = 600000
eventEnd   = 720000
videoName = "testVideo1"
ID = 1
frameClass = "teste"

# dirPath = "..\\images\\{}".format(videoName)
dirPath = "..\\images\\{}".format(videoName)

try:
	os.makedirs(dirPath)
except OSError:
	print("Directory already exists, probably")

frameTime = eventStart
frameCount = 1
while(frameTime < eventEnd):
	errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)

	errRead, frame = video.read()

	# cv2.imshow('frame', frame)
	# cv2.waitKey(framePeriod)

	imgPath = "{}\\{} ID{:2d} FRAME{:3d} {}.jpg".format( dirPath, videoName, ID, frameCount, frameClass)
	# print("\n", imgPath)

	print("ID{:2d} Frame {:3d}".format(ID, frameCount))
	errWrite = cv2.imwrite(imgPath, frame)
	# print("Error write?: ", errWrite)

	frameTime = frameTime + framePeriod
	frameCount = frameCount + 1

print("\nFrame rate: ", frameRate)

video.release()