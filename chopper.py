'''
    invocation: python chopper.py <project_directory_name>
      - the project directory must have a chopper.txt file
      - the project directory should have a directory called "videos" and "audio"
    
      Chopper File Format: [v | a] <video_name.mp4> <t_start> <t_end> <clip_name.mp4>
        - t_start and t_end can be expressed in seconds (15.35), in (min, sec), in (hour, min, sec), or as a string: ‘01:03:05.35’
'''

import sys
import os
from moviepy.editor import *
import ffmpeg

def chop_media(src, s, e, target):
    clip = VideoFileClip(src)
    clip = clip.subclip(s, e)
    clip.write_videofile(target)

def main():
    PATH = os.path.split(os.getcwd())[0] + "\\"

    if len(sys.argv) == 2:
        PATH = PATH + sys.argv[1] + "\\"

    else:
        print('Usage: python3 chopper.py <project_directory_name>')
        sys.exit(1)

    with open(PATH+"chopper.txt", 'r') as f:
        chops = [line.strip().split(" ") for line in f.readlines() if line[0] != '#']

    for src, s, e, target in chops:
        chop_media(PATH+"videos/"+src+".mp4", s, e, PATH+"clips/video/{}.mp4".format(target))
        chop_media(PATH+"audio/"+src+".mp4", s, e, PATH+"clips/audio/{}.mp4".format(target))

    # # convert all .mp4 audio clips to .wav
    for f in os.listdir(PATH+"audio"):
        if f.endswith(".mp4"):
            print(f)
            stream = ffmpeg.input(PATH+"audio/"+f)
            stream = ffmpeg.output(stream, PATH+"clips/audio/"+f.split(".")[0]+".wav")
            ffmpeg.run(stream)

    # delete all .mp4 video clips
    for f in os.listdir(PATH+"audio"):
        if f.endswith(".mp4"):
            os.remove(os.path.join(PATH+"clips/audio", f))


if __name__ == "__main__":
    main()