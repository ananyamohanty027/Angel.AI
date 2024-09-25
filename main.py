import random
import pyautogui
import requests
import wikipedia
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import cv2
import random
import time
from bs4 import BeautifulSoup
# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Select a female voice


def speak(audio):
    print(audio)  # Print to terminal
    engine.say(audio)  # Speak the text
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)

    # Define a list of greetings
    morning_greetings = [
        "Good morning!  Hope your day is filled with positivity and success!",
        "Rise and shine!  Wishing you a productive morning ahead!",
        "Good morning!  Let's seize the day with enthusiasm!"
    ]

    afternoon_greetings = [
        "Good afternoon!  How's your day going so far?",
        "Afternoon!  Let's make the most of this beautiful day!",
        "Good afternoon!  I hope you're enjoying your day!"
    ]

    evening_greetings = [
        "Good evening!  Hope you had a fantastic day!",
        "Evening!  Time to unwind and relax!",
        "Good evening!  I hope you’re ready for a wonderful evening!"
    ]

    if hour < 12:
        greet = random.choice(morning_greetings)
        speak(greet)
    elif hour < 18:
        greet = random.choice(afternoon_greetings)
        speak(greet)
    else:
        greet = random.choice(evening_greetings)
        speak(greet)
    speak("Hi, I am Angel")
    intro = [
        "I'm here to assist you with whatever you need.",
        "Your personal assistant, at your service!",
        "Ready to help you with your tasks today!"
    ]
    speak(random.choice(intro))

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Could you please repeat?")
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    return query.lower()

def searchWikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results for this query. Please be more specific.")
    except Exception:
        speak("Sorry, I couldn't find anything on Wikipedia.")

def getWeather(city):
    api_key = "2243618f45e024a907aea7bf9e505eb5"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()

        if data["cod"] == "404":
            speak("City not found. Please try again.")
            print("City not found. Please try again.")
        else:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
            # print(f"The current temperature in {city} is {temp}°C with {description}.")
    
    except Exception:
        speak("Sorry, I am unable to fetch the weather at the moment.")

def takeScreenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("C:\\Users\\Ananya\\Documents\\screenshot.png")  # Save in Documents
    speak("Screenshot has been taken and saved in your Documents folder.")

def takePhoto():
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera
    if not cap.isOpened():
        speak("Could not access the camera.")
        return
    
    speak("Please smile for the photo...")
    print("Taking your photo in 3 seconds...")
    time.sleep(3)

    ret, frame = cap.read()  # Capture a frame
    if ret:
        cv2.imwrite("my_photo.png", frame)  # Save the photo
        speak("Your photo has been taken and saved as my_photo.png.")
        print("Your photo has been saved as my_photo.png.")
    else:
        speak("Sorry, I couldn't take the photo.")
        print("Error: Could not take the photo.")
    
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close any OpenCV windows
def googleSearch(query):
    speak(f"Searching Google for {query}")
    
    # Perform Google search
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Scrape the highlighted search result (snippet)
        result_divs = soup.find_all('div', class_="BNeawe s3v9rd AP7Wnd")
        
        if result_divs:
            top_result = result_divs[0].get_text()  # Get the top result
            speak(f"The top result is: {top_result}")
            print(f"Top result: {top_result}")
        else:
            speak("Sorry, I couldn't find any results for your query.")
    else:
        speak("Sorry, I'm unable to connect to Google at the moment.")
if __name__ == "__main__":
    wishMe()
    
    while True:
        query = TakeCommand().lower()

        if 'who is' in query:
            speak("Searching Wikipedia...")
            searchWikipedia(query.replace("who is", ""))

        
        elif "take screenshot" in query:
            takeScreenshot()

        elif 'weather in' in query:
            city = query.split("in")[-1].strip()
            speak(f"Fetching weather details for {city}")
            getWeather(city)

        elif "take photo" in query:
            takePhoto()

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")
        
        elif "open google" in query and 'search' not in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif "open google and search" in query:
            # Extract search term from the command if already provided
            search_query = query.replace("open google and search", "").strip()
            
            # If no search term was included, ask the user for it
            if not search_query:
                speak("What do you want me to search?")
                search_query = TakeCommand()
                
            # Proceed with search if valid query is provided
            if search_query != "None" and search_query:
                googleSearch(search_query)  # Perform the search and speak the result
            else:
                speak("I couldn't catch that. Please try again.")
        
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "open code" in query:
            speak("Opening Visual Studio Code")
            codePath = "C:\\Users\\Ananya\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif "open notepad" in query:
            speak("Opening Notepad")
            os.startfile("C:\\Windows\\System32\\notepad.exe")
        
        elif "write in notepad" in query:
            speak("What would you like me to write?")
            note_text = TakeCommand()
            with open("notepad.txt", "w") as f:
                f.write(note_text)
            speak("I have written it in notepad.")
        
        elif "stop listening" in query:
            speak("Goodbye! Have a nice day.")
            break

        elif "thank" in query or "thanks" in query or "thank you" in query:
            responses = [
                "You're welcome!  Have a fantastic day ahead!",
                "No problem at all!  Always here to help!",
                "My pleasure!  If you need anything else, just ask!",
                "Glad to be of assistance! Enjoy your day!",
                "You're very welcome!  Don't hesitate to reach out if you need more help!"
            ]
            speak(random.choice(responses)) 
            break 
        else:
            speak("I'm sorry, I didn't understand that. Could you repeat?")
