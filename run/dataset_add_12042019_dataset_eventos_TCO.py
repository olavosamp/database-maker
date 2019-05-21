from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas       as pd
from glob           import glob

ind = IndexManager()

datasetPath = Path(dirs.dataset) / "all_datasets" / "12042019_dataset_eventos_TCO"

globList = glob(str(datasetPath / '**' / '*.jpg'), recursive=True)

pathList = []
for path in globList:
    pathList.append(Path(path))

datasetDf = pd.DataFrame()
for path in pathList:
    print(path.parts)
    relPath = path.relative_to(datasetPath)

    # Get DVD field
    folderName = relPath.parts[0]
    dvdIndex = str(folderName).find("DVD-")
    if dvdIndex == -1:
        raise ValueError("In this dataset, DVD information should be in the folder name.")
    else:
        dvd = str(folderName)[dvdIndex+4]

    # Get Report field
    report = "TCOpm16-140_OK"

    # Get VideoName field, dont get dvd name in this field
    videoName = folderName[dvdIndex+6:]

    # Get VideoPath field
    videoPath = report / Path("DVD-" + dvd) / Path(videoName +".VOB")

    # Get EventId field
    eventId = None

    # Get RelativeFrameNumber field
    relFrame = None

    # Get AbsoluteFrameNumber field
    absFrame = path.stem.split("_")[-1]

    # Get Tags field
    tags = ['evento']
    folderTag = path.parts[-2]
    if folderTag.find("Outros") != -1 or folderTag.find("outros") != -1:
        tags.append('outros')
    elif folderTag.find("Limpo") != -1 or folderTag.find("limpo") != -1:
        tags.append("limpo")
    else:
        tags.append(folderTag.lower())

    # Join tags with '-'
    tags = "-".join(tags)

    # Get FrameName field
    frameName = path.name

    # Get OriginalDataset field
    originalDataset = "12042019_dataset_eventos_TCO"

    # Get FramePath field
    # TODO: Move each frame to a permanent dataset folder and use this path as FramePath
    framePath = str(path)

    # print('VideoPath ', videoPath)
    # print('Report ', report)
    # print("dvd: ", dvd)
    # print("videoname: ", videoName)
    # print('EventId: ', eventId)
    # # print('FrameTime: ', )
    # print('AbsoluteFrameNumber: ', absFrame)
    # print('RelativeFrameNumber: ', relFrame)
    # print('Tags: ', tags)
    # print('FramePath: ', framePath)
    # print("OriginalDataset: ", originalDataset)
    # input()

    entry = {
    'VideoPath':            [videoPath],
    'Report':               [report],
    'DVD':                  [dvd],
    'VideoName':            [videoName],
    'EventId':              [eventId],
    'FrameTime':            [None],
    'AbsoluteFrameNumber':  [absFrame],
    'RelativeFrameNumber':  [relFrame],
    'Tags':                 [tags],
    'FramePath':            [framePath],
    'FrameName':            [frameName],
    'OriginalDataset':      [originalDataset]
    }

    # print()
    # for e in entry:
    #     print(e, ": ", entry[e])
    ind.add_entry(entry)

ind.write_index()
