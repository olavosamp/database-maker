import os
import glob
import time
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
    #     Tubo, Nada, Conf
    #
    # Returns imagePaths, labels
    # imagePaths contains every image filepath
    # labels contains corresponding ordinal class codes, according to commons.py
    import dirs

    labels         = []
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
            #     print("\nError: Unidentified class\n{}".format(filePath))

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

    # print("\n", nameList)
    dfList = []
    # Create a new dataframe for each unique video name found,
    # splitting the original in many new single video dataframes
    for elem in nameList:
        newDf = data.loc[:][data.VideoName == elem]
        # print("\nNew DF")
        # print(newDf)
        dfList.append(newDf.reset_index())

    return dfList

def rebuildDatasetMulti(csvFolder, videoFolder, targetPath=dirs.images):
    # Extract images from videos based on folder csv files
    #
    # Arguments:
    #    csvPath:    filepath of the csv folder
    #    videoPath:    filepath of the video folder
    #    targetPath:    images destination folder

    # Algorithm: GET FOLDER CSVS
    #
    # FOR EACH FOLDER CSV
    #    SPLIT FOLDER CSV IN NORMAL CSVS
    #    FOR EACH CSV
    #        GET FRAMES FROM CSV
    #

    datasetName = "dataset_registro_de_eventos_test"

    videoList = []
    print("\nScanning for the following file formats:")
    print("\n{}".format(commons.videoFormats))
    # Find video filepaths and store them in videoList
    # for videoFormat in commons.videoFormats:
    #     searchString = videoFolder+'**'+dirs.sep+'*.'+videoFormat
    #     # print(searchString)
    #     newList = glob.glob(searchString, recursive=True)
    #     videoList.extend(newList)
    # print("\n")

    folderCsvList = glob.glob(csvFolder+'**'+dirs.sep+'*.csv', recursive=True)
    # Replaces \\ with defined separator
    # videoList        = list(map(lambda x: x.replace("\\", dirs.sep), videoList))
    folderCsvList    = list(map(lambda x: x.replace("\\", dirs.sep), folderCsvList))

    # print("\nFolder csv list:")
    # print(folderCsvList)

    # list(map(lambda x: csvList.append((x, splitCsv(x))), folderCsvList))
    # list(map(lambda x: (csvList.append((x, df)) for df in splitCsv(x)), folderCsvList))

    # Split each folder csv in video csvs and list them all together
    csvList = [()]                # List of Tuples of (folder name, csv dataframe)
    for csv in folderCsvList:
        subCsvList = splitCsv(csv)
        for df in subCsvList:
            csvList.append((csv, df))

    csvList.pop(0)    # Removes initialization empy entry

    # print("\nSplit csv list:")
    # print(csvList[0][1].loc[:]['VideoName'])
    # print("")

    # for dataTuple in csvList:
    #     folderName = dataTuple[0].split(dirs.sep)[-1][:-4]
    #     print("{}\n{}\n".format(folderName, dataTuple[1].loc[0]['VideoName']))

    print("Df name")
    print(csvList[0][1].loc[0]["VideoName"])

    # Create database folder
    logPath = targetPath+dirs.sep
    try:
        os.makedirs(logPath)
    except OSError:
        pass

    foundVideos = 0
    frameTotal = 0
    # print(csvList)

    # Iterate on csv dataframes
    for csvTuple in csvList:
        # match = False
        csvDf = csvTuple[1]
        csvName = csvDf.loc[0]["VideoName"]#+".csv"
        folderName = csvTuple[0].split(dirs.sep)[-1][:-4]

        print(csvTuple[0])
        input()
        print("\nSearching for: ", csvName)
        print("at folder ", folderName)
        input()


        # fullName = videoPath.split(dirs.sep)[-1]
        # # videoName = videoName.split('.')[-2]
        # videoName = fullName[:-4]                # Only works for file extensions 3 characters long
        #                                         # ex: .avi, .wmv, .vob, .mpg
        # print("Analyzing video {}\n".format(fullName))
        # print("Could it be {}?".format(videoName))

        videoName = ""
        videoList = []
        timeReg = [()]    # (Video name, extraction time) tuple
        nameSplit = csvName.split(dirs.sep)
        if len(nameSplit) > 1:
            for videoFormat in commons.videoFormats:
                searchString = videoFolder+folderName+dirs.sep+nameSplit[0]+dirs.sep+nameSplit[-1]+"."+videoFormat

                newList = glob.glob(searchString, recursive=True)
                videoList.extend(newList)
                # print("Searching:\n{} ".format(searchString))

            videoList   = list(map(lambda x: x.replace("\\", dirs.sep), videoList))

            print("\nFound the following matching videos (more than one indicates a problem):\n ", videoList)

            # # Search for a csv file with the same name as the video
            # if not(videoName.find(nameSplit[0])) and not(videoName.find(nameSplit[-1])):
            #     # If a video has a matching csv file, run getFrames to extract its frames
            #     print("It's a match! Extracting frames...\n")
            #     frameTotal += getFrames(videoPath, csvDf, targetPath)
            #
            #     # print("\nMatch:\n", videoPath)
            #     # print(csvDf)
            #     matched += 1
            #     break
        else:
            for videoFormat in commons.videoFormats:
                searchString = videoFolder+folderName+dirs.sep+"**"+dirs.sep+nameSplit[-1]+"."+videoFormat
                newList = glob.glob(searchString, recursive=True)
                videoList.extend(newList)
                print("Searching:\n{} ".format(searchString))

            videoList = list(map(lambda x: x.replace("\\", dirs.sep), videoList))

            print("\nVideoList: ", videoList)

            # if videoName.find(nameSplit[0]) == 0:
            #     # If a video has a matching csv file, run getFrames to extract its frames
            #     print("It's a match! Extracting frames...\n")
            #     frameTotal += getFrames(videoPath, csvDf, targetPath)
            #
            #     # print("\nMatch:\n", videoPath)
            #     # print(csvDf)
            #     matched += 1
            #     break
        foundVideos += len(videoList)

        # If a video has a matching csv file, run getFrames to extract its frames
        for videoPath in videoList:
            print("\nExtracting frames from:\n{}".format(videoPath))
            startTime = time.time()

            frameTotal += getFrames(videoPath, csvDf, targetPath+folderName+dirs.sep)

            runTime = time.time() - startTime
            print("\nElapsed time:\n{:.2f} seconds".format(runTime) )
            timeReg.append((videoPath, runTime))

            # print("\nMatch:\n", videoPath)
            # print(csvDf)
            # matched += 1

        # # Count videos without csv files
        # if not(match):
        #     print("")
        #     unmatched += 1

    timeReg.pop(0)
    # Count all created images and get class totals
    # tuboCount, nadaCount, confCount, totCount = countImages(targetPath)
    tuboCount = 0
    nadaCount = 0
    confCount = 0

    #TODO: Consertar essa medida
    unmatched = len(csvList) - foundVideos

    ## Information

    # Video search stats
    print("\n{} videos found in csvs.".format(len(csvList)))
    print("{} matched in actual files.".format(foundVideos))
    print("\nFound {} matches. {} csv videos did not have a match and have not been used.".format(foundVideos, unmatched))
    print("A total of {} frames were captured. More information in Info.txt\n".format(frameTotal))

    # Save database information
    file = open(logPath+"Info.txt", 'w')
    file.writelines(["Extracao de frames com periodo variavel","\n\nDataset {}:".format(datasetName),
    "\nTubo:\t{:4d}".format(tuboCount), "\nNada:\t{:4d}".format(nadaCount), "\nConf:\t{:4d}".format(confCount),
    "\nTotal:\t{:4d}".format(frameTotal), "\n\nTamanho em disco: "])
    file.close()

    # Extraction runtimes
    print("\nVideo extraction runtimes:")
    print(timeReg)
    print("")
    for timeTuple in timeReg:
        print("{:}: {:.2f} seconds".format(timeTuple[0], timeTuple[1]))

    return videoList, csvList, frameTotal

