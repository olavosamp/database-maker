from libs.get_frames_class import *

import libs.dirs           as dirs

videoPath  = "E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/GHmls16-263_OK/DVD-1/20161101202838328@DVR-SPARE_Ch1.wmv"

destPath   = dirs.images+'remake/'

getFrames = GetFrames(videoPath, csvPath=None, interval=8000, destPath=destPath,
                      verbose=True)

print(getFrames.frameRate)
print(getFrames.videoPath)
print(getFrames.destPath)

getFrames.get_frames()
