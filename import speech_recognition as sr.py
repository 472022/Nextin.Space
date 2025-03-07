import speech_recognition as sr
import pyttsx3
import openai
import os
import webbrowser
import datetime
import threading

# OpenAI API Key (Replace with your own)
openai.api_key = "your-openai-api-key"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

# Function to Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Recognize Speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError:
        print("Speech Recognition service is unavailable")
        return ""

# Function to Get AI Response
def chat_with_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in AI response: {e}")
        return "I'm sorry, I couldn't process that."

# Function to Execute Commands
def execute_command(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {today}")
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        os._exit(0)
    else:
        response = chat_with_ai(command)
        speak(response)

# Main Function
def jarvis():
    while True:
        command = recognize_speech()
        if command:
            execute_command(command)

# Run the assistant in a separate thread
t = threading.Thread(target=jarvis)
t.daemon = True

try:
    t.start()
except KeyboardInterrupt:
    print("Shutting down...")
    os._exit(0)