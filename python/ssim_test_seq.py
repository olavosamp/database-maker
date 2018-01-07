from skimage.measure import compare_ssim
import cv2      as cv
import numpy    as np
import glob
import os
from tqdm import tqdm

import dirs
import count
from getFrames import getFramesFull

N = 10

basePath    = '..\\..\\testfolder\\'
targetPath  = basePath
# videoPath   = dirs.dataset+'GHmls16-263_OK\\DVD-1\\20161101205058500@DVR-SPARE_Ch1.wmv'
# csvPath     = dirs.csv+'GHmls16-263_OK\\DVD-1\\20161101205058500@DVR-SPARE_Ch1.csv'

# videoName = videoPath.split(os.path.sep)[-1]

# # Get all frames from video
#  frameTotal = getFramesFull(videoPath, csvPath, targetPath)

# List all frame paths
imagePaths = glob.glob(targetPath+'tuboTemp'+os.path.sep+'*.jpg')
# imagePaths = glob.glob(dirs.images+'PIDF-1 PO MRL-021_parte1.mpg'+os.path.sep+'*.jpg')

# print('\n'+targetPath+videoName+os.path.sep+'*.jpg'+'\n')
numFrames = len(imagePaths)

# Compute ssim comparisons for every frame relative to its N next frames
ssimSeq = np.zeros((numFrames, N))
for index in tqdm(range(numFrames -N-1)):
    image1 = cv.imread(imagePaths[index])
    for delay in range(N):
        image2 = cv.imread(imagePaths[index+delay+1])
        # Wang implementation
        ssimSeq[index, delay] = compare_ssim(image1, image2, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False)

        # Other implementation
        # ssimSeq[index, delay] = compare_ssim(image1, image2, multichannel=True)


ssimSeq = np.mean(ssimSeq, 0)
print("SSIM Tubo:")
print(ssimSeq)

# print("SSIM:\n{:.3f}".format(ssimSeq))


# path1 = basePath+'conf1.jpg'
# path2 = basePath+'conf2.jpg'
#
# print('\nComparing SSIM')
# print('Base image: ', path1.split(os.path.sep)[-1])
# print('')
# for path2 in imagePaths:
#     image1 = cv.imread(path1)
#     image2 = cv.imread(path2)
#
#     # print('Shape image1: ', np.shape(image1))
#
#     ssim = compare_ssim(image1, image2, multichannel=True)
#
#     print('{}\n {:.3f}\n'.format(path2.split(os.path.sep)[-1], ssim))
#
# cv.imshow('SSIM: {}'.format(ssim),image1)
# cv.waitKey(0)
# cv.imshow('SSIM: {}'.format(ssim),image2)
# cv.waitKey(0)
#
# cv.destroyAllWindows()
