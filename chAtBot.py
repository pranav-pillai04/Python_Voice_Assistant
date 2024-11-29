import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import pyjokes
import pywhatkit as kit
from googletrans import Translator

BG_COLOR = "#2C3E50"
BUTTON_COLOR = "#3498DB"
BUTTON_FONT = ("Arial", 14, "bold")
HEADING_FONT = ("Helvetica", 24, "bold")
INSTRUCTION_FONT = ("Helvetica", 14)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

translator = Translator()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_time(name):
    hour = datetime.datetime.now().hour
    if 0 <= hour < 6:
        speak(f"Good night, {name}! Sleep tight.")
    elif 6 <= hour < 12:
        speak(f"Good morning, {name}!")
    elif 12 <= hour < 18:
        speak(f"Good afternoon, {name}!")
    else:
        speak(f"Good evening, {name}!")
    speak("How can I help you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.8
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def translate_to_hindi(text):
    translated_text = translator.translate(text, src='en', dest='hi').text
    return translated_text

def perform_task(name):
    while True:
        query = take_command()
        if 'translate' in query:
            speak("What do you want to translate to Hindi?")
            query = take_command()
            translated_text = translate_to_hindi(query)
            speak("Here is the translated text.")
            speak(translated_text)
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"There are multiple meanings for '{query}'. Please be more specific.")
                speak(f"There are multiple meanings for '{query}'. Please be more specific.")
            except wikipedia.exceptions.PageError as e:
                print(f"'{query}' does not match any Wikipedia page. Please try again.")
                speak(f"'{query}' does not match any Wikipedia page. Please try again.")
        elif 'play' in query:
            song = query.replace('play', "")
            speak("Playing " + song)
            kit.playonyt(song)
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")
        elif 'search' in query:
            s = query.replace('search', '')
            kit.search(s)
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"{name}, the time is {str_time}")
        elif 'open code' in query:
            code_path = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
        elif 'joke' in query:
            speak(pyjokes.get_joke())
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak(f"User asked to locate {location}")
            webbrowser.open("https://www.google.nl/maps/place/" + location.replace(" ", "+"))
        elif 'exit' in query:
            speak("Thanks for giving your time")
            break

def start_voice_assistant(name):
    wish_time(name)
    perform_task(name)

def main():
    root = tk.Tk()
    root.title("Chitti")
    root.geometry("500x700")
    root.configure(bg=BG_COLOR)

    background_image = Image.open("D:/python/chatbot/background.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo, bg=BG_COLOR)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    heading_label = tk.Label(root, text="Chitti", font=HEADING_FONT, bg=BG_COLOR, fg="white")
    heading_label.pack(pady=20)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(pady=50)

    image = Image.open("D:/python/chatbot/p.jpg")
    resized_image = image.resize((120, 120))
    microphone_image = ImageTk.PhotoImage(resized_image)
    microphone_label = tk.Label(frame, image=microphone_image, relief=tk.SUNKEN, bg=BG_COLOR)
    microphone_label.pack(side="top", pady=20)

    instruction_label = tk.Label(root, text="Please enter your name:", font=INSTRUCTION_FONT, bg=BG_COLOR, fg="white")
    instruction_label.pack()

    name_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
    name_entry.pack(pady=10)

    def on_button_click():
        name = name_entry.get()
        if name:
            start_voice_assistant_thread = Thread(target=start_voice_assistant, args=(name,))
            start_voice_assistant_thread.start()

    button = tk.Button(root, text="Start Assistant", command=on_button_click, font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", relief=tk.FLAT)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
