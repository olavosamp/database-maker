import cv2
import numpy 				as np
from countClasses import countClasses
import dirs

tuboPath, nadaPath, confPath = countClasses(dirs.images)
print("")

N = 6	# 6 demo images per class

tuboFile = open(tuboPath, 'r')
nadaFile = open(nadaPath, 'r')
confFile = open(confPath, 'r')

tuboList = tuboFile.readlines()[1:]
nadaList = nadaFile.readlines()[1:]
confList = confFile.readlines()[1:]
# tuboList = tuboList[1:]
# nadaList = nadaList[1:]
# confList = confList[1:]

# print("\ntuboList shape: ", np.shape(tuboList))

# Tubo demo images
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

tuboFile.close()
nadaFile.close()
confFile.close()

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