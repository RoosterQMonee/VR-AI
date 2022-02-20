import speech_recognition as sr
from pydub import AudioSegment
import os
from datetime import date
import sounddevice as sd
from scipy.io.wavfile import write
from random import choice, randint
import pyttsx3
import time
import webbrowser
from tkinter import *
from playsound import playsound

# Commands

hello = ["hi", "Hi", "hello", "Hello", "wsg", "Wsg", "WSG", "sup", "Sup", "hey", "Hey", "hi!", "Hi!", "hello!",
         "Hello!", "wsg!", "Wsg!", "WSG!", "sup!", "Sup!", "hey!", "Hey!", "hi :)", "Hi :)", "hello :)", "Hello :)",
         "wsg :)", "Wsg :)", "WSG :)", "sup :)", "Sup :)", "hey :)", "Hey :)", "hi! :)", "Hi! :)", "hello! :)",
         "Hello! :)", "wsg! :)", "Wsg! :)", "WSG! :)", "sup! :)", "Sup! :)", "hey! :)", "Hey! :)", "Ello", "ello",
         "'Ello", "'ello"]
bye = ["bye", "Bye", "goodbye", "Goodbye", "good bye", "Good Bye", "see you", "See you", "later", "Later", "byee",
       "Byee", "byeee", "Byeee"]

insult = ["fucktard", "idot", "idiot", "dumbass", "motherfucker", "stupid", "gay", "fucker", "Fucktard", "Idot",
          "Idiot", "Dumbass", "Motherfucker", "Stupid", "Gay", "Fucker" "ur fat", "Ur fat", "your fat", "Your fat",
          "youre fat", "youre fat", "faggot", "retard", "bitch", "whore", "thot", "fat", "fatty", "ur gay", "Ur gay",
          "your gay", "youre gay", "Youre gay", "Fag", "fag", "Loser", "loser"]
compliment = ["gg", "good job", "nice", "great", "awesome", "good", "your hot", "ur hot", "youre hot", "youre awesome",
              "youre cool", "Nice"]

hi = ["Sup", "Hello", "Hi", "good morning", "Good morning", "Good afternoon", "good afternoon", "good evening",
      "Good evening"]
hi2 = ["Sup", "Hello", "Hi"]
gn = ["Good night", "good night"]

yes = ["yes", "Sure!", "sure", "of course", "yeah"]
no = ["yeah no", "no", "heck no"]

thankYou = ["thank you", "Thank you", "Thanks", "thanks", "Thank you", "thank you", "thx!", "Thx!", "Ty!", "ty!",
            "Thanks!", "thanks!", "Thank u", "thank u"]

startTimer = ["Can you start a timer", "Can you start a timer?", "can you start a timer", "can you start a timer?",
              "please start a timer", "Please start a timer", "timer start", "Timer start", "start timer",
              "Start timer", "can you please start a timer?", "can you start a timer please",
              "Can you start a timer please", "can you start a timer please?", "Can you start a timer please?"]
endTimer = ["End the timer please", "end the timer please", "please end the timer", "Please end the timer", "timer end",
            "Timer end", "End timer", "end timer", "Stop the timer please", "stop the timer please",
            "please stop the timer", "Please stop the timer", "timer stop", "Timer stop", "Stop timer", "stop timer"]

howMany = ["How many", "how many", "how many?", "How many?"]
canIJoin = ["can i join", "Can i join", "Can i join?", "can i join?", "can I join", "Can I join", "Can I join?",
            "can I join?"]
howAreYou = ["How are you", "how are you", "How are you?", "how are you?", "How are you doing", "how are you doing",
             "how are you doing?", "How are you doing?", "How are u", "how are u", "How are u?", "how are u?"]
howImDoing = ["Ok so far", "Pretty good", "Good", "Great"]

wyd = ["What are you doing", "what are you doing", "Wyd", "wyd", "WYD", "What are you doing?", "what are you doing?",
       "Wyd?", "wyd?", "WYD?"]
wid = ["Smoking crack", "Coding", "Talking to people", "Nothing right now", "Playing piano", "Invading poland",
       "Making tacos"]

invpoland = ["wanna go invade poland", "Wanna go invade poland", "Wanna go invade poland?", "wanna go invade poland?",
             "want to go invade poland"]
ily = ["i love you", "I love you", "ily", "Ily", "ILY", "i <3 you", "I <3 you", "i <3 u", "i love u", "I love u"]
isFren = ["Are you a friend", "are you a friend", "Are you a friend?", "are you a friend?", "Are you fren",
          "are you fren", "Are you a fren?", "are you a fren?", "Are you a fren", "are you a fren", "Are you a fren?",
          "are you a fren?", "Are you fren?", "are you fren?", "are you fren", "Are you fren"]

whatCanYouDo = ["What can you do", "what can you do", "what can you do?", "What can you do?", "What do you do?",
                "what do you do?", "cmd use", "Cmd use", "!use"]
