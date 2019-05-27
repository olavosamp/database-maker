import pandas       as pd
from pathlib        import Path
from glob           import glob

import libs.dirs    as dirs
from libs.index     import IndexManager
from libs.utils     import image_grid

destFolder = Path(dirs.images) / 'temp' / 'anodo'
targetPath = Path(dirs.images) / 'image_grid' / ('image_grid_'+'anodo'+'.jpg')

image_grid(destFolder, targetPath=targetPath)
