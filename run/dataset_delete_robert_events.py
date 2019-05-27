from   pathlib        import Path
import pandas         as pd
import numpy          as np
from   glob           import glob

import libs.commons   as commons
from   libs.index     import IndexManager
import libs.dirs      as dirs

ignoreTag = 'ignore_train'

ind = IndexManager()

datasetPath = Path(dirs.dataset) / "datasets_roberto_delete"

globList = glob(str(datasetPath / '**' / '*.jpg'), recursive=True)

print("Files to add 'ignore' Tag.")
pathList = []
for path in globList:
    pathList.append(Path(path))
    print(path)

print("\n\nSearch start.\n")
for path in pathList:
    f = lambda x: x.find(path.name)
    # Find which entries have matching frame names
    mask = ind.index.loc[:, 'FrameName'].copy().apply(f)
    mask = np.where(mask != -1, True, False)    # Create True/False mask

    print("\nSearching for", path.name)
    print("Found {} matches.".format(mask.sum()))
    assert mask.sum() <= 1, "More than one match. Could not resolve."

    # Append new tag
    entryIndex = int(np.squeeze(np.argwhere(mask)))
    print(entryIndex)
    ind.append_tag(entryIndex, ignoreTag)

print(len(pathList))

ind.write_index()
