myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()
write('output.wav', fs, myrecording)  # Save as WAV file 

sound=AudioSegment.from_wav("output.wav")
sound.export("transcript.wav",format="wav")
AUDIO_FILE="transcript.wav"

r=sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
        audio=r.record(source)
        speech = True
        try:
                transcribed = r.recognize_google(audio)
        except:
                transcribed = ""

if transcribed.lower() == 'hey':
                print("Voice Acivated")
                engine.say("Hello, how may i help")
                engine.runAndWait()
                #main()
