from libs.get_frames_class import *

videoPath  = "E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/GHmls16-263_OK/DVD-1/20161101202838328@DVR-SPARE_Ch1.wmv"

getFrames = GetFrames(videoPath, csvPath=None, interval=5, destPath='./images/',
                      verbose=True)

print(getFrames.frameRate)
print(getFrames.videoPath)
print(getFrames.destPath)
