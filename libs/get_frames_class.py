import cv2
import pandas as pd
import numpy  as np

import libs.dirs

class GetFrames:
    def __init__(self, videoPath, csvPath=None, interval=5, destPath='./images/', verbose=False):
        self.videoPath  = videoPath
        self.csvPath    = csvPath
        self.interval   = interval
        self.destPath   = destPath
        self.verbose    = verbose

        # Validate video path and file
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
