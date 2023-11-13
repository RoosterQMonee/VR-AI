import speech_recognition as sr
from speech_recognition import UnknownValueError
from modules.voice import speak

import commands

from threading import Thread
import datetime
import requests
import time
import os


API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": "Token"}


ai_names = ["pi", "pie", "program"]
chat_gen = []
user_his = []


r = sr.Recognizer()
mic = sr.Microphone()


USER = os.getenv("USERNAME")


def execute(cmd, args, vars):
    getattr(commands, cmd)(args, vars)


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class var_sys:
    def __init__(self):
        self.chatting = False


class logger:
    def __init__(self, file):
        self.file = file
        self.error_queue = []
        self.processing = False

    def queue(self, error):
        self.error_queue.append(error)

    def update(self):
        Thread(target=self.process).start()

    def process(self):
        while self.processing:
            time.sleep(1)

        with open(self.file, 'a') as log:
            for item in self.error_queue:
                log.write(item + "\n")


errors = logger("errors.log")
vars = var_sys()


proc_time = datetime.datetime.now().strftime("%H:%M:%S")
print(f"[ START ][ {proc_time} ] clearing cache...")

for file in os.listdir("./cache"):
    os.remove("./cache/" + file)


text = f"Hello! How may i help you?"
speak(text)


with mic as source:

    # --// Main loop

    while True:
        audio = r.listen(source)

        # --// Transcribe Audio

        try:
            res = r.recognize_google(audio)
            res = res.lower()
        
        except UnknownValueError as e:
            print("Could not recognize audio")

            continue

        except Exception as e:
            print("Unknown error: ", e)

            errors.queue(e)
            errors.update()

            continue

        # --// Parse and Process transcription

        proc_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[ INPUT ][ {proc_time} ] " + res)

        if any(res.startswith(item) for item in ai_names):
            command = res.split(' ')

            if len(command) >= 2:
                args = command[2:]

                print(command)

                if 1:
                #try:
                    proc = execute(command[1], args, vars)

                    if type(proc) == var_sys:
                        vars = proc

                #except Exception as e:
                #    print("Unknown command, continuing as question: ", e)

        if vars.chatting:
            comp_start = time.time()

            output = query({
                "inputs": {
                    "past_user_inputs": user_his,
                    "generated_responses": chat_gen,
                    "text": res
                },
            })

            chat_gen.append(output["generated_text"])
            user_his.append(res)

            print(f"[ MODEL ][ {str(time.time() - comp_start)[:5]} ]" + output["generated_text"])
            text = output["generated_text"]

            continue
