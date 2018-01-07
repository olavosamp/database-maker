# from getFrames import getFrames
from getFrames import getFramesFull
import count
import dirs

# videoPath = dirs.dataset+"\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.mpg"
# csvPath = dirs.csv+"\\CIMRL10-676_OK\\PIDF-1 PO MRL-021_parte2.csv"
videoPath = dirs.dataset+"GHmls16-263_OK\\DVD-1\\20161101205058500@DVR-SPARE_Ch1.wmv"
csvPath = dirs.csv+"\\GHmls16-263_OK\\DVD-1\\20161101205058500@DVR-SPARE_Ch1.csv"

targetPath = '..\\..\\testfolder\\'

# frameTotal = getFrames(videoPath, csvPath)
frameTotal = getFramesFull(videoPath, csvPath, targetPath)

print("{} images obtained.".format(frameTotal))

# csvTotals = count.countCsv()
# print("\nTotal potential images (classified and recorded in csv):\n", csvTotals)

# videoList, csvList, frameTotal = count.rebuildDataset(dirs.csv, dirs.dataset)
#
# labels = count.listImages(dirs.images)
# frameTotal = count.countImages(labels)
# print("{} frames obtained.".format(frameTotal))
# print("\nDatabase rebuilt.")
