import speech_recognition as sr
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3
import query
import os

engine = pyttsx3.init()
fs = 44100
seconds = 5
toSay = ''

try: os.remove('output.wav', 'transcript.wav')
except: pass

print("Started!")

API_URL = "https://api-inference.huggingface.co/models/TheDiamondKing/DialoGPT-small-harrypotter"
headers = {"Authorization": "Bearer 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"}

gens = []
inps = []

def main(text):
        inps.append(text)
        if text:
                toSay = query(
                        API_URL,
                        headers,
                        {
                        "inputs": {
                                        "past_user_inputs": inps,
                                        "generated_responses": gens,
                                        "text": text,
                                },
                        })
                        
                gens.append(toSay['generated_text'])

                print(toSay)

                engine.say(toSay['generated_text'])
                engine.runAndWait()

        else:
                print("Command Error")
                pass

while True:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait(), write('output.wav', fs, myrecording)

        sound=AudioSegment.from_wav("output.wav")
        sound.export("transcript.wav", format="wav")
        AUDIO_FILE="transcript.wav"

        r=sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
                audio=r.record(source)
                speech = True
                try: transcribed = r.recognize_google(audio)
                except: pass

        try:
                print(transcribed)
                if transcribed.lower():
                        print("Voice Acivated")
                        main(transcribed)

        except: pass
