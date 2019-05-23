import  os
from   pathlib        import Path
import pandas         as pd
import numpy          as np
from   glob           import glob

import libs.commons   as commons
import libs.dirs      as dirs

ignoreTag = 'ignore_train'


deletePath = Path(dirs.dataset) / "datasets_roberto_delete"
datasetPath = Path(dirs.dataset) / "datasets_roberto"

globDeleteList = glob(str(deletePath / '**' / '*.jpg'), recursive=True)

print("Files to add 'ignore' Tag.")
for path in globDeleteList:
    path = Path(path).relative_to(deletePath)
    # print(path.parts)
    # print((datasetPath / path).parts)
    # input()
    os.remove(datasetPath / path)
    # deleteThis = path.parts[]
