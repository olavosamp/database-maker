import os
import glob
import pandas as pd
import numpy as np
from collections import Counter

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

def listImages(dataPath):
	# dataPath is the path of the image folder to be read
	#
	# Finds images inside dataPath and lists all corresponding image paths
	# Returns labels per class
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
	for filePath in glob.glob(dataPath+'**'+dirs.sep+'*.jpg', recursive=True):
			# Replace backslashes with defined separator (in dirs) for compatibility
			filePath = filePath.replace("\\", dirs.sep)

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

			#TODO: ATUALIZAR PARA SUPORTE A UMA LISTA ARBITRARIA DE CLASSES
			# else:
			# 	print("\nError: Unidentified class\n{}".format(filePath))

	return imagePaths, labels

def countImages(dataPath):
	# Returns four variables, with the number of examples of each class in the dataset and the total
	#
	imagePaths, labels = listImages(dataPath)

	tuboCount   = len(np.squeeze(np.where(np.isin(labels, commons.tuboCode))))
	nadaCount   = len(np.squeeze(np.where(np.isin(labels, commons.nadaCode))))
	confCount   = len(np.squeeze(np.where(np.isin(labels, commons.confCode))))
	totCount    = len(labels)

	return tuboCount, nadaCount, confCount, totCount

def splitCsv(csvPath):
	# Reads a folder csv, splits it one dataframe per video
	# and returns them as a list of dataframes

	# csvPath = dirs.registro_de_eventos+"GHmls16-263_OK.csv"

	data = pd.read_csv(csvPath, dtype=str)

	# Find and list all unique video names found in the csv
	nameList = data['VideoName'].unique().tolist()

	print("\n", nameList)
	dfList = []
	# Create a new dataframe for each unique video name found,
	# splitting the original in many new single video dataframes
	for elem in nameList:
		newDf = data.loc[:][data.VideoName == elem]
		# print("\nNew DF")
		# print(newDf)
		dfList.append(newDf.reset_index())

	return dfList

def rebuildDatasetMulti(csvFolder=dirs.registro_de_eventos, videoFolder=dirs.dataset, targetPath=dirs.images):
	# Extract images from videos based on folder csv files
	#
	# Arguments:
	#	csvPath:	filepath of the csv folder
	#	videoPath:	filepath of the video folder
	#	targetPath:	images destination folder

	# GET FOLDER CSVS
	#
	# FOR EACH FOLDER CSV
	#	SPLIT FOLDER CSV IN NORMAL CSVS
	#	FOR EACH CSV
	#		GET FRAMES FROM CSV
	#

	datasetName = "dataset_registro_de_eventos_test"

	videoList = []
	print("\nScanning for the following file formats:")
	print("\n{}".format(commons.videoFormats))
	# Find video filepaths and store them in videoList
	for videoFormat in commons.videoFormats:
		print(videoFolder+'**'+dirs.sep+'*.'+videoFormat)
		newList = glob.glob(videoFolder+'**'+dirs.sep+'*.'+videoFormat, recursive=True)
		videoList.extend(newList)
	print("\n")

	folderCsvList = glob.glob(csvFolder+'**'+dirs.sep+'*.csv', recursive=True)

	# Replaces \\ with defined separator
	videoList = list(map(lambda x: x.replace("\\", dirs.sep), videoList))
	folderCsvList   = list(map(lambda x: x.replace("\\", dirs.sep), folderCsvList))


	# print("\nFolder csv list:")
	# print(folderCsvList)

	# Split each folder csv in video csvs and list them all together
	csvList = []
	list(map(lambda x: csvList.extend(splitCsv(x)), folderCsvList))

	# print("\nSplit csv list:")
	# print(csvList)

	# print("Df name")
	# print(csvList[0].loc[0]["VideoName"])

	# Create database folder
	logPath = targetPath+dirs.sep
	try:
		os.makedirs(logPath)
	except OSError:
		pass

	unmatched  = 0
	frameTotal = 0
	# For each video file, try to find a matching csv file
	for videoPath in videoList:
		match = False
		videoName = videoPath.split(dirs.sep)[-1]
		# videoName = videoName.split('.')[-2]
		videoName = videoName[:-4]				# Only works for file extensions 3 characters long
												# ex: .avi, .wmv, .vob, .mpg
		# print("\nSearching for: ", videoName)
		# print("")

		for csvDf in csvList:
			csvName = csvDf.loc[0]["VideoName"]+".csv"

			# Search for a csv file with the same name as the video
			if csvName.find(videoName) == 0:
				# If a video has a matching csv file, run getFrames to extract its frames
				print("Processing video {} ...".format(videoPath.split(dirs.sep)[-1]))
				frameTotal += getFrames(videoPath, csvDf, targetPath)

				# print("\nMatch:\n", videoPath)
				# print(csvDf)
				match = True
				break

		# Count videos without csv files
		if not(match):
			unmatched += 1

	# Count all created images and get class totals
	tuboCount, nadaCount, confCount, totCount = countImages(targetPath)

	# print("\nVIDEO LIST:\n{}\n".format(videoList))
	print("\n{} videos found".format(len(videoList)))
	print("\n{} csv files found".format(len(csvList)-1))
	print("\nFound {} matches. {} videos remain without classification and will not be used.".format(len(videoList)-unmatched, unmatched))

	# Save database information
	file = open(logPath+"Info.txt", 'w')
	file.writelines(["Extracao de frames com periodo variavel","\n\nDataset {}:".format(datasetName),
	"\nTubo:\t{:4d}".format(tuboCount), "\nNada:\t{:4d}".format(nadaCount), "\nConf:\t{:4d}".format(confCount),
	"\nTotal:\t{:4d}".format(totCount), "\n\nTamanho em disco: "])
	file.close()


	return frameTotal

