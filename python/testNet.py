import os
# import pandas 		as pd
import numpy 		as np
import cv2

# from keras.applications.inception_v3 import InceptionV3
# # from keras.preprocessing import image
# from keras.models import Model
# from keras.layers import Dense, GlobalAveragePooling2D
# from keras import backend

from countClasses import countClasses

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

print("xAux: \n", xAux)
print("\nxAux shape: ", np.shape(xAux))

x = map(lambda x: cv2.imread(x), xAux)

print("")
print("x: \n", x)
print("y: \n", y)
print("\nx shape: ", np.shape(x))
print("y shape: ", np.shape(y))

# tuboFile.close()
# nadaFile.close()
# confFile.close()

# im = cv2.imread("..\\images\\GHmls16-263_OK\\DVD-1\\20161101202838328@DVR-SPARE_Ch1.wmv\\20161101202838328@DVR-SPARE_Ch1.wmv ID1 FRAME0 tubo.jpg")
# im = cv2.imread(x[0])
# cv2.imshow('image', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(im)
# print(np.shape(im))

# # create the base pre-trained model
# base_model = InceptionV3(weights='imagenet', include_top=False)

# # add a global spatial average pooling layer
# x = base_model.output
# # x = GlobalAveragePooling2D()(x)
# # let's add a fully-connected layer
# x = Dense(1024, activation='relu')(x)
# # and a logistic layer -- let's say we have 200 classes
# predictions = Dense(backend, activation='softmax')(x)

# # this is the model we will train
# model = Model(inputs=base_model.input, outputs=predictions)

# # first: train only the top layers (which were randomly initialized)
# # i.e. freeze all convolutional InceptionV3 layers
# # for layer in base_model.layers:
# #     layer.trainable = False

# # compile the model (should be done *after* setting layers to non-trainable)
# model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

# # train the model on the new data for a few epochs
# hist = model.fit(x, y)
# # model.fit_generator(...)

# # at this point, the top layers are well trained and we can start fine-tuning
# # convolutional layers from inception V3. We will freeze the bottom N layers
# # and train the remaining top layers.

# # let's visualize layer names and layer indices to see how many layers
# # we should freeze:
# for i, layer in enumerate(base_model.layers):
#    print(i, layer.name)

# print(hist)
# print(hist.History)
# # we chose to train the top 2 inception blocks, i.e. we will freeze
# # the first 249 layers and unfreeze the rest:
# # for layer in model.layers[:249]:
# #    layer.trainable = False
# # for layer in model.layers[249:]:
# #    layer.trainable = True

# # # we need to recompile the model for these modifications to take effect
# # # we use SGD with a low learning rate
# # from keras.optimizers import SGD
# # model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# # # we train our model again (this time fine-tuning the top 2 inception blocks
# # # alongside the top Dense layers
# # model.fit_generator(...)