import subprocess
from libs.dirs      import *

def convert_video(video_input, video_output):
    print("\nProcessing video: ", video_input)
    print("Saving to : ", video_output)

    destFolder = '/'.join(video_output.split('/')[:-1])
    create_folder(destFolder)

    cmds = ['ffmpeg', '-i', video_input, video_output]
    subprocess.Popen(cmds)

    print("Video saved to : ", video_output)
    return 0
