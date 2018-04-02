from getFrames import getFrames
import count
import dirs

## Rebuild Dataset
targetPath = dirs.images+'registroTestRev1_take2'+dirs.sep
# Usage
# rebuildDatasetMulti(csv_folder, videos_folder, target_folder)
videoList, csvList, frameTotal = count.rebuildDatasetMulti(dirs.csv+"registro_de_eventos_rev1"+dirs.sep, dirs.dataset, targetPath)

# tuboCount, nadaCount, confCount, totCount = count.countImages(targetPath)
# print("\nTotal frames acquired: ", totCount)
# print("   Tubo: ", tuboCount)
# print("   Nada: ", nadaCount)
# print("   Conf: ", confCount)

print("\nDatabase rebuilt at: \n{}".format(targetPath))
