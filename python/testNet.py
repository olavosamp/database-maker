# import os

# import pandas 			as pd
import numpy 				as np
# import scipy.misc   		as spm
# import mtplotlib.pyplot		as plt

from countClasses import countClasses

import cv2

rootPath = "..\\images"

tuboPath, nadaPath, confPath = countClasses(rootPath)

K = 3	# 0 | [1 0 0] is tubo
		# 1 | [0 1 0] is nada
		# 2 | [0 0 1] is conf

tuboFile = open(tuboPath, 'r')
nadaFile = open(nadaPath, 'r')
confFile = open(confPath, 'r')

tuboList = tuboFile.readlines()
nadaList = nadaFile.readlines()
confList = confFile.readlines()

# Compose data and labels

# print("\ntuboList shape: ", np.shape(tuboList))

# tuboLen = 0
# x = [tuboFile.readline()]
# for line in tuboFile:
# 	# print(x)
# 	# print(line)
# 	# print(np.shape(x))
# 	# print(np.shape(line))

# 	# x.append(line)
# 	x = np.append(x, [line], axis=0)
# 	tuboLen = tuboLen + 1

xAux = np.array(tuboList, dtype="str")
y = np.tile([1, 0, 0], (len(tuboList), 1))

xAux = np.append(xAux, nadaList, axis=0)
y = np.append(y, np.tile([0, 1, 0], (len(nadaList), 1)), axis=0)

xAux = np.append(xAux, confList, axis=0)
y = np.append(y, np.tile([0, 0, 1], (len(confList), 1)), axis=0)

# print("\nxAux: \n", xAux)
print("\nxAux shape: ", np.shape(xAux))
x = xAux
# x = spm.imread("..\\images\\GHmls16-263_OK\\DVD-1\\20161101202838328@DVR-SPARE_Ch1.wmv\\20161101202838328@DVR-SPARE_Ch1.wmv ID1 FRAME0 tubo.jpg")
# img = plt.imshow(x)
# # x = list(map(lambda x: cv2.imread(x), xAux))
# print("")
# print("x: \n", xAux[2])
print("y: \n", y)
# print("\nx shape: ", np.shape(x))
print("y shape: ", np.shape(y))

tuboFile.close()
nadaFile.close()
confFile.close()

im = cv2.imread("..\\images\\GHmls16-263_OK\\DVD-1\\20161101202838328@DVR-SPARE_Ch1.wmv\\20161101202838328@DVR-SPARE_Ch1.wmv ID1 FRAME0 tubo.jpg")
# im = cv2.imread(x[1])
cv2.imshow('image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(im)
print(np.shape(im))
