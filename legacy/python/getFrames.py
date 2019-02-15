import os
import cv2
import numpy             as np
import pandas             as pd
from   tqdm             import tqdm
from   collections         import Counter
# from   skimage.measure     import compare_ssim

import commons
import dirs
from   dirs                import sep
from   utils             import timeConverter

def get_frames_small(videoPath, interval=5, destFolder="./images/", verbose=False):
    '''
        Function to capture frames from videos.
        Please use getFrames instead for large scale systematic frame extraction.
        Arguments:
            videoPath:  Video source path.
            interval:   Frame capture period in seconds.
            destFolder: Base destination folder.
            verbose:    Set True to print progress and results.

        Returns
            frameCount: Number of captured frames.
    '''

    videoName   = videoPath.split("/")[-1]

    # Get destination folder
    videoFolder = videoPath.split("20170724_FTP83G_Petrobras/")[-1]
    destFolder  = destFolder+"/".join(videoFolder.split("/")[:-1])+"/"

    try:
        os.makedirs(destFolder)
    except OSError:
        # Folder already exists or destFolder is invalid
        pass

    video = cv.VideoCapture(videoPath)

    frameRate        = video.get(cv.CAP_PROP_FPS)
    videoTotalFrames = video.get(cv.CAP_PROP_FRAME_COUNT)

    # Get video runtime
    videoRuntime = (videoTotalFrames - 1)/frameRate

    # Limit capture rate to frame rate
    if (1/interval) > frameRate:
        interval = 1/frameRate

    # List of frame times, in ms
    captureTimes = np.arange(np.ceil(videoRuntime/interval))*interval*1000
    captureTimes[-1] = videoRuntime

    frameCount = 0
    if verbose is True:
        from tqdm import tqdm

        print("\nFrame Rate:     ", frameRate)
        print("Runtime:        ", videoRuntime)
        print("Interval:       ", interval, "\n")

        for frameTime in tqdm(captureTimes):
            # Set video time
            errSet = video.set(cv.CAP_PROP_POS_MSEC, frameTime)

            # Read frame at set time
            errRead, frame = video.read()
            frameCount +=1

            # Write frame as jpg
            imgPath = destFolder+"{} {}.jpg".format(videoName, frameCount)
            errWrite = cv.imwrite(imgPath, frame)

        print("\nCaptured {} frames.".format(frameCount))
        print("\nSaved {} frames at {}".format(frameCount, destFolder))

    else:
        for frameTime in captureTimes:
            # Set video time
            errSet = video.set(cv.CAP_PROP_POS_MSEC, frameTime)

            # Read frame at set time
            errRead, frame = video.read()
            frameCount +=1

            # Write frame as jpg
            imgPath = destFolder+"{} {}.jpg".format(videoName, frameCount)
            errWrite = cv.imwrite(imgPath, frame)

    return frameCount


