from getFrames import getFrames, getFramesFull#, getFramesSSIM
import count
import dirs

# Get Frames single video
# videoPath = dirs.base_videos+"CIMRL10-676_OK"+dirs.sep+"PIDF-1 PO MRL-021_parte2.mpg"
# csvPath = dirs.csv+"CIMRL10-676_OK"+dirs.sep+"PIDF-1 PO MRL-021_parte2.csv"
videoPath = dirs.base_videos+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161101215100437@DVR-SPARE_Ch1.wmv"
csvPath = dirs.csv+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161101215100437@DVR-SPARE_Ch1.csv"
#
targetPath = dirs.images+"framesFull"+dirs.sep

frameTotal = getFramesFull(videoPath, csvPath, targetPath)

print("{} images obtained.".format(frameTotal))
csvTotals = count.countCsv()
print("\nTotal potential images (classified and recorded in csv):\n", csvTotals)

## Get Frames SSIM
# videoPath = dirs.base_videos+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161102010731375@DVR-SPARE_Ch1.wmv"
# csvPath = dirs.csv+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161102010731375@DVR-SPARE_Ch1.csv"
#
# targetPath = dirs.images+"ssim"+dirs.sep
#
# frameTotal = getFramesSSIM(videoPath, csvPath, targetPath)
#
# print("{} images obtained.".format(frameTotal))
