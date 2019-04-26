from libs.get_frames_class import *

import libs.dirs           as dirs

# videoPath  = "E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/GHmls16-263_OK/DVD-1/20161101202838328@DVR-SPARE_Ch1.wmv"
# videoPath  = dirs.base_videos+"TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.wmv"
videoPath  = dirs.base_videos+"TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.wmv"
destPath   = dirs.images+'test/'
dirs.create_folder(destPath)

getFrames = GetFramesFull(videoPath, destPath=destPath, interval=60,
                      verbose=True)

print(getFrames.frameRate)
print(getFrames.videoPath)
print(getFrames.destPath)

getFrames.get_frames()
