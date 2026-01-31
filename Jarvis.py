import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import smtplib
import requests

# ================= CONFIG =================

engine = pyttsx3.init()
engine.setProperty('rate', 150)

contacts = {
    "john": "john@example.com",
    "alice": "alice@example.com",
    "akshat": "your_email@example.com"
}

WEATHER_API_KEY = "cf3b55aa601d98eb1eacd10ff9a410db"
NEWS_API_KEY = "f3659c69ba474baa97a0aefa4d4dce33"

country_map = {
    "india": "in",
    "united states": "us",
    "usa": "us",
    "united kingdom": "gb",
    "uk": "gb",
    "canada": "ca",
    "australia": "au",
    "germany": "de",
    "france": "fr"
}

# ================= CORE FUNCTIONS =================

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("Hello, I am Jarvis. How can I help you?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except Exception:
            return "none"

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        speak("Sorry, I didn't catch that.")
        return "none"

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_app_password")
        server.sendmail("your_email@gmail.com", to, content)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print("Email error:", e)

def get_weather(city):
    if city == "none":
        speak("City name not received.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        data = requests.get(url).json()

        if data.get("cod") != 200:
            speak("City not found.")
            return

        speak(
            f"The weather in {city} is {data['weather'][0]['description']}. "
            f"Temperature {data['main']['temp']} degree Celsius, "
            f"humidity {data['main']['humidity']} percent."
        )
    except Exception as e:
        speak("Unable to fetch weather.")
        print("Weather error:", e)

def get_news():
    speak("Which country's news would you like?")
    country_input = takecommand()

    if country_input == "none":
        return

    country_code = country_map.get(country_input)
    if not country_code:
        speak("Country not supported.")
        return

    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={NEWS_API_KEY}"

    try:
        data = requests.get(url).json()
        articles = data.get("articles", [])[:5]

        if not articles:
            speak("No news available.")
            return

        speak(f"Top headlines from {country_input}")
        for i, article in enumerate(articles, 1):
            speak(f"News {i}: {article['title']}")
    except Exception as e:
        speak("Error fetching news.")
        print("News error:", e)

# ================= MAIN PROGRAM =================

if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()

        if query == "none":
            continue

        if "jarvis" not in query:
            continue

        query = query.replace("jarvis", "").strip()

        if 'wikipedia' in query:
            speak("Searching Wikipedia")
            try:
                result = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
                speak(result)
            except Exception:
                speak("No results found.")

        elif 'weather' in query:
            speak("Tell me the city name.")
            get_weather(takecommand())

        elif 'news' in query:
            get_news()

        elif 'search youtube' in query:
            q = query.replace("search youtube", "").strip()
            speak(f"Searching YouTube for {q}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}")

        elif 'search google' in query:
            q = query.replace("search google", "").strip()
            speak(f"Searching Google for {q}")
            webbrowser.open(f"https://www.google.com/search?q={q.replace(' ', '+')}")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")

        elif 'open spotify' in query:
            speak("Opening Spotify")
            webbrowser.open("https://spotify.com")

        elif 'send email' in query:
            speak("Recipient name?")
            name = takecommand()
            to = contacts.get(name)

            if to:
                speak("What should I say?")
                content = takecommand()
                sendEmail(to, content)
            else:
                speak("Contact not found.")

        elif 'exit' in query or 'quit' in query or 'close' in query:
            speak("Goodbye Akshat.")
            break
