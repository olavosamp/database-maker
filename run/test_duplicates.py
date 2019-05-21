from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas       as pd
from glob           import glob

ind = IndexManager()

datasetPath = Path(dirs.dataset) / "all_datasets" / "12042019_dataset_handpicked_Events_1.1"

globList = glob(str(datasetPath / '**' / '*.jpg'), recursive=True)

pathList = []
for path in globList:
    pathList.append(Path(path))

videoPath = Path(dirs.dataset+"CIMRL10-676_OK/PIDF-1 PO MRL-021_parte1.mpg")
framePath = Path(dirs.images+"testcsv/frame01.jpg")

newEntry0 = {
            'Report':               ['CIMRL10-676_OK'],
            'DVD':                  [1],
            'VideoName':            ['PIDF-1 PO MRL-021_parte1.mpg'],
            'Tags':                 ['duto-peixe-anodo'],
            'FrameName':            ['PIDF-1_PO_MRL-021_parte3.mpg_115080.jpg'],
            'FramePath':            ['PIDF-1_PO_MRL-021_parte3.mpg_115080.jpg'],
            'OriginalDataset':      ['dataset1']
}

newEntry1 = {
            'Report':               ['CIMRL10-676_OK'],
            'DVD':                  [1],
            'VideoName':            ['PIDF-1 PO MRL-021_parte1.mpg'],
            'Tags':                 ['duto-zoom'],
            'FrameName':            ['PIDF-1_PO_MRL-021_parte3.mpg_115080.jpg'],
            'FramePath':            ['PIDF-1_PO_MRL-021_parte3.mpg_115080.jpg'],
            'OriginalDataset':      ['dataset2']
}

newEntry2 = {
            'Report':               ['GHmls16-263'],
            'DVD':                  [2],
            'VideoName':            ['20161102045347140@DVR-SPARE_Ch1.wmv'],
            'Tags':                 ['duto-flange'],
            'FrameName':            ['20161101212059250@DVR-SPARE_Ch1.wmv ID17 FRAME5 tubo.jpg'],
            'FramePath':            ['GHmls16-263/DVD-1/20161101212059250@DVR-SPARE_Ch1.wmv/20161101212059250@DVR-SPARE_Ch1.wmv ID17 FRAME5 tubo.jpg'],
            'OriginalDataset':      ['dataset1']
}

newEntry3 = {
            'Report':               ['GHmls16-263'],
            'DVD':                  [2],
            'VideoName':            ['20161102045347140@DVR-SPARE_Ch1.wmv'],
            'Tags':                 ['duto-flange-anodo'],
            'FrameName':            ['20161101212059250@DVR-SPARE_Ch1.wmv ID17 FRAME5 tubo.jpg'],
            'FramePath':            ['GHmls16-263/DVD-1/20161101212059250@DVR-SPARE_Ch1.wmv/20161101212059250@DVR-SPARE_Ch1.wmv ID17 FRAME5 tubo.jpg'],
            'OriginalDataset':      ['dataset_robert']
}

ind  = IndexManager()

# print(ind.index.info())

print("\n\n")
print("Entry 0")
ind.add_entry(newEntry0)
print(ind.index)
input()

print("\n\n")
print("Entry 1")
ind.add_entry(newEntry1)
print(ind.index)
input()

print("\n\n")
print("Entry 2")
ind.add_entry(newEntry2)
print(ind.index)
input()

print("\n\n")
print("Entry 3")
ind.add_entry(newEntry3)
print(ind.index)
input()

# ind.check_duplicates()
# print(ind.index)
#
# # print("\n\nIndex:\n")
# # print(ind.index)
# # print("\n\n")
#
# # ind.check_duplicates()
#
# # print(ind.index)
#
# # ind.write_index()
