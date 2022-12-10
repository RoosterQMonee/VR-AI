from modules.voice import speak

def echo(args, vars):
    print("[ VOICE ] You said: ", ' '.join(args))
    speak("You said, " + ' '.join(args))

    return vars