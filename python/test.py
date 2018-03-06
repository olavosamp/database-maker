import os
from collections import Counter
import count
import dirs
import pandas as pd
import numpy as np

newList = [0, 1, 3, 4, 4]

uniques = list(Counter(newList))
numElements = len(uniques)

print(uniques)
newDict = dict(zip(uniques, np.zeros(numElements, dtype=np.int32)))
print(newDict)

print(newDict[3])
newDict[3] += 1

print(newDict[3])

sum1 = np.sum(newDict)
print(sum1)

# csvFolder = dirs.registro_de_eventos
# videoFolder = dirs.dataset
# targetPath = dirs.new_images+"registroTest"+dirs.sep
#
# frameTotal = count.rebuildDatasetMulti(csvFolder, videoFolder, targetPath)
