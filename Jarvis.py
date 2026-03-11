import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import smtplib
import requests

# ================= CONFIG =================

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

# ================= SPEAK FUNCTION =================

def speak(text):
    print("Jarvis:", text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 210)
    engine.say(text)
    engine.runAndWait()

# ================= GREETING =================

def wishme():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("Hello Akshat, I am Jarvis. How can I help you?")

# ================= VOICE INPUT =================

def takecommand():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)

            audio = r.listen(source, timeout=5, phrase_time_limit=7)

        query = r.recognize_google(audio, language='en-in')
        print("User said:", query)

        return query.lower()

    except sr.WaitTimeoutError:
        return "none"

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return "none"

    except Exception as e:
        print("Mic Error:", e)
        return "none"

# ================= EMAIL FUNCTION =================

def sendEmail(to, content):

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login("your_email@gmail.com", "your_app_password")

        server.sendmail("your_email@gmail.com", to, content)

        server.quit()

        speak("Email sent successfully")

    except Exception as e:
        print(e)
        speak("Failed to send email")
    
# ================= JOKES =========================

def get_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        data = response.json()

        setup = data["setup"]
        punchline = data["punchline"]

        print(setup)
        speak(setup)

        print(punchline)
        speak(punchline)

    except:
        speak("Sorry, I could not retrieve a joke right now.")
        print("Error fetching joke")

# ================= WEATHER =================

def get_weather(city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:

        data = requests.get(url).json()

        if data["cod"] != 200:
            speak("City not found")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]

        speak(f"The weather in {city} is {desc}")
        speak(f"Temperature is {temp} degree Celsius")
        speak(f"Humidity is {humidity} percent")

    except Exception as e:
        print(e)
        speak("Unable to fetch weather")

# ================= NEWS =================

def get_news():

    speak("Which country's news do you want?")
    country = takecommand()

    code = country_map.get(country)

    if not code:
        speak("Country not supported")
        return

    url = f"https://newsapi.org/v2/top-headlines?country={code}&apiKey={NEWS_API_KEY}"

    try:

        data = requests.get(url).json()

        articles = data["articles"][:5]

        speak(f"Top headlines from {country}")

        for i, article in enumerate(articles, 1):
            speak(f"News {i}")
            speak(article["title"])

    except Exception as e:
        print(e)
        speak("Error fetching news")

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

        # Wikipedia
        if "wikipedia" in query:

            speak("Searching Wikipedia")

            try:
                result = wikipedia.summary(query.replace("wikipedia",""), sentences=2)
                speak(result)

            except:
                speak("No result found")

        # Weather
        if "weather" in query:

            speak("Tell me the city name")
            city = takecommand()

            if city != "none":
                get_weather(city)

        # News
        elif "news" in query:

            get_news()
            
        # Jokes
        elif "joke" in query:
            
            get_joke()

        # YouTube search
        elif "search youtube" in query:

            q = query.replace("search youtube","")
            webbrowser.open(f"https://www.youtube.com/results?search_query={q}")

        # Google search
        elif "search google" in query:

            q = query.replace("search google","")
            webbrowser.open(f"https://www.google.com/search?q={q}")

        # Open websites
        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            webbrowser.open("https://google.com")

        elif "open github" in query:
            webbrowser.open("https://github.com")

        elif "open spotify" in query:
            webbrowser.open("https://spotify.com")

        # Email
        elif "send email" in query:

            speak("Who is the recipient")

            name = takecommand()

            if name in contacts:

                speak("What should I say?")
                content = takecommand()

                sendEmail(contacts[name], content)

            else:
                speak("Contact not found")

        # Exit
        elif "exit" in query or "quit" in query or "stop" in query:

            speak("Goodbye Akshat")
            break