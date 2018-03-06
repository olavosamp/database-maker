import os
from collections import Counter
import count
import dirs
import pandas as pd

csvFolder   = "csv"+dirs.sep
videoFolder = "videos"+dirs.sep
targetPath  = "images"+dirs.sep

try:
    os.makedirs(targetPath)
except OSError:
    pass

frameTotal = count.rebuildDatasetMulti(dirs.registro_de_eventos, dirs.dataset, dirs.images+"registro_de_eventos"+dirs.sep)

input("\nCaptura de frames finalizada. Pressione Enter para sair.")
