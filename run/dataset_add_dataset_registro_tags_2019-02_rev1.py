from pathlib        import Path
from libs.index     import IndexManager

import libs.dirs    as dirs
import pandas       as pd
from glob           import glob

ind = IndexManager()

datasetPath = Path(dirs.dataset) / "all_datasets" / "dataset_registro_tags_2019-02_rev1"

globList = glob(str(datasetPath / '**' / '*.jpg'), recursive=True)

pathList = []
for path in globList:
    pathList.append(Path(path))

datasetDf = pd.DataFrame()
for path in pathList:
    print(path.parts)
    relPath = path.relative_to(datasetPath)

    # Get Report field
    report = relPath.parts[0]

    # Get DVD field
    dvdIndex = str(path).find("DVD-")
    if dvdIndex == -1:
        dvd = None
    else:
        dvd = str(path)[dvdIndex+4]

    # Get VideoName field, dont get dvd name in this field
    videoName = relPath.parts[-2]
    if videoName.find("Dive") != -1:
        videoName += ".wmv"

    # Get VideoPath field
    videoPath = report / Path("DVD-" + dvd) / Path(videoName)

    # Get EventId field
    # Find number after "ID". Make exception because of VIDEO strings
    idSubPath = path.stem[path.stem.find(" ID")+1:].split(" ")[0]
    eventId = idSubPath[2:]

    # Get AbsoluteFrameNumber
    absFrame = None

    # Get RelativeFrameNumber field
    # Find number after "FRAME"
    frameSubPath = path.stem[path.stem.find("FRAME"):].split(" ")[0]
    relFrame = frameSubPath[5:]

    # Get Tags field
    tags = []
    tagsSubstring = path.stem[path.stem.find("FRAME"):]
    for tag in tagsSubstring.split(" ")[1:]:
        tags.append(tag)
    tags = "-".join(tags)

    # Get OriginalDataset field
    originalDataset = "dataset_registro_tags_2019-02_rev1"

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
    # # print('FramePath: ', str)
    # print("OriginalDataset: ", originalDataset)
    # input()

    entry = {
    'VideoPath':            [videoPath],
    'Report':               [report],
    'DVD':                  [dvd],
    'VideoName':            [videoName],
    'EventId':              [eventId],
    'FrameTime':            [None],
    'AbsoluteFrameNumber':  [None],
    'RelativeFrameNumber':  [relFrame],
    'Tags':                 [tags],
    'FramePath':            [framePath],
    'OriginalDataset':      [originalDataset]
    }
    ind.add_entry(entry)

ind.write_index()
