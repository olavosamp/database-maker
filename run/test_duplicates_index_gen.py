from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas       as pd
from glob           import glob

path1 = dirs.csv+'main_index_2019-5-20_19-56-2.csv'
# path2 = dirs.csv+'main_index_CHECK_DUPS_2019-5-20_18-7-11.csv'

ind1  = IndexManager(path=path1)
# ind2  = IndexManager(path=path2)

print(ind1.index.info())
# print(ind2.index.info())
print("")

check1     = ind1.index.duplicated(['Report'], keep=False)
check2     = ind1.index.duplicated(['DVD'], keep=False)
check3     = ind1.index.duplicated(['FrameName'], keep=False)

# print(check1)
# input()
# print(check2)
# input()
# print(check3)

print(check1.sum())
print(check2.sum())
print(check3.sum())
print(check1.shape)
print(ind1.index.loc[check3])

# Split Tags fields
# tagList = []
# f = lambda x: tagList.extend(x.split('-'))
# ind.index['Tags'].apply(f)
# tagList = list(dict.fromkeys(tagList))
# print(ind1.get_unique_tags())
# print(ind2.get_unique_tags())
