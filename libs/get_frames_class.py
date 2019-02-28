import cv2
import pandas       as pd
import numpy        as np
import datetime

import libs.dirs    as dirs
from libs.utils     import timeConverter

class GetFrames:
    '''
        Base frame extractor class
    '''
    def __init__(self, destPath, verbose=True):
        self.destPath   = destPath
        self.verbose    = verbose

        self.videoError = {'read': True, 'set': True, 'write': True}
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

        self.numFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
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



class GetFramesCsv:
    '''
        csvPath:  reference csv filepath
        destPath: dataset destination folder
        interval: frame capture interval, in seconds.
    '''
    def __init__(self, csvPath, destPath='./images/', verbose=True):
        super().__init__(destPath, verbose=verbose)
        self.csvPath    = csvPath

        # Get csv data
        if self.csvPath != None:
            self.csvData   = self.get_csv_data()
        else:
            raise NameError("CSV filepath not defined.")


    def get_csv_data(self):
        self.csvData = pd.read_csv(self.csvPath, dtype=str)
        return self.csvData


    def get_capture_interval(self):
        self.interval = 20*(runTime[self.event]*self.numEntries/maxFrames)*1000
        self.interval = np.clip(self.interval, self.interMin, self.interMax)
        return self.interval


    def get_filename(self):
        path = self.videoName.replace("/", "--")

        self.fileName = path+ " {} ID {} FRAME {}.jpg".format(self.eventClass, self.event, self.eventFrame)
        self.filePath = self.destPath+self.fileName

        return self.filePath


    def _routine_get_frames(self):
        self.numEntries = self.csvData.shape[0]

        for self.event in range(self.numEntries):
            self.eventFrames= 0
            self.eventStart = timeConverter(self.csvData.loc[self.event,'StartTime'])*1000
            self.eventEnd   = timeConverter(self.csvData.loc[self.event,'EndTime'])*1000
            self.eventClass = self.csvData.loc[self.event,'Class']
            self.videoName  = self.csvData[self.event, 'VideoName']

            if self.eventClass not in commons.classes:
                print("\n\nError: Proposed class is not in accepted classes list.\nSkipping entry.\n\n")
                continue

            self.interval  =  self.get_capture_interval()

            self.timePos   = self.eventStart
            self.timeLimit = self.eventEnd
            while self.timePos < self.timeLimit:
                if self.verbose:
                    print("Frame ", self.eventFrames)
                self.videoError['set'] = self.video.set(cv2.CAP_PROP_POS_MSEC, self.timePos*1000)

                self.frameNum = self.video.get(cv2.CAP_PROP_POS_FRAMES)
                self.videoError['read'], self.frame = self.video.read()

                self.videoError['write'] = cv2.imwrite(self.get_filename(), self.frame)

                self.timePos     += self.interval
                self.eventFrames += 1

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
