import dirs
import commons
from PIL import Image

def timeConverter( strTime ):
	# int seconds = timeConverter( string strTime )
	# Converts HHMMSS input string to integer seconds
	#
	length = len(strTime)
	if length > 6:
		seconds = 0
	else:
		h = int(strTime[0:2])
		m = int(strTime[2:4])
		s = int(strTime[4:6])

		seconds = s + m*60 + h*3600
	return seconds

def image_grid(path, targetPath="image_grid.jpg", side=6, upperCrop=0, lowerCrop=0, show=True, save=True):
    '''
        Creates a square grid of images randomly samples from available files on path.

        path:
            Target images folder path;

        targetPath:
            Path where resulting grid will be saved;

        side:
            Number of images to allocate on a grid side. Total number of images on the grid
        will be side².

        upperCrop and lowerCrop:
            Number of pixels to be cropped from each composing image. The crops executed
        are horizontal crops and are measured from top to center and bottom to center,
        respectively.
    '''


    # # Paths for a video
    # dirPath = dirs.images+"framesFull"+dirs.sep
    # gridName = dirs.images+"video_grid3x3.jpg"

    # # Paths for a dataset
    # dirPath = ".."+dirs.sep+".."+dirs.sep+"datasets"+dirs.sep+"dataset_tmax_20s_tmin_1s"+dirs.sep
    # gridName = dirs.images+"dataset_grid3x3.jpg"

    files = glob(path+'**'+dirs.sep+'*.jpg', recursive=True)

    # upperCrop = 60
    # lowerCrop = 40

    # Square Grid
    # Side of a square image grid. It will contain side^2 images.
    imageDim = (300,300)                                                # (width, height)
    destDim = (side*imageDim[0], side*(imageDim[1] - lowerCrop - upperCrop))   # (width, height)
    # shuffle(files)

    im_grid = Image.new('RGB', destDim)
    index = 0

    for j in range(0,destDim[1], imageDim[1] - lowerCrop - upperCrop):
        for i in range(0,destDim[0], imageDim[0]):
            im = Image.open(files[index])

            im = im.resize(imageDim)
            im = im.crop((0, upperCrop, imageDim[0], imageDim[1] - lowerCrop))

            im.thumbnail(imageDim)
            im_grid.paste(im, (i,j))
            index += 1

    if save is True:
        im_grid.save(targetPath)
        print("\nYour image grid is ready. It was saved at {}\n".format(targetPath))
    if show is True:
        im_grid.show()
    return 0
