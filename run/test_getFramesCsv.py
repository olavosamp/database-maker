from libs.get_frames_class import *

import libs.dirs           as dirs

# videoPath  = "E:/Projeto Final/Projeto Petrobras/20170724_FTP83G_Petrobras/GHmls16-263_OK/DVD-1/20161101202838328@DVR-SPARE_Ch1.wmv"
# csvPath = dirs.csv+"registro_tags/FSll16-224_OK/DVD-3/VTS_01_1.csv"
csvPath = dirs.csv+"/csv_unificado/TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.csv"

destPath   = dirs.images+'remake/'

getFrames = GetFramesCsv(csvPath, destPath='./images/testcsv/', verbose=True)

getFrames.get_frames()
print(getFrames.frameRate)
print(getFrames.videoPath)
print(getFrames.destPath)
