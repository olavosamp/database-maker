from getFrames import getFrames
import count
import dirs

## Rebuild Dataset
targetPath = dirs.images + "registro_tags_test" + dirs.sep
csvPath    = dirs.csv    + "registro_tags"      + dirs.sep
'''
    Usage
    rebuildDatasetMulti(csv_folder, videos_folder, target_folder)
    rebuildDataset     (csv_folder, videos_folder, target_folder)
'''

# videoList, csvList, frameTotal = count.rebuildDatasetMulti(csvPath, dirs.base_videos, targetPath)
videoList, csvList, frameTotal = count.rebuildDataset(csvPath, dirs.base_videos, targetPath)

# tuboCount, nadaCount, confCount, totCount = count.countImages(targetPath)
# print("\nTotal frames acquired: ", totCount)
# print("   Tubo: ", tuboCount)
# print("   Nada: ", nadaCount)
# print("   Conf: ", confCount)

print("\nDatabase rebuilt at: \n{}".format(targetPath))
