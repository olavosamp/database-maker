from libs.get_frames_class import *

import libs.dirs           as dirs

destBase   = dirs.images+'remake/'

basePath = "E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/"
paths    = [
            # "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 20.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 21.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 21.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 22.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 23.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-1/Dive 420 16-02-24 23.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 00.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 00.32.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 01.02.35_C1.wmv",
            "TVILL16-054_OK/DVD-2/Dive 420 16-02-25 02.32.35_C1.wmv",
]

for path in paths:
    videoPath = basePath+path

    destEnd   = ".".join(path.split(".")[:-1])+"/"
    destPath  = destBase+destEnd

    getFrames = GetFrames(videoPath, csvPath=None, interval=1, destPath=destPath,
                            verbose=True)

    print("Video:\n", getFrames.videoPath)
    print("Saving to: ", getFrames.destPath)

    getFrames.get_frames()
    input()
