import cv2
import pandas as pd
import numpy  as np
import datetime

import libs.dirs as dirs

class GetFrames:
    '''
        interval: frame capture interval, in seconds.
    '''
    def __init__(self, videoPath, csvPath=None, interval=5, destPath='./images/', verbose=False):
        if verbose:
    	       print("\nUsing opencv version: ", cv2.__version__)

        self.videoPath  = videoPath
        self.csvPath    = csvPath
        self.interval   = interval
        self.destPath   = destPath
        self.verbose    = verbose

        self.videoError = dict()
        self.frameCount = 0

        # Validate video path and file
        dirs.create_folder(self.destPath)
        self.video = self.get_video_data()

        # Get csv or interval information
        if self.csvPath == None:
            self._from_csv = False
            self.validate_interval()
        else:
            self._from_csv = True
            self.csvData   = self.get_csv_data()

    def get_csv_data(self):
        self.csvData = pd.read_csv(self.csvPath, dtype=str)
        return self.csvData

    def validate_interval(self):
        self.interval = np.clip(self.interval, self.frameRate, None)
        return self.interval

    def get_video_data(self):
        try:
        	self.video = cv2.VideoCapture(self.videoPath)
        except:
            print("\nError opening video:\n")
            cv2.VideoCapture(self.videoPath)

        self.frameRate = self.video.get(cv2.CAP_PROP_FPS)
        return self.video

    def get_frames(self):
        self.totalFrames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.videoTime   = self.totalFrames/self.frameRate
        if self.verbose:
            print("Total video time:")
            print(str(datetime.timedelta(seconds=self.videoTime)))

        if self._from_csv:
            raise NotImplementedError("Frame extraction from csv file not yet implemented")
        else:
            if self.verbose:
                print("")
            self.timePos    = 0
            self.frameCount = 0

            while self.timePos < self.videoTime:
                if self.verbose:
                    print("Frame ", self.frameCount)
                self.videoError['set'] = self.video.set(cv2.CAP_PROP_POS_MSEC, self.timePos*1000)

                self.frameNum = self.video.get(cv2.CAP_PROP_POS_FRAMES)
                self.videoError['read'], self.frame = self.video.read()

                # self.framePath = dirs.images+'test_remake/'
                self.framePath = self.destPath
                self.framePath += 'FRAME_{}.jpg'.format(self.frameCount)

                self.videoError['write'] = cv2.imwrite(self.framePath, self.frame)

                self.timePos    += self.interval
                self.frameCount += 1
