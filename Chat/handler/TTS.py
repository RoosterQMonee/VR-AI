from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
import os

mytext = """
"""
language = 'en'

try: os.remove("test.wav"), os.remove("welcome.mp3")
except: pass

myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")

src = "welcome.mp3"
dst = "test.wav"
                                                    
audSeg = AudioSegment.from_mp3(src)
audSeg.export(dst, format="wav")

playsound("test.wav")
