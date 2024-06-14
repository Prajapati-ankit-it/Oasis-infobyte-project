import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# OpenWeatherMap API key
API_KEY = '6ddec2f560686e41e571e8cd7fe99e48'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to convert text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to recognize speech and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

# Function to tell the current time
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The time is {current_time}")

# Function to tell the current date
def tell_date():
    today = datetime.date.today()
    speak(f"Today's date is {today.strftime('%B %d, %Y')}")

# Function to perform a web search
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.get().open(url)
    speak(f"Here are the search results for {query}")

# Function to get weather information
def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        speak(f"The current weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't retrieve the weather information.")

# Main function to handle voice commands
def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        tell_time()
    elif "date" in command:
        tell_date()
    elif "search" in command:
        query = command.replace("search", "").strip()
        search_web(query)
    elif "weather" in command:
        city = command.replace("weather in", "").strip()
        get_weather(city)
    else:
        speak("Sorry, I can only respond to simple commands like 'hello', 'time', 'date', 'search', and 'weather'.")

# Run the assistant in a loop to continuously listen for commands
def run_assistant():
    speak("Voice assistant activated. How can I help you?")
    while True:
        command = listen()
        if "exit" in command or "stop" in command:
            speak("Goodbye")
            break
        handle_command(command)

# Start the voice assistant
if __name__ == "__main__":
    run_assistant()