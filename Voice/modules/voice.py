from pydub import AudioSegment
import playsound
import requests
import asyncio
import time
import os


def voice_query(payload, url, head):
    response = requests.post(url, headers=head, json=payload)
    return response.content

def speak(text):
    url = "https://api-inference.huggingface.co/models/espnet/english_male_ryanspeech_fastspeech2"
    head = {"Authorization": "Token"}
        
    output = voice_query({
        "inputs": text
    }, url, head)

    with open("./cache/out.flac", "wb") as f:
        f.write(output)

    audio = AudioSegment.from_file("./cache/out.flac", format="flac")
    audio.export("./cache/voice.wav", format="wav")

    playsound.playsound("./cache/voice.wav")
