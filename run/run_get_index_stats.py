from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas       as pd
from glob           import glob

ind1  = IndexManager()

print(ind1.index.info())
print("")
for elem in ind1.index.columns:
    print(elem)
print("")
print(ind1.get_unique_tags())
print("")
