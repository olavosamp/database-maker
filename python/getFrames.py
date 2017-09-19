import cv2
import numpy as np

videoPath = "F:\\Program Files\\Arquivos Incomuns\\Relevante\\UFRJ\\Projeto Final\\DadosPetrobras\\20170724_FTP83G_Petrobras\\CIMRL10-676_OK\PIDF-1 PO MRL-021_parte2.mpg"
csvPath = "..\\csv\\PIDF-1 PO MRL-021_parte2 TEST.csv"

video = cv2.VideoCapture(videoPath)

frameRate = np.ceil(video.get(cv2.CAP_PROP_FPS))

framePeriod = 2000

eventStart = 600000
eventEnd   = 720000

videoName = "testVideo1"
dirPath = "..\\images\\{}".format(videoName)

ID = 1

frameTime = eventStart
frameCount = 1
while(frameTime < eventEnd):
	errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)

	errRead, frame = video.read()

	cv2.imshow('frame', frame)
	# cv2.waitKey(framePeriod)

	imgPath = "{}\\{} ID{:2d} FRAME{:3d} class".format( dirPath, videoName, ID, frameCount)
	print("\n", imgPath)

	frameTime = frameTime + framePeriod
	frameCount = frameCount + 1

print("\n", frameRate)

video.release()