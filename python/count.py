import os
import glob
import pandas as pd
import numpy as np

import commons
import dirs
from getFrames import getFrames

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

def listImages(targetPath=dirs.images):
	# Finds images inside targetPath and lists all corresponding image paths
	# Save labels per class
	#
	# Identifies each file as belonging to one of three classes
	#	 Tubo, Nada, Conf
	#
	# Returns imagePaths, labels
	# imagePaths contains every image filepath
	# labels contains corresponding ordinal class codes, according to commons.py
	import dirs

	labels 		= []
	imagePaths  = []

	# Find every file in the root path
	for path, dirs, files in os.walk(targetPath):
		for fileTemp in files:
			filePath = os.path.join(path, fileTemp)
			# Replace backslashes with <other symbol?> for compatibility
			# filePath = filePath.replace("\\", "\\\\")

			# Append each file path to a list
			if filePath.find("tubo") > 0:
				imagePaths.append(filePath)
				labels.append(commons.tuboCode)

			elif filePath.find("nada") > 0:
				imagePaths.append(filePath)
				labels.append(commons.nadaCode)

			elif filePath.find("conf") > 0:
				imagePaths.append(filePath)
				labels.append(commons.confCode)

			else:
				print("\nError: Unidentified class\n{}\n".format(filePath))

	return imagePaths, labels

def countImages(labels):
	# Returns four variables, with the number of examples of each class in the dataset and the total
	#
	tuboCount   = len(np.squeeze(np.where(np.isin(labels, commons.tuboCode))))
	nadaCount   = len(np.squeeze(np.where(np.isin(labels, commons.nadaCode))))
	confCount   = len(np.squeeze(np.where(np.isin(labels, commons.confCode))))
	totCount    = len(labels)

	return tuboCount, nadaCount, confCount, totCount

def rebuildDataset(csvFolder=dirs.csv, videoFolder=dirs.dataset):
	# Extract images from videos, according to class descriptions
	#
	# Arguments:
	#	csvPath is filepath of the csv folder
	#	videoPath is filepath of the video folder
	#

	videoList = glob.glob(videoFolder+'**/*.*', recursive=True)
	csvList = glob.glob(csvFolder+'**/*.csv', recursive=True)

	unmatched  = 0
	frameTotal = 0

	# For each video file, try to find a matching csv file
	for videoPath in videoList:
		match = False
		videoName = videoPath.split(os.path.sep)[-1]
		videoName = videoName.split('.')[0]
		# print("\nSearching for: ", videoName)
		# print("")
		for csvPath in csvList:
			csvName = csvPath.split(os.path.sep)[-1]
			# print(csvName)

			# Search for a csv file with the same name as the video
			if csvName.find(videoName) == 0:
				# If a video has a matching csv file, run getFrames to extract its frames
				print("Processing video {} ...".format(videoPath.split(os.path.sep)[-1]))
				frameTotal += getFrames(videoPath, csvPath)

				# print("\nMatch:\n", videoPath)
				# print(csvPath)
				match = True
				break

		# Count videos without csv files
		if not(match):
			unmatched += 1

	print("\n{} videos found".format(len(videoList)))
	print("\n{} csv files found".format(len(csvList)-1))
	print("\nFound {} matches. {} videos remain without classification and will not be used.".format(len(videoList)-unmatched, unmatched))

	return videoList, csvList, frameTotal
