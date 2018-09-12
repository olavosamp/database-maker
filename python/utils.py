import os
import math
import numpy 	as np
from PIL 		import Image
from glob 		import glob
from tqdm		import tqdm

import dirs
import commons

def get_perfect_square(number, round='down'):
	if round == 'down':
		return int(math.sqrt(number))**2
	else:
		return round(math.sqrt(number))**2

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
	files = glob(path+'**'+dirs.sep+'*.jpg', recursive=True)
	numImages 		= len(files)
	squareNumImages = get_perfect_square(numImages)

	files = np.random.choice(files, size=squareNumImages, replace=False)

	# Square Grid
	# Side of a square image grid. It will contain side^2 images.
	side = int(math.sqrt(numImages))
	imageDim = (300,300)   	   # (width, height)
	# imageDim = (100,100)
	destDim = (side*imageDim[0], side*(imageDim[1] - lowerCrop - upperCrop))

	im_grid = Image.new('RGB', destDim)
	index = 0
	for j in tqdm(range(0, destDim[1], imageDim[1] - lowerCrop - upperCrop)):
		for i in range(0,destDim[0], imageDim[0]):
			im = Image.open(files[index])

			im = im.resize(imageDim)
			im = im.crop((0, upperCrop, imageDim[0], imageDim[1] - lowerCrop))

			im.thumbnail(imageDim)
			im_grid.paste(im, (i,j))
			index += 1

	if save is True:
		dirPath = dirs.sep.join(targetPath.split(dirs.sep)[:-1])

		try:
			os.makedirs(dirPath)
		except OSError:
			pass

		im_grid.save(targetPath)
		print("\nYour image grid is ready. It was saved at {}\n".format(targetPath))
	if show is True:
	    im_grid.show()
	return 0
