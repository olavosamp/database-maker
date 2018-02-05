from getFrames import getFrames, getFramesFull, getFramesSSIM
import count
import dirs

# Get Frames single video
# videoPath = dirs.dataset+"CIMRL10-676_OK"+dirs.sep+"PIDF-1 PO MRL-021_parte2.mpg"
# csvPath = dirs.csv+"CIMRL10-676_OK"+dirs.sep+"PIDF-1 PO MRL-021_parte2.csv"
videoPath = dirs.dataset+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161101205058500@DVR-SPARE_Ch1.wmv"
csvPath = dirs.csv+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161101205058500@DVR-SPARE_Ch1.csv"

targetPath = "".."+dirs.sep+".."+dirs.sep+"testfolder"+dirs.sep

# frameTotal = getFrames(videoPath, csvPath)
frameTotal = getFramesFull(videoPath, csvPath, targetPath)

print("{} images obtained.".format(frameTotal))
csvTotals = count.countCsv()
print("\nTotal potential images (classified and recorded in csv):\n", csvTotals)

# ## Rebuild Dataset
# targetPath = dirs.new_images+'dataset_tmax_20s_tmin_1_2s'+dirs.sep
# videoList, csvList, frameTotal = count.rebuildDataset(dirs.registro_de_eventos, dirs.dataset, targetPath)
#
# # tuboCount, nadaCount, confCount, totCount = count.countImages(targetPath)
# # print("\nTotal frames acquired: ", totCount)
# # print("   Tubo: ", tuboCount)
# # print("   Nada: ", nadaCount)
# # print("   Conf: ", confCount)
#
# print("\nDatabase rebuilt at: \n{}".format(targetPath))

## Get Frames SSIM
# videoPath = dirs.dataset+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161102010731375@DVR-SPARE_Ch1.wmv"
# csvPath = dirs.csv+"GHmls16-263_OK"+dirs.sep+"DVD-1"+dirs.sep+"20161102010731375@DVR-SPARE_Ch1.csv"
#
# targetPath = dirs.images+"ssim"+dirs.sep
#
# frameTotal = getFramesSSIM(videoPath, csvPath, targetPath)
#
# print("{} images obtained.".format(frameTotal))
