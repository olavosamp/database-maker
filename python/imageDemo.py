import os
import cv2
import numpy 				as np
import glob

import dirs
import commons
import count

N = 10	# 6 demo images per class

targetPath = dirs.images

# tuboFile = open(tuboPath, 'r')
# nadaFile = open(nadaPath, 'r')
# confFile = open(confPath, 'r')

# tuboList = tuboFile.readlines()[1:]
# nadaList = nadaFile.readlines()[1:]
# confList = confFile.readlines()[1:]

# Get list of image paths and corresponding labels
imageList, labels = count.listImages(targetPath)

tuboList = np.extract(np.equal(labels, commons.tuboCode), imageList)
nadaList = np.extract(np.equal(labels, commons.nadaCode), imageList)
confList = np.extract(np.equal(labels, commons.confCode), imageList)

# print(imageList)
print(tuboList)
print(nadaList)
print(confList)

# Create demo directory
try:
	os.makedirs(dirs.demo)
except OSError:
	print()

# Save N randomly selected images of each class to demo directory
print("")
for pathList in [tuboList, nadaList, confList]:
	sample = np.random.permutation(pathList)[:N]
	for path in sample:
		name = path.split("\\")[-1]
		writePath = dirs.demo+name.rstrip()
		# print(path.split("\\")[-1])
		# print(path)
		print("Writing to ", writePath)
		image = cv2.imread(path.rstrip())
		writeError = cv2.imwrite(writePath, image)
		if not(writeError):
			print("Write Error")
		# cv2.imshow('image sample', image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

# tuboFile.close()
# nadaFile.close()
# confFile.close()

# print("")
# # im = cv2.imread(r"..\images\GHmls16-263_OK\DVD-1\20161101225102250@DVR-SPARE_Ch1.wmv\20161101225102250@DVR-SPARE_Ch1.wmv ID1 FRAME52 tubo.jpg")
# # path = tuboList[0].rstrip()
# path = "..\\images\\GHmls16-263_OK\\DVD-1\\20161101225102250@DVR-SPARE_Ch1.wmv\\20161101225102250@DVR-SPARE_Ch1.wmv ID1 FRAME52 tubo.jpg"
# print(path)
# # print(tuboList[0].rstrip())
# # print(tuboList[0])
# # print(str(tuboList[0]))
# im = cv2.imread(path)
#
# cv2.imshow('image', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# writePath = "..\\demo\\20161101225102250@DVR-SPARE_Ch1.wmv ID1 FRAME52 tubo.jpg"
# writeError = cv2.imwrite(writePath, image)
# print(writeError)
# #
# # print("Read image:\n")
# print(im)
# print("\nim shape: ", np.shape(im))
