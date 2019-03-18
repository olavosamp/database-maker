import cv2
import pandas       as pd
import numpy        as np
import datetime

import libs.dirs    as dirs
import libs.commons as commons
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

        self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
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



class GetFramesCsv(GetFrames):
    '''
        csvPath:  reference csv filepath
        destPath: dataset destination folder
        interval: frame capture interval, in seconds.
    '''
    def __init__(self, csvPath, destPath='./images/', interMin=0.8, interMax=20, verbose=True):
        super().__init__(destPath, verbose=verbose)
        self.csvPath    = csvPath
        self.interMin   = interMin
        self.interMax   = interMax

        # Get csv data
        if self.csvPath != None:
            self.csvData   = self.get_csv_data()
        else:
            raise NameError("CSV filepath not defined.")


    # def validate_csv_path(self):
    #     # Check if csv path exists and if it is a list


    def get_csv_data(self):
        # CSV Data is a pandas DataFrame of the csv file
        self.csvData = pd.read_csv(self.csvPath, dtype=str)
        return self.csvData


    def get_capture_interval(self):
        # self.interval = 20*(runTime[self.eventNum]*self.numEntries/maxFrames)*1000
        self.interval = 20*(self.eventTime*self.numEntries/self.totalFrames)*1000
        self.interval = np.clip(self.interval, self.interMin, self.interMax)
        return self.interval


    def get_filename(self):
        path = self.videoName.replace("/", "--")

        self.fileName  = path+ " {} ID {} FRAME {}.jpg".format(self.eventClass, self.eventNum, self.eventFrames)
        self.framePath = self.destPath+self.fileName

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

        self.videoPath = dirs.dataset+self.csvData.loc[0, 'VideoName']

        self.video = self.get_video_data(self.videoPath)
        print("\nframeRate:", self.frameRate)
        print("totalFrames:", self.totalFrames)
        print()


        # if self.totalFrames == 0:
            # TODO: GET TOTAL FRAMES AND VIDEO TIME SOME WAY

        # self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.videoTime   = self.totalFrames/self.frameRate
        self.numEntries = self.csvData.shape[0]

        self.frameCount = 0
        for self.eventNum in range(self.numEntries):
            self.eventFrames= 0
            self.eventStart = timeConverter(self.csvData.loc[self.eventNum,'StartTime'])*1000
            self.eventEnd   = timeConverter(self.csvData.loc[self.eventNum,'EndTime'])*1000
            self.eventClass = self.csvData.loc[self.eventNum,'Class']
            self.videoName  = self.csvData.loc[self.eventNum, 'VideoName']

            self.eventTime = self.eventEnd - self.eventStart

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

                self.framePath = self.get_filename()
                self.videoError['write'] = cv2.imwrite(self.framePath, self.frame)

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
