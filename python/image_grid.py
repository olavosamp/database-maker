from PIL import Image
from os import listdir
from os.path import isfile, join
from glob import glob
from random import shuffle

import dirs


# Utility to create a grid of images sourced from dirPath.
#

# Paths for a video
# dirPath = dirs.images+"framesFull"+dirs.sep+"20161101215100437@DVR-SPARE_Ch1.wmv"+dirs.sep
# gridName = dirs.images+"video_grid3x3.png"

# Paths for a dataset
dirPath = ".."+dirs.sep+".."+dirs.sep+"datasets"+dirs.sep+"dataset_tmax_20s_tmin_1s"+dirs.sep
gridName = dirs.images+"dataset_grid3x3.jpg"


K = 3 # Side of the image grid. It will contain K^2 images.

# files = [ join(dirPath, f) for f in listdir(dirPath) if isfile(join(dirPath, f)) ]
files = glob(dirPath+'**'+dirs.sep+'*.jpg', recursive=True)
shuffle(files)

sourceDim = (704, 576)   # (height, width)
destDim = (K*sourceDim[0],K*sourceDim[1])


new_im = Image.new('RGB', destDim)

index = 0
for j in range(0,destDim[1],sourceDim[1]):
    for i in range(0,destDim[0],sourceDim[0]):
        im = Image.open(files[index])
        im.thumbnail(sourceDim)
        new_im.paste(im, (i,j))
        index += 1


new_im.save(gridName)

print("\nYour image grid is ready. It is called {}\n".format(gridName))
