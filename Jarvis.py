import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning, sir.")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")
    speak("I am Jarvis, your personal assistant. How may I assist you today?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception:
        print("Say that again please.....")
        return "none"
    return query.lower()

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('avats1044@gmail.com', 'Arpit123#')
        server.sendmail('avats1044@gmail.com', to, content)
        server.close()
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand()

        if query == "none":
            continue

        # Optional: Only respond if your name Jarvis is mentioned
        if 'jarvis' not in query:
            # You can skip processing if you want wake word control
            # Otherwise comment this continue to always respond
            continue

        # Remove wake word from query for easier command detection
        query = query.replace('jarvis', '').strip()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find any results on Wikipedia.")

        elif 'search' in query and 'in youtube' in query:
            query = query.replace('search', '').replace('in youtube', '').strip()
            url = 'https://www.youtube.com/results?search_query=' + query.replace(' ', '+')
            speak(f"Searching YouTube for {query}")
            webbrowser.open_new(url)

        elif 'search' in query and 'in google' in query:
            query = query.replace('search', '').replace('in google', '').strip()
            url = 'https://www.google.com/search?q=' + query.replace(' ', '+')
            speak(f"Searching Google for {query}")
            webbrowser.open_new(url)

        elif 'open youtube' in query:
            speak('Opening YouTube')
            webbrowser.open_new('https://youtube.com')

        elif 'open python' in query:
            speak('Opening Coursera Python courses')
            webbrowser.open_new("https://coursera.org")

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

        elif 'thank you' in query:
            speak('You’re welcome, sir.')

        elif 'close' in query or 'exit' in query or 'quit' in query:
            speak('Goodbye, sir. Have a great day!')
            break
