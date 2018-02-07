import os
from collections import Counter
import count
import dirs
import pandas as pd

csvFolder = dirs.registro_de_eventos
videoFolder = dirs.dataset
targetPath = dirs.new_images+"registroTest"+dirs.sep

frameTotal = count.rebuildDatasetMulti(csvFolder, videoFolder, targetPath)
