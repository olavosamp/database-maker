import glob

import count
import dirs
import commons
from trimDatabase import trimDatabase

targetDir   = dirs.trim+"dataset_SSIM_{}".format(commons.ssimLim)+dirs.sep
# dataPath    = dirs.images+"20161101202838328@DVR-SPARE_Ch1.wmv"+dirs.sep
dataPath    = dirs.images

trimDatabase(dataPath, targetDir)

# folders = glob.glob(dataPath+'*'+dirs.sep)
# folders = map(lambda x: x.replace('\\', dirs.sep), folders) # Replaces \\ with defined separator
#
# print("")
# for folder in folders:
#     # folder = folder.replace('\\', dirs.sep)
#     print(folder+'\n')
#     imagePaths, labels = count.listImages(folder)
#     print(imagePaths)
#

# tuboCount, nadaCount, confCount, totCount = count.countImages(dataPath)
# print("\nNew frame count:")
# print("Total frames: ", totCount)
# print("   Tubo: ", tuboCount)
# print("   Nada: ", nadaCount)
# print("   Conf: ", confCount)
