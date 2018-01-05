from skimage.measure import compare_ssim
import cv2      as cv
import numpy    as np
import glob
import os

import dirs
import count

basePath = '..\\..\\testfolder\\20161101222101578@DVR-SPARE_Ch1.wmv\\'

# imagePaths = glob.glob(basePath+'*.jpg')

path1 = basePath+'20161101222101578@DVR-SPARE_Ch1.wmv ID1 FRAME0 tubo.jpg'
path2 = basePath+'20161101222101578@DVR-SPARE_Ch1.wmv ID1 FRAME5 tubo.jpg'

print('\nComparing SSIM')
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

image1 = cv.imread(path1)
image2 = cv.imread(path2)

# print('Shape image1: ', np.shape(image1))

ssim = compare_ssim(image1, image2, multichannel=True)

print('{}\n {:.3f}\n'.format(path2.split(os.path.sep)[-1], ssim))

# cv.imshow('SSIM: {}'.format(ssim),image1)
# cv.waitKey(0)
# cv.imshow('SSIM: {}'.format(ssim),image2)
# cv.waitKey(0)
#
# cv.destroyAllWindows()
