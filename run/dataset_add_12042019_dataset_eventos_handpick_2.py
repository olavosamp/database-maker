from   pathlib        import Path
import pandas         as pd
from   glob           import glob

import libs.commons   as commons
from   libs.index     import IndexManager
import libs.dirs      as dirs


ind = IndexManager()

datasetPath = Path(dirs.dataset) / "all_datasets" / "12042019_dataset_eventos_handpick_2"

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
    videoName = None
    for ext in commons.videoFormats:
        extIndex = path.stem.lower().find("." + ext)
        if extIndex != -1:
            videoName = path.stem[:extIndex+4]

            # Exception for VTS videos with report and dvd bundled together with video name
            vtsIndex = videoName.lower().find("vts")
            if vtsIndex != -1:
                videoName = videoName[vtsIndex:]
            break

    if videoName == None:
        raise ValueError("Unable to find video extension for video name detection.")

    # Get VideoPath field
    if dvd != None:
        videoPath = report / Path("DVD-" + dvd) / Path(videoName)
    else:
        videoPath = report / Path(videoName)

    # Get EventId field
    # Find number after "ID". Make exception because of VIDEO strings
    eventId = None

    # Get AbsoluteFrameNumber
    absFrame = path.stem[extIndex+5:]

    # Get RelativeFrameNumber field
    # Find number after "FRAME"
    relFrame = None

    # Get Tags field
    tags = []
    tags.append("evento")
    tags.append(path.parts[-2].lower())

    tags = "-".join(tags)

    # Get FrameName field
    frameName = path.name

    # Get OriginalDataset field
    originalDataset = "12042019_dataset_eventos_handpick_2"

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
    'FrameName':            [frameName],
    'OriginalDataset':      [originalDataset]
    }
    ind.add_entry(entry)

ind.write_index()
