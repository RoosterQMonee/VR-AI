from pytube import YouTube
import urllib.request
import playsound
import time
import os
import re

from pydub import AudioSegment
from modules.voice import speak


def play(args, vars):
    query = '+'.join(args)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    temp = ' '.join(args)

    speak(f"OK! finding {temp}")
    print("[ MUSIC ] Finding best video...")

    for video_id in video_ids:
        yt = YouTube('https://youtu.be/' + video_id)

        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path="./cache")
        
        new_file = 'audio.mp3'
        os.rename(out_file, "./cache/" + new_file)

        print("[ MUSIC ] Downloading video " + video_id)
    
        break

    try:
        audio = AudioSegment.from_file("./cache/audio.mp3", "mp3")

    except:
        audio = AudioSegment.from_file("./cache/audio.mp3", format="mp4")

    speak(f"Playing {temp}")
    audio.export("./cache/audio.wav", format="wav")
    playsound.playsound('./cache/audio.wav')
    
    return vars