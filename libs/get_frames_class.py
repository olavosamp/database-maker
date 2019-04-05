import cv2
import pandas       as pd
import numpy        as np
import datetime
import os.path

import libs.dirs    as dirs
import libs.commons as commons
from libs.utils     import timeConverter

class GetFrames:
    '''
        Base frame extractor class
    '''
    def __init__(self, destPath, verbose=True, errorLog=True):
        self.destPath   = destPath
        self.verbose    = verbose
        self.errorLog   = errorLog

        self.videoError   = {'read': False, 'set': False, 'write': False}
        if self.errorLog:
            self.errorCounter = {'read': 0,     'set': 0,     'write': 0}
            self.errorList = []

        self.frameCount = 0

        if self.verbose:
            print("\nUsing opencv version: ", cv2.__version__)

        # Create destination folder
        dirs.create_folder(self.destPath)


    def get_video_data(self, videoPath):
        try:
        	self.video = cv2.VideoCapture(videoPath)
        except:
            print("\nError opening video:\n")
            cv2.VideoCapture(videoPath)

        self.frameRate = self.video.get(cv2.CAP_PROP_FPS)
        if self.frameRate == 0:
            self.frameRate = 25  # Default frame rate is 30 or 25 fps

        self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)

        self.videoFolderPath = "/".join(videoPath.split("/")[3:-1])+"/"
        dirs.create_folder(self.destPath+self.videoFolderPath)
        return self.video


    def get_frames(self):
        self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.videoTime   = self.totalFrames/self.frameRate
        if self.verbose:
            print("Total video time:")
        print(str(datetime.timedelta(seconds=self.videoTime)))

        self.timePos    = 0
        self.frameCount = 0

        # Actual frame extraction function
        self._routine_get_frames()

        print(self.videoError)
        print("{} frames captured.".format(self.frameCount))


    def reset_error_flags(self):
        # Reset video error flags
        self.videoError["set"]   = True
        self.videoError["read"]  = True
        self.videoError["write"] = True



