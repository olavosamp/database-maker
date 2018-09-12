import dirs
from utils import image_grid


# # Paths for a video
# dirPath = dirs.images+"framesFull"+dirs.sep
# gridName = dirs.images+"video_grid3x3.jpg"

# Paths for a dataset
# dirPath = ".."+dirs.sep+".."+dirs.sep+"datasets"+dirs.sep+"dataset_tmax_20s_tmin_1s"+dirs.sep
dirPath = "../../datasets/dataset_handpicked/"
gridName = dirs.images+"dataset_grid3x3.jpg"

# upperCrop = 60
# lowerCrop = 40

image_grid(dirPath, targetPath=gridName)
