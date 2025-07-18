import speech_recognition as sr
import webbrowser
import pyttsx3
from gtts import gTTS
import pygame
import time
import os
import musiclibrary
import pyjokes
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()


# text to speech
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
        speak("Opening Google")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("Opening Youyube")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "tell a joke" in c.lower():
        tell_joke()
    elif "take notes" in c.lower():
        text = command.replace("note", "").strip()
        notes(text)
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    else:
        speak("Sorry, I don't understand that yet.")

def notes(text):
    with open("notes.txt", "a") as file:
        file.write(f"{text}\n")
    speak("notes saved.")


def tell_joke():
    joke = pyjokes.get_joke()
    print(f"[JOKE]: {joke}")
    speak(joke)

if __name__ == "__main__":
    speak("Initializing Iris....")
    while True:
        # Listen for the wake word "iris"

        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech
        try:
            with sr.Microphone() as source:
                print("say 'Iris' to activate...!")
                audio = r.listen(source, timeout=4, phrase_time_limit=4)
            word = r.recognize_google(audio)
            if "iris" in word.lower():
                iris_active = True
                speak("Iris is ready!")
        except Exception as e:
            print("Error:", e)
            continue

            # listen for command
        while iris_active:
            try:
                with sr.Microphone() as source:
                    print("Iris Active. Awaiting for your command...!")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                if any(
                    exit_word in command
                    for exit_word in ["go to sleep", "exit", "stop", "deactivate"]
                ):
                    speak("Alrigt Boss, going to sleep")
                    iris_active = False
                else:
                    processCommand(command)

            except sr.WaitTimeoutError:
                print("Timeout : No speech Detected.")
            except sr.UnknownValueError:
                print("I couldn't understand what you said..")
                speak("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print("Network Error")
                speak("Sorry, I can't connect to the service currently..")
            except Exception as e:
                print("error; {0}".format(e))
