import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import smtplib
import requests

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Contact list for email
contacts = {
    "john": "john@example.com",
    "alice": "alice@example.com",
    "akshat": "your_email@example.com"
}

def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
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
            print("Microphone error:", e)
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        print("Could not understand. Please say again.")
        return "none"
    return query.lower()

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_app_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
    except Exception as e:
        print("Failed to send email:", e)

def get_weather(city):
    api_key = "cf3b55aa601d98eb1eacd10ff9a410db"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    full_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    print("Requesting:", full_url)
    response = requests.get(full_url)
    data = response.json()
    print("Response:", data)

    if data.get("cod") != 200:
        speak(f"Sorry, I couldn't find the weather for {city}. Error: {data.get('message')}")
        return

    temp = data['main']['temp']
    weather_desc = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    weather_report = f"The weather in {city} is {weather_desc} with a temperature of {temp} degrees Celsius, humidity at {humidity} percent, and wind speed of {wind_speed} meters per second."
    speak(weather_report)


# ========== MAIN LOOP ==========
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
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find any results.")

        elif 'weather' in query:
            speak("Which city's weather do you want to know?")
            city = takecommand()
            if city != "none":
                get_weather(city)
            else:
                speak("I didn't catch the city name.")

        elif 'search' in query and 'youtube' in query:
            query = query.replace('search', '').replace('youtube', '').strip()
            url = 'https://www.youtube.com/results?search_query=' + query.replace(' ', '+')
            speak(f"Searching YouTube for {query}")
            webbrowser.open_new(url)

        elif 'search' in query and 'google' in query:
            query = query.replace('search', '').replace('google', '').strip()
            url = 'https://www.google.com/search?q=' + query.replace(' ', '+')
            speak(f"Searching Google for {query}")
            webbrowser.open_new(url)

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
            try:
                speak("Who is the recipient?")
                recipient_name = takecommand().lower()
                to = contacts.get(recipient_name)

                if to is None:
                    speak(f"I don't have an email address for {recipient_name}.")
                    continue

                speak("What should I say?")
                content = takecommand()
                sendEmail(to, content)
                speak("Email has been sent successfully!")
            except Exception as e:
                print(e)
                speak("Sorry, I was not able to send the email.")

        elif 'thank you' in query:
            speak('My pleasure.')

        elif 'close' in query or 'exit' in query or 'quit' in query:
            speak('Goodbye!')
            break
