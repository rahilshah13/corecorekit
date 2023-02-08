'''
invoation: python downloader.py <project_directory_name>
- the project directory must have a media.txt file
'''
import sys
import os
from pytube import YouTube

def main():
    PATH = os.path.split(os.getcwd())[0] + "\\"

    if len(sys.argv) == 2:
        PATH = PATH + sys.argv[1] + "\\"

    else:
        sys.exit(1)

    with open(PATH+"media.txt", 'r') as f:
        media = [line.strip().split(" ") for line in f.readlines() if line[0] != '#']
    
    for url, target in media:
        print(url, target)
        YouTube(url).streams.filter(file_extension='mp4', only_audio=True).first().download(output_path=PATH+"audio/", filename=target+".mp4")       
        YouTube(url).streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(output_path=PATH+"videos/", filename=target+".mp4")

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