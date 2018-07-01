import os
import cv2              as cv
import numpy            as np

def get_frames(videoPath, interval=5, destFolder="./images/", verbose=False):
    '''
        videoPath:  Video source path.
        interval:   Frame capture period in seconds.
        destFolder: Frame destination folder.
    '''
    videoName   = videoPath.split("/")[-1]
    videoFolder = videoPath.split("20170724_FTP83G_Petrobras/")[-1]
    destFolder  = destFolder+"/".join(videoFolder.split("/")[:-1])+"/"

    try:
        os.makedirs(destFolder)
    except OSError:
        # Folder already exists or destFolder is invalid
        pass

    video = cv.VideoCapture(videoPath)

    frameRate   = video.get(cv.CAP_PROP_FPS)
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

        print("\nTotal frames: ", videoTotalFrames)
        print("Frame Rate:     ", frameRate)
        print("Runtime:        ", videoRuntime)
        print("Interval:       ", interval, "\n")

        for frameTime in tqdm(captureTimes):
            errSet = video.set(cv.CAP_PROP_POS_MSEC, frameTime)

            errRead, frame = video.read()
            frameCount +=1

            # Write frame as jpg
            imgPath = destFolder+"{} {}.jpg".format(videoName, frameCount)
            print("\n")
            print(imgPath)
            errWrite = cv.imwrite(imgPath, frame)
            print("ErrWrite? ",errWrite)

    else:
        for frameTime in captureTimes:
            errSet = video.set(cv.CAP_PROP_POS_MSEC, frameTime)

            errRead, frame = video.read()
            frameCount +=1

            # Write frame as jpg
            imgPath = destFolder+"{} {}.jpg".format(videoName, frameCount)
            errWrite = cv.imwrite(imgPath, frame)

    print("\nCaptured {} frames.".format(frameCount))
    print("\nSaved {} frames at {}".format(frameCount, imgPath))


    return frameCount

if __name__ == "__main__":
    videoPath = "../../20170724_FTP83G_Petrobras/GHmls16-263_OK/DVD-1/20161101202838328@DVR-SPARE_Ch1.wmv"

    frameNum = get_frames(videoPath, interval=5, verbose=True)
