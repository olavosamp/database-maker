def getFramesSSIM(videoPath, csvPath, targetPath=dirs.images+'ssim'+sep, ssim=True):
  # Read the data csv and open the video file
  print("\nUsing opencv version: ", cv2.__version__)
  print("")

  data = pd.read_csv(csvPath, dtype=str)
  video = cv2.VideoCapture(videoPath)

  ssimLim = 0.600
  frameRate = video.get(cv2.CAP_PROP_FPS)

  print("Frame rate", frameRate)

  # Interval between captured frames, in ms
  # framePeriod = (20/frameRate)*1000

  # Number of class events
  numEntries = data.loc[:,'Id'].count()

  videoName = data.loc[0,'VideoName']
  dirPath = targetPath+videoName+sep
  # dirPath = ".."+sep+"images"+sep+"{}".format(videoName)

  # Create necessary folders
  try:
  	os.makedirs(dirPath)
  except OSError:
  	pass

  try:
  	os.makedirs(dirs.images+"Totals"+sep)
  except OSError:
  	pass

  errComp 	= 1
  tuboCount	= 0
  nadaCount	= 0
  confCount	= 0
  errCount	= {'errSet': 0, 'errRead': 0, 'errWrite': 0, 'errComp': 0}
  frameCount 	= np.zeros(numEntries, dtype=np.int32)
  runTime		= np.zeros(numEntries)
  ssim 		= []
  frameCountSSIM = 0
  frameCountFull = 0
  # Get video times
  for i in range(numEntries):
  	eventStart 	= timeConverter(data.loc[i,'StartTime'])*1000
  	eventEnd   	= timeConverter(data.loc[i,'EndTime'])*1000
  	runTime[i]  = eventEnd - eventStart		# In ms

  # Number of frames in video (aprox)
  maxFrames = np.sum(runTime)*frameRate
  #maxFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)

  ## Frame capture operations
  for i in range(numEntries):
  	ID 			= int(data.loc[i,'Id'])
  	eventStart 	= timeConverter(data.loc[i,'StartTime'])*1000
  	eventEnd   	= timeConverter(data.loc[i,'EndTime'])*1000
  	frameClass 	= data.loc[i,'Class']

  	# Use minimum frame period
  	framePeriod = 1/frameRate*1000

  	# Start new entry
  	print("\nID{:2d} framePeriod {:.3f}".format(ID, framePeriod))
  	frameTime = eventStart

  	# Read and save first frame
  	errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
  	errRead, image1 = video.read()
  	frameTime = frameTime + framePeriod
  	# Write frame to file
  	if errRead and errSet:
  		imgPath = "{}{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
  		errWrite = cv2.imwrite(imgPath, image1)

  	# Process next frames
  	while(frameTime <= eventEnd):
  		# Set video time and read next frame
  		errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
  		errRead, image2 = video.read()

  		# Compute frame similarity
  		try:
  			ssimFrame = compare_ssim(image1, image2, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False)
  		except OSError:
  			errComp = 0

  		print("ID{:2d} Frame {:4d} Comparison No {:4d} SSIM {:.3f}".format(ID, frameCountFull, frameCountSSIM, ssimFrame))
  		frameCountSSIM += 1
  		frameCountFull += 1

  		# Only save frame if it is dissimilar enough from last saved frame
  		if ssimFrame < ssimLim:
  			# Image path
  			imgPath = "{}{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
  			# print("\n", imgPath)

  			print("\nFrame captured.\n")
  			frameCountSSIM = 0
  			# Compare next frames against the last one saved
  			image1 = image2

  			if errRead and errSet:
  				# Write frame to file
  				errWrite = cv2.imwrite(imgPath, image2)

  				# Count class occurrences
  				if frameClass == 'tubo':
  					tuboCount = tuboCount + 1
  				elif frameClass == 'nada':
  					nadaCount = nadaCount + 1
  				elif frameClass == 'conf':
  					confCount = confCount + 1

  				frameCount[i] = frameCount[i] + 1
  				ssim.append(ssimFrame)	# Record dataset ssim

  		# Error handling
  		if not(errWrite) or not(errRead) or not(errSet) or not(errComp):
  			print("\n!!! Error!!! ")
  			print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
  			print("errWrite: {}\nerrRead: {}\nerrSet: {}\nerrComp: {}".format(errWrite, errRead, errSet, errComp))

  		errCount['errWrite'] += (not(errWrite))
  		errCount['errSet']   += (not(errSet))
  		errCount['errRead']  += (not(errRead))
  		errCount['errComp']  += (not(errComp))

  		# Advance time one framePeriod
  		frameTime = frameTime + framePeriod

  	print("ID{}: {} frames".format(ID, frameCount[i]))
  	frameTotal = np.sum(frameCount)

  ## Information
  print('\nErrors during extraction:')
  print(errCount)
  # print("errWrite", errWrite)
  # print("errRead", errRead)
  # print("errSet", errSet)

  print("\nFrame rate: {:.2f}".format( frameRate))
  print("Total frames (csv): {:.2f}".format( maxFrames/1000))
  print("Total frames (video): {:.2f}".format( video.get(cv2.CAP_PROP_FRAME_COUNT)))
  print("Total frames acquired: ", frameTotal)
  print("   Tubo: ", tuboCount)
  print("   Nada: ", nadaCount)
  print("   Conf: ", confCount)

  # Save frame totals
  logPath = dirs.csv+"Totals"+sep+"{}.tot".format(videoName)
  file = open(logPath, 'w')
  file.writelines(["Tubo,Nada,Conf,Total,SSIM\n", "{},{},{},{},{}".format(tuboCount, nadaCount, confCount, frameTotal, np.mean(np.mean(ssim)))])
  file.close()

  runTime = np.divide(runTime, 1000)
  print("\nRun time: {} seconds (for contiguous classification, should be the same as video run time)".format(np.sum(runTime)))
  print("   Mean: {:.2f}".format( np.mean(runTime)))
  print("   Std: {:.2f}".format( np.std(runTime)))

  print("\nTotals saved at {}".format(logPath))

  video.release()
  return frameTotal
