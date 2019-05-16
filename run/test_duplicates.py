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

newEntry = {
            # 'VideoPath':            [str(videoPath)],
            'Report':               ['CIMRL10-676_OK'],
            'DVD':                  [1],
            'VideoName':            ['PIDF-1 PO MRL-021_parte1.mpg'],
            # 'EventId':              [1],
            # 'FrameTime':            [000000],
            # 'AbsoluteFrameNumber':  [1],
            # 'RelativeFrameNumber':  [1],
            'Tags':                 ['duto-peixe-anodo'],
            'FrameName':            ['PIDF-1 PO MRL-021_parte1.mpg'],
            # 'FramePath':            [framePath]
}

newEntry2 = {
            'Report':               ['GHmls16-263'],
            'DVD':                  [2],
            'VideoName':            ['20161102045347140@DVR-SPARE_Ch1.wmv'],
            'Tags':                 ['duto-flange'],
            'FrameName':            ['20161102045347140@DVR-SPARE_Ch1.wmv'],
}

newEntry3 = {
            'Report':               ['GHmls16-263'],
            'DVD':                  [2],
            'VideoName':            ['20161102045347140@DVR-SPARE_Ch1.wmv'],
            'Tags':                 ['duto-flange-anodo'],
            'FrameName':            ['20161102045347140@DVR-SPARE_Ch1.wmv'],
}



ind  = IndexManager()

ind.add_entry(newEntry)
print("\n\n")
print(ind.index)
ind.add_entry(newEntry2)
print("\n\n")
print(ind.index)
ind.add_entry(newEntry3)
print("\n\n")
print(ind.index)
# print("\n\nIndex:\n")
# print(ind.index)
# print("\n\n")

# ind.check_duplicates()

# print(ind.index)

# ind.write_index()