class GetFramesCsv(GetFrames):
    '''
        csvPath:  reference csv filepath
        destPath: dataset destination folder
        interMin: minimum frame capture interval, in seconds
        interMax: maximum frame capture interval, in seconds
    '''
    def __init__(self, csvPath, destPath='./images/', interMin=0.8, interMax=20,
     verbose=True, errorLog=True, ignorePathError=False):
        super().__init__(destPath, verbose=verbose)
        self.ignorePathError = ignorePathError
        self.csvPath         = csvPath
        self.interMin        = interMin
        self.interMax        = interMax

        # Get csv data
        if self.csvPath != None:
            self.csvData   = self.get_csv_data()
        else:
            raise NameError("CSV filepath not defined.")


    # def validate_csv_path(self):
    #     # Check if csv path exists


    def get_csv_data(self):
        # CSV Data is a pandas DataFrame of the csv file
        self.csvData = pd.read_csv(self.csvPath, dtype=str)

        # Validate video paths
        # Assumes that there can be many videopaths in one csv
        # note: iterrows does not preserve dtypes;
        #       don't modify dataframe while iterating.
        for index, row in self.csvData.iterrows():
            checkPath = dirs.dataset+row['VideoName']
            if os.path.isfile(checkPath) == False:
                print("\n", checkPath, "\n")
                raise FileNotFoundError("Csv points to a video that doesn't exist.")

        # Assumes there can be only one videopath in the entire csv
        self.videoPath    = dirs.dataset+self.csvData.loc[0, 'VideoName']

        return self.csvData


    def get_capture_interval(self):
        # self.interval = 20*(runTime[self.eventNum]*self.numEntries/maxFrames)*1000
        self.interval = 20*(self.eventTime*self.numEntries/self.totalFrames)#*1000
        self.interval = np.clip(self.interval, self.interMin, self.interMax)
        return self.interval


    def get_filename(self):
        # videoPath:       dataset path + csv['VideoName']
        # videoName:       csv['VideoName']
        # videoNameClean:  csv['VideoName'] sem extensão ".wmv"
        # videoNameTail:   nome do vídeo sem extensão
        # videoFolderPath: "/".join(videoPath.split("/")[3:-1])+"/" path relativo do video
        # fileName:        nome do frame "<Nome do video> ID<> FRAME<> <classe>.jpg"
        # folderPath:      videoPath + video name + frame file path
        # framePath:       path nome do frame

        videoNameClean = ".".join(self.videoName.split(".")[:-1]).replace("/", "--")
        videoNameTail  = videoNameClean.split("--")[-1]

        self.fileName   = videoNameClean+ " ID{} FRAME{} {}.jpg".format(self.eventId, self.eventFrames, self.eventClass)
        self.folderPath = self.destPath+self.videoFolderPath+videoNameTail+"/"
        self.framePath  = self.folderPath+self.fileName

        dirs.create_folder(self.folderPath)

        # print(self.destPath)
        # print(self.videoFolderPath)
        # print(self.fileName)
        # print(self.framePath)
        # input()

        return self.framePath


    def get_frames(self):
        # self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        # self.videoTime   = self.totalFrames/self.frameRate
        # if self.verbose:
        #     print("Total video time:")
        # print(str(datetime.timedelta(seconds=self.videoTime)))

        # Actual frame extraction function
        self._routine_get_frames()

        print(self.videoError)
        print("{} frames captured.".format(self.frameCount))


    def _routine_get_frames(self):
        ''' Get frames from using a csv file as reference'''


        self.video = self.get_video_data(self.videoPath)
        print("\nframeRate:", self.frameRate)
        print("totalFrames:", self.totalFrames)
        print()


        # if self.totalFrames == 0:
            # TODO: GET TOTAL FRAMES AND VIDEO TIME SOME WAY

        # self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.videoTime   = self.totalFrames/self.frameRate
        self.numEntries = self.csvData.shape[0]
        # print("\nFound ", self.numEntries, "lines in csv.\n")

        self.frameCount = 0
        for self.eventNum in range(self.numEntries):
            self.eventFrames= 0
            self.eventStart = timeConverter(self.csvData.loc[self.eventNum,'StartTime'])#*1000
            self.eventEnd   = timeConverter(self.csvData.loc[self.eventNum,'EndTime'])#*1000
            self.eventClass = self.csvData.loc[self.eventNum,'Class']
            self.eventId    = self.csvData.loc[self.eventNum, 'Id']
            self.videoName  = self.csvData.loc[self.eventNum, 'VideoName']

            self.eventTime = self.eventEnd - self.eventStart

            if self.eventClass not in commons.classes:
                print("\n\nError: Proposed class is not in accepted classes list.\nSkipping entry.\n\n")
                continue

            self.interval  =  self.get_capture_interval()

            self.timePos   = self.eventStart
            self.timeLimit = self.eventEnd

            print("\nEvent ", self.eventId)
            print("timeStart: ", self.eventStart)
            print("interval: ", self.interval)
            print("timeEnd: ", self.eventEnd)

            while self.timePos < self.timeLimit:
                # if self.verbose:
                    # print("Frame ", self.eventFrames)
                    # print("Time: ", self.timePos)

                self.videoError['set'] = self.video.set(cv2.CAP_PROP_POS_MSEC, self.timePos*1000)

                # frameNum is Absolute frame number
                # frameCount is the number of frames extracted from the video so far
                self.frameNum = self.video.get(cv2.CAP_PROP_POS_FRAMES)

                self.videoError['read'], self.frame = self.video.read()

                self.framePath = self.get_filename()
                self.videoError['write'] = cv2.imwrite(self.framePath, self.frame)

                self.timePos     += self.interval
                self.eventFrames += 1

                if self.errorLog:
                    for key in self.videoError.keys():
                        if self.videoError[key] == False:
                            self.errorCounter[key] += 1
                            self.errorList.append((self.framePath, key))

                # Print errors
                if self.verbose:
                    if (self.videoError['set'] == False) or (self.videoError['read'] == False) or (self.videoError['write'] == False):
                        print("\n!!! Error !!!\n\
                        Set  : {}\n\
                        Read : {}\n\
                        Write: {}\n".format(self.videoError['set'],self.videoError['read'],self.videoError['write']))

                self.reset_error_flags()

            print("Captured frames: {}\n".format( self.eventFrames))
            self.frameCount += self.eventFrames



class GetFramesFull(GetFrames):
    def __init__(self, videoPath, destPath='./images/', interval=5, interMin=0.8, interMax=20, verbose=True):
        super().__init__(destPath, verbose=verbose)
        self.videoPath  = videoPath
        self.interval   = interval
        self.interMin   = interMin
        self.interMax   = interMax

        # Validate video path and file
        self.video = self.get_video_data(self.videoPath)

        self.validate_interval()


    def validate_interval(self):
        self.interval = np.clip(self.interval, self.frameRate, None)
        self.interMin = np.clip(self.interMin, self.frameRate, None)
        self.interMax = np.clip(self.interMax, self.frameRate, None)


    def get_filename(self):
        # Get relative video path from full video path
        self.videoName = self.videoPath.split(dirs.dataset)[1]
        self.videoName = self.videoName.replace("/", "--")

        self.fileName = self.videoName+ " FRAME {}.jpg".format(self.frameCount)
        self.filePath = self.destPath+self.fileName

        return self.filePath


    def _routine_get_frames(self):
        if self.verbose:
            print("Full video frame capture")

        self.timeLimit = self.videoTime
        while self.timePos < self.timeLimit:
            if self.verbose:
                print("Frame ", self.frameCount)
            self.videoError['set'] = self.video.set(cv2.CAP_PROP_POS_MSEC, self.timePos*1000)

            self.frameNum = self.video.get(cv2.CAP_PROP_POS_FRAMES)
            self.videoError['read'], self.frame = self.video.read()

            self.videoError['write'] = cv2.imwrite(self.get_filename(), self.frame)

            self.timePos    += self.interval
            self.frameCount += 1
