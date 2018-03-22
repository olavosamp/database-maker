from PIL import Image
from os import listdir
from os.path import isfile, join
from glob import glob
from random import shuffle

import dirs


# Utility to create a grid of images sourced from dirPath.
#

# Paths for a video
dirPath = dirs.images+"framesFull"+dirs.sep
gridName = dirs.images+"video_grid3x3.jpg"

# # Paths for a dataset
# dirPath = ".."+dirs.sep+".."+dirs.sep+"datasets"+dirs.sep+"dataset_tmax_20s_tmin_1s"+dirs.sep
# gridName = dirs.images+"dataset_grid3x3.jpg"

# # Paths for class examples
# dirPath =   dirs.images+"classExamples"+dirs.sep+"nada"+dirs.sep
# gridName = dirs.images+"classExamples"+dirs.sep+"nada_grid.jpg"


# files = [ join(dirPath, f) for f in listdir(dirPath) if isfile(join(dirPath, f)) ]
files = glob(dirPath+'**'+dirs.sep+'*.jpg', recursive=True)

upperCrop = 60
lowerCrop = 40

# Square Grid
K = 3                                     # Side of a square image grid. It will contain K^2 images.
imageDim = (300,300)                                                # (width, height)
destDim = (K*imageDim[0],K*(imageDim[1] - lowerCrop - upperCrop))   # (width, height)
# shuffle(files)

# # Rectangular grid
# K = len(files)                          # Length of the rectangle. I will contain K images.
# imageDim = (300,300)                    # (width, height)
# destDim = (K*imageDim[0],imageDim[1])   # (width, height)

# images = list(map(lambda x: Image.open(x).resize(imageDim), files))   # only first K^2 images ares used, stupid

new_im = Image.new('RGB', destDim)

index = 0

for j in range(0,destDim[1], imageDim[1] - lowerCrop - upperCrop):
    for i in range(0,destDim[0], imageDim[0]):
        im = Image.open(files[index])

        im = im.resize(imageDim)
        im = im.crop((0, upperCrop, imageDim[0], imageDim[1] - lowerCrop))

        im.thumbnail(imageDim)
        new_im.paste(im, (i,j))
        index += 1

new_im.save(gridName)

print("\nYour image grid is ready. It is called {}\n".format(gridName))
