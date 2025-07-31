import pyttsx3
import schedule
import time
import speech_recognition as sr
import requests
serpapi_key = '5ea1d4f9f868c3da57b61dfe42a42e3744980e32a9c8f4b50479ce3d36cd0c48'
from serpapi import GoogleSearch

# ------------ TTS Setup ------------

def speak(text):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Max volume

    # Optional: Set voice (male/female)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # or voices[1].id for female

    for sentence in text.split("\n"):  # Speak each sentence separately
        engine.say(sentence)
    engine.runAndWait()

# ------------ Weather Function ------------

def get_weather(city='Mumbai'):
    api_key = "8ee6cbfeee6b4a03833150925252407"  # Your API key
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        data = requests.get(url).json()

        # Check if there's an error in response
        if "error" in data:
            return "City not found."

        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        location = data["location"]["name"]

        return f"The temperature in {location} is {temp}°C with {condition.lower()}."

    except Exception as e:
        return f"Could not fetch weather. Error: {str(e)}"

# ------------ News Function ------------

def get_news():
    params = {
        "engine": "google_news",
        "q": "top news India",
        "hl": "en",
        "api_key": '5ea1d4f9f868c3da57b61dfe42a42e3744980e32a9c8f4b50479ce3d36cd0c48'
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results", [])

        if not news_results:
            return "No news found right now."

        news_list = [f"{i+1}. {news['title']}" for i, news in enumerate(news_results[:5])]
        return "Here are the latest headlines:\n" + "\n".join(news_list)

    except Exception as e:
        return f"Error fetching news: {e}"

# ------------ Reminder System ------------

reminders = []

def set_reminder(text):
    reminders.append(text)
    speak(f"Reminder set for: {text}")

def check_reminders():
    for reminder in reminders:
        speak(f"Reminder: {reminder}")
    reminders.clear()

schedule.every(1).minutes.do(check_reminders)

# ------------ Speech Recognition ------------

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Optional but improves accuracy
        print("Listening...")
        try:
            # Increase timeout (max wait for speech) and phrase_time_limit (max speech duration)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Try again.")
            return ''
        except sr.UnknownValueError:
            speak("Sorry, I didn’t catch that.")
            return ''

# ------------ Command Handler ------------

def handle_command(command):
    if "weather" in command:
        # Extract city by removing the word "weather"
        city = command.replace("weather", "").strip()
        if not city:
            city = "Mumbai"  # fallback
        response= get_weather(city)
        speak(f'fetching weather for {city}....')
        speak(response)

    elif "news" in command or "headlines" in command:
        print("Fetching news...")
        headlines = get_news()
        print(headlines)  # Debug: Print to console
        for i in headlines.split('\n'):
            speak(i)


    elif "remind" in command:
        speak("What should I remind you about?")
        reminder = get_audio()
        if reminder:
            set_reminder(reminder)

    elif 'exit' in command:
        speak('Goodbye!')
        return False
    else:
        speak("Sorry, I don’t understand that command.")
    return True

# ------------ Main Loop ------------

if __name__ == "__main__":
    speak("Hello! What can I help you with?")
    running = True
    while running:
        command = get_audio()
        if command:
            running = handle_command(command)
        schedule.run_pending()
        time.sleep(1)