def rebuildDataset(csvFolder=dirs.csv, videoFolder=dirs.dataset, targetPath=dirs.images):
	# Extract images from videos, according to class descriptions
	#
	# Arguments:
	#	csvPath is filepath of the csv folder
	#	videoPath is filepath of the video folder
	#	targetPath is images destination folder

	datasetName = "dataset_tmax_20s_tmin_1_2s"

	videoList = []
	print("\nScanning for the following file formats:\n")
	for videoFormat in commons.videoFormats:
		print(videoFolder+'**'+dirs.sep+'*.'+videoFormat)
		newList = glob.glob(videoFolder+'**'+dirs.sep+'*.'+videoFormat, recursive=True)
		videoList.extend(newList)
	print("\n")

	csvList = glob.glob(csvFolder+'**'+dirs.sep+'*.csv', recursive=True)

	# Replaces \\ with defined separator
	videoList = list(map(lambda x: x.replace("\\", dirs.sep), videoList))
	csvList   = list(map(lambda x: x.replace("\\", dirs.sep), csvList))

	# Create database folder
	logPath = targetPath+dirs.sep
	try:
		os.makedirs(logPath)
	except OSError:
		pass

	# for video in videoList:
	# 	print(video)

	unmatched  = 0
	frameTotal = 0
	# For each video file, try to find a matching csv file
	for videoPath in videoList:
		match = False
		videoName = videoPath.split(dirs.sep)[-1]
		# videoName = videoName.split('.')[-2]
		videoName = videoName[:-4]				# Only works for file extensions 3 characters long
												# ex: .avi, .wmv, .vob, .mpg

		# print("\nSearching for: ", videoName)
		# print("")
		for csvPath in csvList:
			csvName = csvPath.split(dirs.sep)[-1]
			# print(csvName)

			# Search for a csv file with the same name as the video
			if csvName.find(videoName) == 0:
				# If a video has a matching csv file, run getFrames to extract its frames
				print("Processing video {} ...".format(videoPath.split(dirs.sep)[-1]))
				frameTotal += getFrames(videoPath, csvPath, targetPath)

				# print("\nMatch:\n", videoPath)
				# print(csvPath)
				match = True
				break

		# Count videos without csv files
		if not(match):
			unmatched += 1

	# Count all created images and get class totals
	tuboCount, nadaCount, confCount, totCount = countImages(targetPath)

	# print("\nVIDEO LIST:\n{}\n".format(videoList))
	print("\n{} videos found".format(len(videoList)))
	print("\n{} csv files found".format(len(csvList)-1))
	print("\nFound {} matches. {} videos remain without classification and will not be used.".format(len(videoList)-unmatched, unmatched))

	# Save database information
	file = open(logPath+"Info.txt", 'w')
	file.writelines(["Extracao de frames com periodo variavel","\nDataset {}:".format(datasetName),
	"Tubo:\t{:4d}".format(tuboCount), "Nada:\t{:4d}".format(nadaCount), "Conf:\t{:4d}".format(confCount),
	"Total:\t{:4d}".format(totCount), "\nTamanho em disco: "])
	file.close()

	return videoList, csvList, frameTotal
