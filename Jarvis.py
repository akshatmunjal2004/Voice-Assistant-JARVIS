import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import smtplib
import requests

# ========== CONFIG ==========

engine = pyttsx3.init()
engine.setProperty('rate', 150)

contacts = {
    "john": "john@example.com",
    "alice": "alice@example.com",
    "akshat": "your_email@example.com"
}

weather_api_key = "cf3b55aa601d98eb1eacd10ff9a410db"
news_api_key = "f3659c69ba474baa97a0aefa4d4dce33"

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

# ========== CORE FUNCTIONS ==========

def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
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
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except Exception as e:
            speak("Microphone issue occurred.")
            return "none"

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        speak("Could not understand. Please say again.")
        return "none"

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_app_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

def get_weather(city):
    if not city or city == "none":
        speak("I didn't catch the city name.")
        return

    full_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    try:
        response = requests.get(full_url)
        data = response.json()

        if data.get("cod") != 200:
            speak(f"Sorry, I couldn't find the weather for {city}.")
            return

        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_report = (
            f"The weather in {city} is {weather_desc}, "
            f"temperature is {temp}°C, humidity is {humidity} percent, "
            f"and wind speed is {wind_speed} meters per second."
        )
        speak(weather_report)

    except Exception as e:
        speak("I was unable to fetch the weather.")
        print("Weather error:", e)

def get_news():
    speak("Which country's news would you like to hear?")
    country_input = takecommand().lower()

    country_code = country_map.get(country_input)
    if not country_code:
        speak("Sorry, I don't support news from that country yet.")
        return

    api_key = "f3659c69ba474baa97a0aefa4d4dce33"
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={api_key}"

    try:
        response = requests.get(url)
        news_data = response.json()

        if news_data["status"] != "ok" or not news_data["articles"]:
            speak("Sorry, no news found.")
            return

        articles = news_data["articles"][:5]
        speak(f"Here are the top news headlines from {country_input.capitalize()}.")

        for i, article in enumerate(articles, 1):
            title = article.get('title')
            if title:
                speak(f"News {i}: {title}")
            else:
                speak(f"News {i}: Title not available")

    except Exception as e:
        speak("An error occurred while getting the news.")
        print("News error:", e)


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if query == "none" or "jarvis" not in query:
            continue

        query = query.replace("jarvis", "").strip()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            try:
                results = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find any results.")

        elif 'weather' in query:
            speak("Which city's weather do you want to know?")
            get_weather(takecommand())

        elif 'news' in query:
            get_news()

        elif 'search' in query and 'youtube' in query:
            query = query.replace('search', '').replace('youtube', '').strip()
            speak(f"Searching YouTube for {query}")
            webbrowser.open_new(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")

        elif 'search' in query and 'google' in query:
            query = query.replace('search', '').replace('google', '').strip()
            speak(f"Searching Google for {query}")
            webbrowser.open_new(f"https://www.google.com/search?q={query.replace(' ', '+')}")

        elif 'open youtube' in query:
            speak('Opening YouTube')
            webbrowser.open_new('https://youtube.com')

        elif 'open google' in query:
            speak('Opening Google')
            webbrowser.open_new('https://google.com')

        elif 'open github' in query:
            speak('Opening GitHub')
            webbrowser.open_new("https://github.com")

        elif 'open stackoverflow' in query:
            speak('Opening StackOverflow')
            webbrowser.open_new('https://stackoverflow.com')

        elif 'open spotify' in query:
            speak('Opening Spotify')
            webbrowser.open_new('https://spotify.com')

        elif 'send email' in query:
            speak("Who is the recipient?")
            recipient_name = takecommand().lower()
            to = contacts.get(recipient_name)

            if to:
                speak("What should I say?")
                content = takecommand()
                sendEmail(to, content)
                speak("Email has been sent successfully!")
            else:
                speak(f"I don't have an email address for {recipient_name}.")

        elif 'thank you' in query:
            speak('My pleasure.')

        elif 'close' in query or 'exit' in query or 'quit' in query:
            speak('Goodbye!')
            break
