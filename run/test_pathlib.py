from glob import glob
from pathlib               import Path
import libs.dirs           as dirs
import cv2

from libs.get_frames_class import *

# destPath   = dirs.images / Path('testcsv/')
# csvPathList = [dirs.csv+"csv_unificado/TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.csv",
#                dirs.csv+"csv_unificado/TVILL16-054_OK/DVD-1/Dive 420 16-02-24 20.02.35_C1.csv",
#                dirs.csv+"csv_unificado/TVILL16-054_OK/DVD-2/Dive 420 16-02-25 00.02.35_C1.csv",
# ]
relative = "/TVILL16-054_OK/DVD-1/Dive 420 16-02-24 19.32.32_C1.wmv"
videoPath = dirs.dataset / Path(relative)

# baseCsv = Path(dirs.csv)
# print(dirs.csv)
# print(baseCsv)
#
# baseDest = Path(dirs.images)
# print(dirs.images+"testcsv/")
# print(baseDest / Path("testcsv/"))

print(videoPath)
print(dirs.dataset)
# destPath = Path(videoPath).relative_to(str(dirs.dataset))
# destPath = Path(dirs.images / "testcsv/") / destPath
# print(destPath)
#
# folderPath = destPath.parent / destPath.stem
# print(folderPath)
#
# print("--".join(folderPath.parts))
# exit()
#
# framePath  = folderPath / Path(str(destPath.stem) + " ID1 FRAME00 duto.jpg")
# print(framePath)
#
# # video = cv2.VideoCapture(str(q))
