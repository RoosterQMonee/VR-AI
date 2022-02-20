import os

os.system("git clone https://github.com/RoosterQMonee/GTAG-PyAI.git")
os.chdir("GTAG-PyAI")

os.system("pip install opencv-python")
os.system("pip install pandas")
os.system("pip install re")
os.system("pip install ctypes")
os.system("pip install SpeechRecognition")
os.system("pip install pydub")
os.system("pip install sounddevice")
os.system("pip install scipy")
os.system("pip install pyttsx3")

print("Installed Dependencies.")
