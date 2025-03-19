import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import json
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "fa7e62b57e3a41ac8e9955240b919cf7"

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')
#     # Initialize the mixer module
#     pygame.mixer.init()

#     # Load the MP3 file
#     pygame.mixer.music.load("temp.mp3")  # Replace with your MP3 file

#     # Play the MP3 file
#     pygame.mixer.music.play()

#     # Keep the program running while music is playing
#     while pygame.mixer.music.get_busy():
#         continue  # Keeps checking if music is still playing
#     pygame.mixer.music.unload()
#     os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    )

    completion = client.chat.completions.create(
    model="deepseek/deepseek-chat:free",
    messages=[
        {
        "role": "system","content":"You are a virtual assitant nemed lexa skilled in tasks like Alexa and jarvis. Give short response plese",
        "role":"user","content": command
        }
    ]
    )
    return completion.choices[0].message.content
def processCommand(command):
    command = command.lower()

    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open microsoft" in command:
        speak("Opening Microsoft")
        webbrowser.open("https://microsoft.com")
    elif "open chatgpt" in command:
        speak("Opening ChatGpt")
        webbrowser.open("https://chatgpt.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "temperature" in command.lower():
        speak("Tell me the City name")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)              
        City = recognizer.recognize_google(audio).lower()       
        api = "dc4755a022f44ce2818101101251803"
        url = f"http://api.weatherapi.com/v1/current.json?key={api}&q={City}&aqi=yes"
        r = requests.get(url)
        if r.status_code == 200:
            weather_dic = json.loads(r.text)
            w = weather_dic["current"]["temp_c"]
            
            # Text to speech
            text = f"Today, the temperature in {City} is {w} degrees Celsius."
            speak(text)
        else:
            speak("Error: Invalid city name or API key.")
    elif "news" in command.lower():
        url = f"https://newsapi.org/v2/top-headlines?q=India&apiKey={newsapi}"

        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        output = aiProcess(command)
        speak(output)

if __name__ == "__main__":
    speak("Initializing lexa...")  # Fixed spelling
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            
            try:
                # Adjust for background noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Capture audio input
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

                print("Recognizing...")
                command = recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")

                # Wake word detection
                if "lexa" in command:
                    speak("Ya")
                    print("Lexa activate...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                    
                    command = recognizer.recognize_google(audio).lower()
                    processCommand(command)


            except sr.UnknownValueError:
                print("Could not understand audio. Please repeat.")
            except sr.RequestError:
                print("Could not request results, check your internet connection.")
            except Exception as e:
                print(f"Error! {e}")
