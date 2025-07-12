import speech_recognition as sr
import webbrowser
import pyttsx3
from gtts import gTTS
import pygame
import time
import os
import musiclibrary


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()
    
def speak(text):
    
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    if "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    if "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
if __name__ == "__main__":
    speak("Initializing Iris....")
    while True:
        # Listen for the wake word "nova"
        

        # obtain audio from the microphone
        r = sr.Recognizer()
        
            
       

        # recognize speech using gtts
        try:
            with sr.Microphone() as source:
                print("Listening...!")
                audio = r.listen(source, timeout=4, phrase_time_limit=4)
            word = r.recognize_google(audio)
            if"iris" in word.lower():
                speak("Yes")
               
                #listen for command
                with sr.Microphone() as source: 
                    print("Iris Active...!")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)
                
        except Exception as e:
            print("error; {0}".format(e))
        
    