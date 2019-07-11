import pandas       as pd
from pathlib        import Path
from glob           import glob

import libs.dirs    as dirs
from libs.index     import IndexManager
from libs.utils     import image_grid

ind1  = IndexManager()
print(ind1.index.info())
print("Total images: ", ind1.index.shape[0])
uniqueTags = ind1.get_unique_tags()

for targetTag in uniqueTags:
    ind1 = IndexManager()
    destFolder = Path(dirs.images) / 'temp' / targetTag

    print("Selecting images of class: ", targetTag)
    selectDf = ind1.index.copy()
    f = lambda x: x.split('-')
    selectDf['TagList'] = ind1.index['Tags'].apply(f)

    selectIndex = [i for i,x in enumerate(selectDf['TagList']) if targetTag in x]
    ind1.index = selectDf.loc[selectIndex, :]
    print(len(selectIndex), " images found.")

    ind1.move_files(destFolder=destFolder)

    targetPath = Path(dirs.images) / 'image_grid' / ('image_grid_'+targetTag+'.jpg')

    image_grid(destFolder, targetPath=targetPath)
