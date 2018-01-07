from skimage.measure import compare_ssim
import cv2      as cv
import numpy    as np
import glob
import os

import dirs
import count

basePath = '..\\..\\testfolder\\'

imagePaths = glob.glob(basePath+'*.jpg')

path1 = basePath+'20161101205058500@DVR-SPARE_Ch1.wmv ID1 FRAME122 conf.jpg'
# path2 = basePath+'20161101205058500@DVR-SPARE_Ch1.wmv ID1 FRAME123 conf.jpg'

print('\nComparing SSIM')
print('Base image: ', path1.split(os.path.sep)[-1])
print('')
for path2 in imagePaths:
    image1 = cv.imread(path1)
    image2 = cv.imread(path2)

    ssim = compare_ssim(image1, image2, multichannel=True)

    print('{}\n {:.3f}\n'.format(path2.split(os.path.sep)[-1], ssim))


print('{}'.format(path1.split(os.path.sep)[-1]))
print('{}'.format(path2.split(os.path.sep)[-1]))
print('{:.3f}'.format(ssim))

# cv.imshow('SSIM: {}'.format(ssim),image1)
# cv.waitKey(0)
# cv.imshow('SSIM: {}'.format(ssim),image2)
# cv.waitKey(0)
#
# cv.destroyAllWindows()
