from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas as pd

videoPath = Path(dirs.dataset+"CIMRL10-676_OK/PIDF-1 PO MRL-021_parte1.mpg")
framePath = Path(dirs.images+"testcsv/frame01.jpg")

newEntry = {
            'VideoPath':            [str(videoPath)],
            'Report':               ['CIMRL10-676_OK'],
            'DVD':                  [1],
            'VideoName':            ['PIDF-1 PO MRL-021_parte1.mpg'],
            'EventId':              [1],
            'FrameTime':            [000000],
            'AbsoluteFrameNumber':  [1],
            'RelativeFrameNumber':  [1],
            'Tags':                 ['duto-peixe-anodo'],
            'FramePath':            [framePath]
}
# print("New entry:")
# print(newEntry)
# for key in newEntry.keys():
#     print(key)
# t = pd.read_csv(dirs.index)
# t = pd.DataFrame.from_dict(newEntry)
# print(t.shape)
# print(t)
#
# newDf = pd.DataFrame.from_dict(newEntry)
# t = t.append(newDf).reset_index(drop=True)
# print(t.shape)
# print(t)

# print()
# ind = IndexManager()
# ind.add_entry(newEntry)
# ind.add_entry(newEntry)
# # for col in ind.index.columns:
# #     print(col)
# # print(ind.index.columns)
# # ind.add_entry(newEntry)
# print(ind.index)
# ind.write_index()

ind  = IndexManager()
datasets = ["12042019_dataset_eventos_handpick_2",
            "12042019_dataset_eventos_TCO",
            "12042019_dataset_handpicked_Events_1.1",
            "dataset_registro_tags_2019-02_rev1",
            "dataset_registro_de_eventos"
]
# print(ind.index['OriginalDataset'])
# print(datasets[0])
for ds in datasets:
    mask = ind.index['OriginalDataset'] == ds
    print(ds, ": ",  (ind.index.loc[mask, 'OriginalDataset']).shape)
