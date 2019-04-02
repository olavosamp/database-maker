from libs.get_frames_class import *

import libs.dirs           as dirs

destPath   = dirs.images+'testcsv/'
csvPathList = [dirs.csv+"csv_unificado/TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.csv",
               dirs.csv+"csv_unificado/TVILL16-054_OK/DVD-1/Dive 420 16-02-24 20.02.35_C1.csv",
               dirs.csv+"csv_unificado/TVILL16-054_OK/DVD-2/Dive 420 16-02-25 00.02.35_C1.csv",
]

for csvPath in csvPathList:
    getFrames = GetFramesCsv(csvPath, destPath=destPath, verbose=True)

    print("\nProcessing csv: ", csvPath)
    getFrames.get_frames()
    print("\nProcessing finished.")
    print(getFrames.videoPath)
    print(getFrames.frameRate)
    print(getFrames.destPath)
    print("\nError logs:")
    print(getFrames.errorCounter)
    for elem in getFrames.errorList:
        print(elem)