def rebuildDataset(csvFolder=dirs.csv, videoFolder=dirs.base_videos, targetPath=dirs.images):
    # Extract images from videos, according to class descriptions
    #
    # Arguments:
    #    csvPath is filepath of the csv folder
    #    videoPath is filepath of the video folder
    #    targetPath is images destination folder

    datasetName = "dataset_tmax_20s_tmin_1_2s"

    videoList = []
    print("\nScanning for the following file formats:\n")
    for videoFormat in commons.videoFormats:
        print(videoFolder+'**'+dirs.sep+'*.'+videoFormat)
        newList = glob.glob(videoFolder+'**'+dirs.sep+'*.'+videoFormat, recursive=True)
        videoList.extend(newList)
    print("\n")

    print("\nSearching for csv files in\n", csvFolder, "\n")
    csvList = glob.glob(csvFolder+'**'+dirs.sep+'*.csv', recursive=True)

    # Replaces \\ with defined separator
    videoList = list(map(lambda x: x.replace("\\", dirs.sep), videoList))
    csvList   = list(map(lambda x: x.replace("\\", dirs.sep), csvList))

    print("\nCSV List\n")
    for path in csvList:
        print(path)

    # print("\nVideo List\n")
    # for path in videoList:
    #     print(path)

    # Create database folder
    logPath = targetPath+dirs.sep
    try:
        os.makedirs(logPath)
    except OSError:
        pass

    # for video in videoList:
    #     print(video)

    unmatched  = 0
    frameTotal = 0

    # For each csv file, try to find a matching video file
    for csvPath in csvList:
        match = False
        csvDf = pd.read_csv(csvPath, dtype='str')
        videoPath = csvDf.loc[0]['VideoName']

        # Check if videoPath has extension
        for videoFormat in commons.videoFormats:
            videoFormat = "."+videoFormat
            if videoFormat in videoPath:
                # print("Found extension")
                videoPath = videoPath[:-4]
                break

        # videoName = videoPath.split(dirs.sep)[-1]
        # videoName = videoName.split('.')[-2]
        # videoName = videoName[:-4]                # Only works for file extensions 3 characters long
                                                  # ex: .avi, .wmv, .vob, .mpg

        print("\nSearching for: ", videoPath)

        for video in videoList:
            if videoPath in video:
                print("Video match")

                # If a video has a matching csv file, run getFrames to extract its frames
                print("Processing video {} ...".format(video.split(dirs.sep)[-1]))
                # data = pd.read_csv(csvPath, dtype=str)
                frameTotal += getFrames(video, csvDf, targetPath)

                match = True
                break

        # Count videos without csv files
        if not(match):
            unmatched += 1

    # Count all created images and get class totals
    tuboCount, nadaCount, confCount, totCount = countImages(targetPath)

    # print("\nVIDEO LIST:\n{}\n".format(videoList))
    print("\n{} videos found".format(len(videoList)))
    print("\n{} csv files found".format(len(csvList)))
    print("\nFound {} matches. {} videos remain without classification and will not be used.".format(len(videoList)-unmatched, unmatched))

    # Save database information
    file = open(logPath+"Info.txt", 'w')
    file.writelines(["Extracao de frames com periodo variavel","\nDataset {}:".format(datasetName),
    "Tubo:\t{:4d}".format(tuboCount), "Nada:\t{:4d}".format(nadaCount), "Conf:\t{:4d}".format(confCount),
    "Total:\t{:4d}".format(totCount), "\nTamanho em disco: "])
    file.close()

    return videoList, csvList, frameTotal
