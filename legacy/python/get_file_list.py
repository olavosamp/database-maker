# from PIL import Image
from os import listdir
from os.path import isfile, join

import dirs
import commons

def listVideos(dataPath):
    '''
        dataPath is the path of the image folder to be read

        Finds videos inside dataPath and lists all corresponding image paths

    	Returns videoPaths
    	videoPaths contains every video filepath
    '''
    from glob import glob

    videoPaths  = []

    # Find every file in the root path
    for ext in commons.videoFormats:
    	for filePath in glob(dataPath+'**'+dirs.sep+'*.'+ext, recursive=True):
            # Replace backslashes with defined separator (in dirs) for compatibility
            filePath = filePath.replace("\\", dirs.sep)

            # print("\n"+filePath)

            # Ignore vob headers
            if filePath.find("VIDEO_TS") > 0:
            	print("This is not a video")
            else:
            	videoPaths.append(filePath)
    return videoPaths

## List dataset folders
# dirPath = "E:/Projeto Final/Projeto Petrobras/datasets/dataset_handpicked/"
#
# folders = [ join(dirPath, f) for f in listdir(dirPath) if not(isfile(join(dirPath, f))) ]
#
# print("")
# for folder in folders:
#     print(folder)
#     print("")

videoPaths = listVideos(dirs.base_videos)

## List videos
# print("")
# for video in videoPaths:
#     print(video)
#     print("")

## Save videos to file
logPath = "E:/Projeto Final/Projeto Petrobras/resultados/lista_videos.txt"
file = open(logPath, 'w')
for video in videoPaths:
    file.writelines(video+"\n")
file.close()
