import os
import cv2
import glob
import numpy 			as np
import pandas 			as pd
from tqdm 				import tqdm
from skimage.measure 	import compare_ssim

import dirs
import count
import commons

# def trimDatabase(dataPath, targetDir):
#     # Scan the dataset and search for frames that are in accordance to some metric
#     # Then saves those frames in a new path
#
#     imagePaths, labels = count.listImages(dataPath)
#     # Get new directory path
#     videoName = imagePaths[0].split(dirs.sep)[-1].split(" ")[0]
#     targetDir = targetDir+videoName+dirs.sep
#
#     ssimLim = 0.600     # SSIM comparison threshold
#     numImages = len(imagePaths)
#
#     try:
#         os.makedirs(targetDir)
#     except OSError:
#         pass
#
#     # Report original frame count
#     tuboCount, nadaCount, confCount, totCount = count.countImages(dataPath)
#     print("Trimming database with criteria:")
#     print("SSIM <= {}".format(ssimLim))
#     print("\nOriginal frame count:")
#     print("Total frames: ", totCount)
#     print("   Tubo: ", tuboCount)
#     print("   Nada: ", nadaCount)
#     print("   Conf: ", confCount)
#
#     # Always save first frame
#     newSet = []
#     image1 = cv2.imread(imagePaths[0])
#     newSet.append(imagePaths[0])
#
#     newCount = 1
#     for path in tqdm(imagePaths):
#         image2 = cv2.imread(path)
#
#         ssimFrame = compare_ssim(image1, image2, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False)
#
#         if ssimFrame <= ssimLim:
#             newSet.append(path)
#             imageName = path.split(dirs.sep)[-1]
#
#             newPath = targetDir+imageName
#             errWrite = cv2.imwrite(newPath, image2)
#
#             image1 = image2
#             newCount += 1
#
#     print("\nNew dataset has {} frames.\n".format(newCount))
#
#     tuboCount, nadaCount, confCount, totCount = count.countImages(targetDir)
#     print("\nNew frame count:")
#     print("Total frames: ", totCount)
#     print("   Tubo: ", tuboCount)
#     print("   Nada: ", nadaCount)
#     print("   Conf: ", confCount)
#
#     return newCount

def trimDatabase(dataPath, targetDir):
    # Scan the dataset and search for frames that are in accordance to some metric
    # Then saves those frames in a new path

    ssimLim = commons.ssimLim     # SSIM comparison threshold

    # Scan given path for subdirectories
    folders = glob.glob(dataPath+'*'+dirs.sep)
    folders = map(lambda x: x.replace('\\', dirs.sep), folders) # Replaces \\ with defined separator

    # If there are no subdirectories in dataPath, use it as the only directory
    if not folders:
        folders = dataPath

    print("\nTrimming database with criteria:")
    print("SSIM <= {}".format(ssimLim))

    totCountFull  = 0
    tuboCountFull = 0
    nadaCountFull = 0
    confCountFull = 0
    # Trim each subdirectory
    for folderPath in tqdm(folders):
        imagePaths, labels = count.listImages(folderPath)
        # Get new directory path
        videoName = imagePaths[0].split(dirs.sep)[-1].split(" ")[0]
        targetSubdir = targetDir+videoName+dirs.sep

        numImages = len(imagePaths)

        try:
            os.makedirs(targetSubdir)
        except OSError:
            pass

        # Report original frame count
        tuboCount, nadaCount, confCount, totCount = count.countImages(folderPath)
        print("\nOriginal frame count for video\n{}:".format(videoName))
        print("Total frames: ", totCount)
        print("   Tubo: ", tuboCount)
        print("   Nada: ", nadaCount)
        print("   Conf: ", confCount)

        # Always save first frame
        newSet = []
        image1 = cv2.imread(imagePaths[0])
        newSet.append(imagePaths[0])

        newCount = 1
        for path in tqdm(imagePaths):
            image2 = cv2.imread(path)

            ssimFrame = compare_ssim(image1, image2, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False)

            if ssimFrame <= ssimLim:
                newSet.append(path)
                imageName = path.split(dirs.sep)[-1]

                newPath = targetSubdir+imageName
                errWrite = cv2.imwrite(newPath, image2)

                image1 = image2
                newCount += 1

        # print("\nNew dataset has {} frames.\n".format(newCount))

        tuboCount, nadaCount, confCount, totCount = count.countImages(targetDir)
        print("\nNew frame count for video\n{}:".format(videoName))
        print("Total frames: ", totCount)
        print("   Tubo: ", tuboCount)
        print("   Nada: ", nadaCount)
        print("   Conf: ", confCount)

        totCountFull  += totCount
        tuboCountFull += tuboCount
        nadaCountFull += nadaCount
        confCountFull += confCount

    print("\nNew dataset total frame count:")
    print("Total frames: ", totCountFull)
    print("   Tubo: ", tuboCountFull)
    print("   Nada: ", nadaCountFull)
    print("   Conf: ", confCountFull)

    return newCount