def getFrames(videoPath, data, targetPath=dirs.images, ssim=True):
    '''
        Main frame capture routine
    '''
    # videoPath = ".."+sep+".."+sep+".."+sep+"20170724_FTP83G_Petrobras"+sep+"CIMRL10-676_OK"+sep+"PIDF-1 PO MRL-021_parte2.mpg"
    # csvPath = ".."+sep+".."+sep+"csv"+sep+"PIDF-1 PO MRL-021_parte2.csv"

    # Read the data csv and open the video file
    print("\nUsing opencv version: ", cv2.__version__)
    print("")

    # print("\nReference csv:{}".format(data))

    # data = pd.read_csv(csvPath, dtype=str)
    video = cv2.VideoCapture(videoPath)
    frameRate = video.get(cv2.CAP_PROP_FPS)
    # print("Frame rate", frameRate)

    # Using fixed frame period
    # Interval between captured frames, in ms
    # framePeriod = (20/frameRate)*1000

    # Number of class events
    numEntries = data.loc[:,'Id'].count()

    # folderName = csvPath.split(dirs.sep)[-1][:-4]
    folderName = data.loc[0]["VideoName"]
    dirPath = targetPath+folderName+sep

    # Create output folder
    try:
        os.makedirs(dirPath)
    except OSError:
        # print("Directory already exists or invalid path")
        # print(OSError)
        # print()
        pass
    try:
        os.makedirs(dirs.totals)
    except OSError:
        # print()
        pass

    tuboCount = 0
    nadaCount = 0
    confCount = 0
    errWrite  = True
    errRead   = True
    errSet    = True
    errCount = {'errSet': 0, 'errRead': 0, 'errWrite': 0}
    runTime = np.zeros(numEntries)
    idList = []
    ## Perform frame capture operations
    for i in range(numEntries):
        eventStart     = timeConverter(data.loc[i,'StartTime'])*1000
        eventEnd       = timeConverter(data.loc[i,'EndTime'])*1000
        runTime[i]  = eventEnd - eventStart        # In ms
        idList.append(int(data.loc[i,'Id']))

    # Number of frames in video (aprox)
    maxFrames = np.sum(runTime)*frameRate
    #maxFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # List of unique IDs
    idCounter = Counter(idList)
    numIds = len(list(idCounter))
    frameCount = dict(zip(idCounter, np.zeros(numIds, dtype=np.int32)))

    for i in range(numEntries):
        ID             = int(data.loc[i,'Id'])
        eventStart     = timeConverter(data.loc[i,'StartTime'])*1000
        eventEnd       = timeConverter(data.loc[i,'EndTime'])*1000
        videoName      = data.loc[i,'VideoName']

        tags    = data.loc[i, 'Tags']
        tagList = tags.split('-')
        if commons.skipTag in tagList:
            # Skip csv entry if it contains a skip tag
            continue

        if len(videoName.split(dirs.sep) ) > 1:
            videoName = videoName.replace(dirs.sep, '--')

        # Check for matching classes
        frameClass     = data.loc[i,'Class']
        if frameClass not in commons.classes:
            print("\n!!! Error!!! ")
            print("Video: {}\nID{:2d}\n Class {} does not match any class codes.\n".format(videoName, ID, frameClass))

            i += 1        # Fails if this is already the last entry in the csv
            continue      # Returns to the beginning of the iteration

        # Find frame period
        framePeriod = 20*(runTime[i]*numEntries/maxFrames)*1000
        # Limit frame period
        # tMax = 20000                    # 20 seconds
        # tMin = (20/frameRate)*1000    # 0.66 seconds for 30 frames/s
        #                                 # 0.8 seconds for 25 frames/s

        tMax = 20000                    # 20 seconds
        tMin = (30/frameRate)*1000        # 1 seconds for 30 frames/s
                                        # 1.2 seconds for 25 frames/s
        # Limit framePeriod
        if framePeriod > tMax:
            framePeriod = tMax
        if framePeriod < tMin:
            framePeriod = tMin

        print("\nID{:2d} framePeriod {:.3f}".format(ID, framePeriod))
        frameTime = eventStart
        while(frameTime < eventEnd):
            # Set video time and read next frame
            errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
            errRead, frame = video.read()

            # print("\n", imgPath)
            # print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))

            if errRead and errSet:
                frameCount[ID] += 1
                # Saved image name/path
                imgPath = "{}{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[ID], frameClass)

                # Write frame to file
                errWrite = cv2.imwrite(imgPath, frame)

                # Count class occurrences
                if frameClass == 'tubo':
                    tuboCount = tuboCount + 1
                elif frameClass == 'nada':
                    nadaCount = nadaCount + 1
                elif frameClass == 'conf':
                    confCount = confCount + 1

            # Error handling
            if not(errWrite) or not(errRead) or not(errSet):
                print("\n!!! Error!!! ")
                print("ID{:2d} Frame {:3d}".format(ID, frameCount[ID]))
                print("errWrite: {}\nerrRead: {}\nerrSet: {}".format(errWrite, errRead, errSet))

            errCount['errWrite'] += (not(errWrite))
            errCount['errSet']   += (not(errSet))
            errCount['errRead']  += (not(errRead))

            # Advance time one framePeriod
            frameTime += framePeriod

        print("ID{}: {} frames".format(ID, frameCount[ID]))
        frameTotal = sum(frameCount.values())

    ## Information
    print('\nErrors during extraction:')
    print(errCount)
    # print("errWrite", errWrite)
    # print("errRead", errRead)
    # print("errSet", errSet)

    print("\nFrame rate: {:.2f} frames/s".format( frameRate))
    print("Parameters:\n\tTmin: {:2.2f}\tseconds\n\tTmax: {:2.2f}\tseconds\n".format(tMin/1000, tMax/1000))
    # print("Total frames (csv): {:.2f}".format( maxFrames/1000))
    # print("Total frames (video): {:.2f}".format( video.get(cv2.CAP_PROP_FRAME_COUNT)))
    print("Total frames acquired: ", frameTotal)
    # print("\tTubo: {:4d}".format(tuboCount))
    # print("\tNada: {:4d}".format(nadaCount))
    # print("\tConf: {:4d}".format(confCount))

    # Save frame totals
    logPath = dirs.totals+"{}.tot".format(videoName)
    file = open(logPath, 'w')
    file.writelines(["Tubo,Nada,Conf,Total\n", "{},{},{},{}".format(tuboCount, nadaCount, confCount, frameTotal)])
    file.close()

    runTime = np.divide(runTime, 1000)
    # print("\nRun time: {} seconds (for contiguous classification, should be the same as video run time)".format(np.sum(runTime)))
    # print("\tMean: {:.2f}".format( np.mean(runTime)))
    # print("\tStd:  {:.2f}".format( np.std(runTime)))

    print("\nTotals saved at {}".format(logPath))

    video.release()
    return frameTotal

