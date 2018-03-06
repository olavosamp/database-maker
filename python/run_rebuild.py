from getFrames import getFrames
import count
import dirs

## Rebuild Dataset
targetPath = dirs.images+'registroTest'+dirs.sep

videoList, csvList, frameTotal = count.rebuildDatasetMulti(dirs.registro_de_eventos, dirs.dataset, targetPath)

# tuboCount, nadaCount, confCount, totCount = count.countImages(targetPath)
# print("\nTotal frames acquired: ", totCount)
# print("   Tubo: ", tuboCount)
# print("   Nada: ", nadaCount)
# print("   Conf: ", confCount)

print("\nDatabase rebuilt at: \n{}".format(targetPath))
