import pytchat
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 135)

chat = pytchat.create(video_id="ID")
while chat.is_alive():
    for c in chat.get().sync_items():
        msg = f"{c.author.name} said {c.message}"
        print(msg)

        engine.say(msg)
        engine.runAndWait()
