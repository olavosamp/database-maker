from getFrames import getFrames
import count
import dirs

## Rebuild Dataset
targetPath = dirs.images+'registro_de_eventos_test'+dirs.sep
# Usage
# rebuildDatasetMulti(csv_folder, videos_folder, target_folder)
videoList, csvList, frameTotal = count.rebuildDatasetMulti(dirs.csv+"registro_de_eventos_test"+dirs.sep, dirs.dataset, targetPath)

# tuboCount, nadaCount, confCount, totCount = count.countImages(targetPath)
# print("\nTotal frames acquired: ", totCount)
# print("   Tubo: ", tuboCount)
# print("   Nada: ", nadaCount)
# print("   Conf: ", confCount)

print("\nDatabase rebuilt at: \n{}".format(targetPath))
