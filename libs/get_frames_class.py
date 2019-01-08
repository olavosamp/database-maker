import cv2
import pandas as pd

import dirs

class GetFrames:
    def __init__(self, videoPath, csvPath=None, interval=5, destFolder='./images/', verbose=False):
        self.videoPath  = videoPath
        self.csvPath    = csvPath
        self.interval   = interval
        self.destFolder = destFolder
        self.verbose    = verbose

        # Validate video path and file
        

        # Get csv or interval information
        if self.csvPath == None:
            self._from_csv = False
            self.validate_interval()
        else:
            self._from_csv = True
            self.csvData   = self.get_csv_data()

    def get_csv_data(self):
        self.csvData = pd.read_csv(csvPath, dtype=str)
        return self.csvData

    def validate_interval(self):
        self.interval = np.clip(self.interval, self.frameRate, None)
        return self.interval