theDate = ["What is the date", "what is the date", "what is today", "What is today", "can you please tell me the date",
           "Can you please tell me the date", "what is the date today", "What is the date today", "What is the date?",
           "what is the date?", "what is today?", "What is today?", "can you please tell me the date?",
           "Can you please tell me the date?", "what is the date today?", "What is the date today?"]



enable_speech = ["enable speech", "speech enable", "speech on"]
disable_speech = ["disable speech", "speech disable", "speech off"]

enable_man = ["enable manual", "manual enable", "manual on"]
disable_man = ["disable manual", "manual disable", "manual off"]

openSite = ["Open site", "open site", "website", "site", "site open"]

engine = pyttsx3.init()
fs = 44100
seconds = 3

strtTime = 0
endtime = 0

manual = False
speech = True
bot_name = ['ivan', 'hey ivan', 'boot ivan', 'help ivan', 'Yo ivan wake up']
toSay = ''
count = 0
window = Tk()

try:
    os.remove('output.wav', 'transcript.wav')
except:
    pass

print("Started!")


def main():
    global count
    while count < 3:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write('output.wav', fs, myrecording)  # Save as WAV file

        sound = AudioSegment.from_wav('output.wav')
        sound.export('transcript.wav', format="wav")

        AUDIO_FILE = "transcript.wav"

        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            global speech
            global manual
            global strtTime
            global endtime
            global toSay
            audio = r.record(source)
            try:
                transcribed = r.recognize_google(audio)
            except:
                transcribed = "Sorry, i did not understand"
                engine.say(transcribed)
                engine.runAndWait()
                if manual == True:
                    transcribed = input("Manual Command> ")

            try:
                print("Transcription: " + transcribed)
                text = transcribed.lower()

                if text in theDate:
                    toSay = (date.today())

                elif text in openSite:
                    engine.say("What site do you want to open?")
                    engine.runAndWait()

                    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                    sd.wait()
                    write('output.wav', fs, myrecording)  # Save as WAV file

                    AUDIO_FILE = "output.wav"

                    r = sr.Recognizer()
                    with sr.AudioFile(AUDIO_FILE) as source:
                        audio = r.record(source)
                        speech = True
                        try:
                            transcribed = r.recognize_google(audio)
                        except:
                            transcribed = "I couldn't understand what you said"
                            engine.say(transcribed)
                            engine.runAndWait()

                        print(transcribed)
                        engine.say("Opening site.")
                        engine.runAndWait()

                        if transcribed != "I couldn't understand what you said":
                            url = f'https://www.{transcribed}.org'
                            webbrowser.open(url)

                            if transcribed.lower() != 'python':
                                url = f'https://www.{transcribed}.com'
                                webbrowser.open(url)

                elif text in compliment:
                    toSay = choice(thankYou)

                elif text in whatCanYouDo:
                    toSay = f"I am {bot_name}. I can answer questions and run commands as you wish! Just remember i was made by a thirteen year old and a twelve year old"

                elif text in isFren:
                    toSay = "Of course, im always here to help"

                elif text in canIJoin:
                    toSay = 'Sure'

                elif text in insult:
                    toSay = "You do know i don't get offended, right?"

                elif text in enable_man:
                    manual = True

                elif text in disable_man:
                    manual = False

                elif text in ily:
                    playsound('yugay.wav')

                elif text in wyd:
                    toSay = choice(wid)

                elif text in thankYou:
                    toSay = "You're welcome"

                elif text in howMany:
                    toSay = str(randint(1, 50))

                elif text in howAreYou:
                    toSay = choice(howImDoing)

                elif text in invpoland:
                    toSay = "Sure"

                elif text in hi:
                    toSay = choice(hi2)

                elif text in hello:
                    toSay = choice(hi2)

                elif text in bye:
                    toSay = choice(bye)

                elif text in startTimer:
                    strtTime == time.time()
                    toSay = 'Ok'

                elif text in endTimer:
                    endtime == time.time()
                    toSay = (f'Ok, Time is {str(endtime - strtTime)}')

                elif text in enable_speech:
                    global speech
                    speech = True
                    toSay = "Ok"

                elif text in disable_speech:
                    global speech
                    speech = False
                    toSay = "Ok"
                    
                elif text == 'what is the time':
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(current_time)

                else:
                    toSay = "Unknown command"

                print(toSay)

                if speech == True:
                    engine.say(toSay)
                    engine.runAndWait()

                else:
                    count += 1
                    pass

                input("")
            except:
                pass
                # input("Continue? ")
    count = 0


while True:
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, myrecording)

    sound = AudioSegment.from_wav("output.wav")
    sound.export("transcript.wav", format="wav")
    AUDIO_FILE = "transcript.wav"

    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
        speech = True
        try:
            transcribed = r.recognize_google(audio)
        except:
            pass

    try:
        if transcribed.lower() in bot_name and transcribed:
            print("Voice Acivated")
            engine.say(f"Hello {os.getenv('USERNAME')}, how may i help")
            engine.runAndWait()

            main()
    except:
        pass
