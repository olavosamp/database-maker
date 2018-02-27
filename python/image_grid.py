from PIL import Image

from os import listdir
from os.path import isfile, join
import dirs

# Utility to create a grid of images sourced from dirPath.
#

dirPath = dirs.images+"20161102003730171@DVR-SPARE_Ch1"+dirs.sep    # Source folder
gridName = dirs.images+"image_grid.png"                             # Target path

K = 3 # Side of the image grid. It will contain K^2 images.

files = [ join(dirPath, f) for f in listdir(dirPath) if isfile(join(dirPath, f)) ]

sourceDim = (704, 576)   # (height, width)
destDim = (K*sourceDim[0],K*sourceDim[1])

# print(sourceDim)
# print(destDim)

new_im = Image.new('RGB', destDim)

index = 0
for i in range(0,destDim[0],sourceDim[0]):
    for j in range(0,destDim[1],sourceDim[1]):
        im = Image.open(files[index])
        im.thumbnail(sourceDim)
        new_im.paste(im, (i,j))
        index += 1


new_im.save(gridName)

print("Your image grid is ready. It is called {}".format(gridName))
