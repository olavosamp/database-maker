from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas       as pd
from glob           import glob

path1 = dirs.csv+'main_index_2019-5-21_0-6-46.csv'

ind1  = IndexManager(path=path1)
print(ind1.index.info())
print("")

ind1.move_files()
