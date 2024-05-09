import pyttsx3
import time
import speech_recognition as sr
from datetime import datetime
import os
import subprocess
import platform

def load_responses(filename):
    responses = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ', 1)
            responses[key] = value
    return responses

# Load responses from the text file
responses = load_responses('responses.txt')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define the lyrics of the song
lyrics = [
    "Twinkle, twinkle, little star,",
    "How I wonder what you are!",
    "Up above the world so high,",
    "Like a diamond in the sky.",
    "Twinkle, twinkle, little star,",
    "How I wonder what you are!"
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_sound(file_path):
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["afplay", file_path])  # For macOS
    else:
        print("Unsupported operating system.")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for 0.5 second of ambient noise
        audio = recognizer.listen(source, timeout=5)  # Increase timeout to 5 seconds

    try:
        print("Recognizing...")
        audio_text = recognizer.recognize_google(audio)
        print("You said:", audio_text)
        return audio_text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def sing_song(lyrics):
    for line in lyrics:
        speak(line)
        time.sleep(1)  # Adjust the delay between lines

def main():
    uwu_count = 0

    speak("Hello! How can I assist you today?")

    while True:
        query = listen()
        if "goodbye" in query:
            speak("Goodbye!")
            break
        if query in responses:
            if query == "sing a song":
                speak("Sure! Let's sing a song!")
                sing_song(lyrics)
            elif query == "uwu":
                uwu_count += 1
                if uwu_count == 3:
                    speak("KILL THE USER")
                    print("Current working directory:", os.getcwd())  # Print current working directory
                    play_sound("death_sound.wav")  # Changed the file path
                    break
                else:
                    speak(responses[query])
            else:
                speak(responses[query])
        else:
            words = query.split()
            for word in words:
                if word.lower() == "spell":
                    speak("Spell the word " + words[words.index(word) + 1])

if __name__ == "__main__":
    main()