def getFramesFull(videoPath, csvPath, targetPath=dirs.images+'full'+sep, ssim=True):
    # videoPath = "F:"+sep+"Program Files"+sep+"Arquivos Incomuns"+sep+"Relevante"+sep+"UFRJ"+sep+"Projeto Final"+sep+"DadosPetrobras"+sep+"20170724_FTP83G_Petrobras"+sep+"CIMRL10-676_OK"+sep+"PIDF-1 PO MRL-021_parte2.mpg"
    # csvPath = ".."+sep+"csv"+sep+"PIDF-1 PO MRL-021_parte2.csv"

    # Read the data csv and open the video file
    print("\nUsing opencv version: ", cv2.__version__)
    print("")

    data = pd.read_csv(csvPath, dtype=str)
    video = cv2.VideoCapture(videoPath)

    frameRate = video.get(cv2.CAP_PROP_FPS)

    print("Frame rate", frameRate)

    # Interval between captured frames, in ms
    # framePeriod = (20/frameRate)*1000

    # Number of class events
    numEntries = data.loc[:,'Id'].count()

    videoName = "testVideo1"
    videoName = data.loc[0,'VideoName']
    dirPath = targetPath+videoName+sep
    # dirPath = ".."+sep+"images"+sep+"{}".format(videoName)

    # Create output folder
    try:
        os.makedirs(dirPath)
    except OSError:
        # print("Directory already exists or invalid path")
        # print(OSError)
        # print()
        pass
    try:
        os.makedirs(dirs.images+"Totals"+sep)
    except OSError:
        # print()
        pass

    tuboCount  = 0
    nadaCount  = 0
    confCount  = 0
    errCount = {'errSet': 0, 'errRead': 0, 'errWrite': 0}
    frameCount = np.zeros(numEntries, dtype=np.int32)
    runTime = np.zeros(numEntries)

    ## Perform frame capture operations
    for i in range(numEntries):
        eventStart     = timeConverter(data.loc[i,'StartTime'])*1000
        eventEnd       = timeConverter(data.loc[i,'EndTime'])*1000
        runTime[i]  = eventEnd - eventStart        # In ms

    # Number of frames in video (aprox)
    maxFrames = np.sum(runTime)*frameRate
    #maxFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    K = 20
    for i in range(numEntries):
        ID             = int(data.loc[i,'Id'])
        eventStart     = timeConverter(data.loc[i,'StartTime'])*1000
        eventEnd       = timeConverter(data.loc[i,'EndTime'])*1000
        frameClass     = data.loc[i,'Class']

        # Use minimum frame period
        framePeriod = 1/frameRate*1000

        # Use fixed frame period
        framePeriod = K/frameRate*1000


        # # Find frame period
        # framePeriod = 20*(runTime[i]*numEntries/maxFrames)*1000
        # # Limit frame period
        # tMax = 5000                    # 5 seconds
        # tMin = (10/frameRate)*1000    # 0.5 seconds
        # if framePeriod > tMax:
        #     framePeriod = tMax
        # if framePeriod < tMin:
        #     framePeriod = tMin

        print("\nID{:2d} framePeriod {:.3f}".format(ID, framePeriod))
        frameTime = eventStart
        while(frameTime < eventEnd):
            # Set video time and read next frame
            errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
            errRead, frame = video.read()

            # Saved image name/path
            imgPath = "{}{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
            # print("\n", imgPath)
            print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))

            if errRead and errSet:
                # Write frame to file
                errWrite = cv2.imwrite(imgPath, frame)

                # Count class occurrences
                if frameClass == 'tubo':
                    tuboCount = tuboCount + 1
                elif frameClass == 'nada':
                    nadaCount = nadaCount + 1
                elif frameClass == 'conf':
                    confCount = confCount + 1

            # Error handling
            if not(errWrite) or not(errRead) or not(errSet):
                print("\n!!! Error!!! ")
                print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
                print("errWrite: {}\nerrRead: {}\nerrSet: {}".format(errWrite, errRead, errSet))

            errCount['errWrite'] = errCount['errWrite'] + (not(errWrite))
            errCount['errSet']   = errCount['errSet']   + (not(errSet))
            errCount['errRead']  = errCount['errRead']  + (not(errRead))

            # Advance time one framePeriod
            frameTime = frameTime + framePeriod
            frameCount[i] = frameCount[i] + 1


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
    file.writelines(["Tubo,Nada,Conf,Total\n", "{},{},{},{}".format(tuboCount, nadaCount, confCount, frameTotal)])
    file.close()

    runTime = np.divide(runTime, 1000)
    print("\nRun time: {} seconds (for contiguous classification, should be the same as video run time)".format(np.sum(runTime)))
    print("   Mean: {:.2f}".format( np.mean(runTime)))
    print("   Std: {:.2f}".format( np.std(runTime)))

    print("\nTotals saved at {}".format(logPath))

    video.release()
    return frameTotal

 # def getFramesSSIM(videoPath, csvPath, targetPath=dirs.images+'ssim'+sep, ssim=True):
    # # Read the data csv and open the video file
    # print("\nUsing opencv version: ", cv2.__version__)
    # print("")
 #
    # data = pd.read_csv(csvPath, dtype=str)
    # video = cv2.VideoCapture(videoPath)
 #
    # ssimLim = 0.600
    # frameRate = video.get(cv2.CAP_PROP_FPS)
 #
    # print("Frame rate", frameRate)
 #
    # # Interval between captured frames, in ms
    # # framePeriod = (20/frameRate)*1000
 #
    # # Number of class events
    # numEntries = data.loc[:,'Id'].count()
 #
    # videoName = data.loc[0,'VideoName']
    # dirPath = targetPath+videoName+sep
    # # dirPath = ".."+sep+"images"+sep+"{}".format(videoName)
 #
    # # Create necessary folders
    # try:
    #     os.makedirs(dirPath)
    # except OSError:
    #     pass
 #
    # try:
    #     os.makedirs(dirs.images+"Totals"+sep)
    # except OSError:
    #     pass
 #
    # errComp     = 1
    # tuboCount    = 0
    # nadaCount    = 0
    # confCount    = 0
    # errCount    = {'errSet': 0, 'errRead': 0, 'errWrite': 0, 'errComp': 0}
    # frameCount     = np.zeros(numEntries, dtype=np.int32)
    # runTime        = np.zeros(numEntries)
    # ssim         = []
    # frameCountSSIM = 0
    # frameCountFull = 0
    # # Get video times
    # for i in range(numEntries):
    #     eventStart     = timeConverter(data.loc[i,'StartTime'])*1000
    #     eventEnd       = timeConverter(data.loc[i,'EndTime'])*1000
    #     runTime[i]  = eventEnd - eventStart        # In ms
 #
    # # Number of frames in video (aprox)
    # maxFrames = np.sum(runTime)*frameRate
    # #maxFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
 #
    # ## Frame capture operations
    # for i in range(numEntries):
    #     ID             = int(data.loc[i,'Id'])
    #     eventStart     = timeConverter(data.loc[i,'StartTime'])*1000
    #     eventEnd       = timeConverter(data.loc[i,'EndTime'])*1000
    #     frameClass     = data.loc[i,'Class']
 #
    #     # Use minimum frame period
    #     framePeriod = 1/frameRate*1000
 #
    #     # Start new entry
    #     print("\nID{:2d} framePeriod {:.3f}".format(ID, framePeriod))
    #     frameTime = eventStart
 #
    #     # Read and save first frame
    #     errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
    #     errRead, image1 = video.read()
    #     frameTime = frameTime + framePeriod
    #     # Write frame to file
    #     if errRead and errSet:
    #         imgPath = "{}{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
    #         errWrite = cv2.imwrite(imgPath, image1)
 #
    #     # Process next frames
    #     while(frameTime <= eventEnd):
    #         # Set video time and read next frame
    #         errSet = video.set(cv2.CAP_PROP_POS_MSEC, frameTime)
    #         errRead, image2 = video.read()
 #
    #         # Compute frame similarity
    #         try:
    #             ssimFrame = compare_ssim(image1, image2, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False)
    #         except OSError:
    #             errComp = 0
 #
    #         print("ID{:2d} Frame {:4d} Comparison No {:4d} SSIM {:.3f}".format(ID, frameCountFull, frameCountSSIM, ssimFrame))
    #         frameCountSSIM += 1
    #         frameCountFull += 1
 #
    #         # Only save frame if it is dissimilar enough from last saved frame
    #         if ssimFrame < ssimLim:
    #             # Image path
    #             imgPath = "{}{} ID{:d} FRAME{:d} {}.jpg".format( dirPath, videoName, ID, frameCount[i], frameClass)
    #             # print("\n", imgPath)
 #
    #             print("\nFrame captured.\n")
    #             frameCountSSIM = 0
    #             # Compare next frames against the last one saved
    #             image1 = image2
 #
    #             if errRead and errSet:
    #                 # Write frame to file
    #                 errWrite = cv2.imwrite(imgPath, image2)
 #
    #                 # Count class occurrences
    #                 if frameClass == 'tubo':
    #                     tuboCount = tuboCount + 1
    #                 elif frameClass == 'nada':
    #                     nadaCount = nadaCount + 1
    #                 elif frameClass == 'conf':
    #                     confCount = confCount + 1
 #
    #                 frameCount[i] = frameCount[i] + 1
    #                 ssim.append(ssimFrame)    # Record dataset ssim
 #
    #         # Error handling
    #         if not(errWrite) or not(errRead) or not(errSet) or not(errComp):
    #             print("\n!!! Error!!! ")
    #             print("ID{:2d} Frame {:3d}".format(ID, frameCount[i]))
    #             print("errWrite: {}\nerrRead: {}\nerrSet: {}\nerrComp: {}".format(errWrite, errRead, errSet, errComp))
 #
    #         errCount['errWrite'] += (not(errWrite))
    #         errCount['errSet']   += (not(errSet))
    #         errCount['errRead']  += (not(errRead))
    #         errCount['errComp']  += (not(errComp))
 #
    #         # Advance time one framePeriod
    #         frameTime = frameTime + framePeriod
 #
    #     print("ID{}: {} frames".format(ID, frameCount[i]))
    #     frameTotal = np.sum(frameCount)
 #
    # ## Information
    # print('\nErrors during extraction:')
    # print(errCount)
    # # print("errWrite", errWrite)
    # # print("errRead", errRead)
    # # print("errSet", errSet)
 #
    # print("\nFrame rate: {:.2f}".format( frameRate))
    # print("Total frames (csv): {:.2f}".format( maxFrames/1000))
    # print("Total frames (video): {:.2f}".format( video.get(cv2.CAP_PROP_FRAME_COUNT)))
    # print("Total frames acquired: ", frameTotal)
    # print("   Tubo: ", tuboCount)
    # print("   Nada: ", nadaCount)
    # print("   Conf: ", confCount)
 #
    # # Save frame totals
    # logPath = dirs.csv+"Totals"+sep+"{}.tot".format(videoName)
    # file = open(logPath, 'w')
    # file.writelines(["Tubo,Nada,Conf,Total,SSIM\n", "{},{},{},{},{}".format(tuboCount, nadaCount, confCount, frameTotal, np.mean(np.mean(ssim)))])
    # file.close()
 #
    # runTime = np.divide(runTime, 1000)
    # print("\nRun time: {} seconds (for contiguous classification, should be the same as video run time)".format(np.sum(runTime)))
    # print("   Mean: {:.2f}".format( np.mean(runTime)))
    # print("   Std: {:.2f}".format( np.std(runTime)))
 #
    # print("\nTotals saved at {}".format(logPath))
 #
    # video.release()
    # return frameTotal
