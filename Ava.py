# Libraries
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime as dt
import wikipedia
import pyjokes
import requests
import time
import re
from playsound import playsound

# Weather API
base_url = "https://api.openweathermap.org/data/2.5/weather?"
api_key = "24ee69ed4e9c5ecc1910b285e47ffd00"
city = "Oakville"
url = base_url + "appid=" + api_key + "&q=" + city
response = requests.get(url).json()

# Temperature Function
def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

# Timer Function
def timer(seconds):
    time.sleep(seconds)

# Calculator Functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

# Weather Conversion
temp_kelvin = response['main']['temp']
temp_celsius = kelvin_to_celsius(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celcius = kelvin_to_celsius(feels_like_kelvin)
humidity = response['main']['humidity']
description = response['weather'][0]['description']
sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
wind_speed = response['wind']['speed']

# Speech Recognition
listener = sr.Recognizer()

# Text to Speech
engine = pyttsx3.init() 
voiceList = engine.getProperty('voices')
engine.setProperty('voice', voiceList[1].id) # voice index position of 1

# Ava Functions
def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration = 1) # microphone sensitivity
            talk("Listening.")
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'ava' in command:
                command = command.replace('ava', '')
                print(command)
    except:
        command = ''
    return command

def run_ava(user_command, temperature, feels_like_temperature, humidty, desription, sunrise, sunset, wind_speed):
    command = user_command
    print(command)
    if "+" in command:
        add_num = re.findall(r'\d+', command)
        plus_occurences = command.count("+")
        add_answer = add(int(add_num[0]), int(add_num[1]))
        add_index = 1
        for add_count in range(plus_occurences):
            try:
                add_answer = add(add_answer, int(add_num[add_index + 1]))
                add_index += 1
            except:
                pass
        talk(add_answer)
    elif "-" in command:
        subtract_num = re.findall(r'\d+', command)
        minus_occurences = command.count("-")
        subtract_answer = subtract(int(subtract_num[0]), int(subtract_num[1]))
        subtract_index = 1
        for subtract_count in range(minus_occurences):
            try:
                subtract_answer = subtract(subtract_answer, int(subtract_num[subtract_index + 1]))
                subtract_index += 1
            except:
                pass
        talk(subtract_answer)
    elif "*" in command:
        multiply_num = re.findall(r'\d+', command)
        multiply_occurences = command.count("*")
        multiply_answer = multiply(int(multiply_num[0]), int(multiply_num[1]))
        multiply_index = 1
        for multiply_count in range(multiply_occurences):
            try:
                multiply_answer = multiply(multiply_answer, int(multiply_num[multiply_index + 1]))
                multiply_index += 1
            except:
                pass
        talk(multiply_answer)
    elif "/" in command:
        divide_num = re.findall(r'\d+', command)
        divide_occurences = command.count("/")
        divide_answer = divide(float(divide_num[0]), float(divide_num[1]))
        divide_index = 1
        for divide_count in range(divide_occurences):
            try:
                divide_answer = divide(divide_answer, float(divide_num[divide_index + 1]))
                divide_index += 1
            except:
                pass
        talk(divide_answer)
    elif "timer" in command:
        strTime = ""
        for t in command:
            if t.isdigit():
                strTime = strTime + t
                timer_value = int(strTime)   
        if strTime == "":
             talk("You did not set a time for the timer. Please try again.")
        else:   
            talk("Starting timer for " + strTime + " seconds.")
            timer(timer_value)
            talk("Countdown finished.")
    elif "play" in command:
        song = command.replace('play', '')
        talk("playing" + song)
        pywhatkit.playonyt(song)
    elif "time" in command:
        time = dt.datetime.now().strftime("%I:%M %p") # format: 12 hour clock with a.m. / p.m.
        talk("Current time is " + time)
    elif "what is" in command:
        try:
            wiki_info1 = command.replace("what is", '')
            info1 = wikipedia.summary(wiki_info1, 1) # single sentence
            talk(info1)
        except:
            talk("Sorry. I can't seem to find the information about this. Please try again.")
    elif "who is" in command:
        try:
            wiki_info2 = command.replace("who is", '')
            info2 = wikipedia.summary(wiki_info2, 1) # single sentence
            talk(info2)
        except:
            talk("Sorry. I can't seem to find the information about this person. Please try again.")
    elif "joke" in command:
        talk(pyjokes.get_joke())
    elif "weather" in command:
        talk("Weather in Oakville is " + description + " and is at " + str(round(temperature)) + " degrees Celcius which feels like " + str(round(feels_like_temperature)) + " degrees Celcius." + " In addition, the humidity is at " + str(round(humidity)) + "%.")
    elif "sunrise" in command:
        talk("The sun rises in Oakville at " + str(sunrise) + ".")
    elif "sunset" in command:
        talk("The sun sets in Oakville at " + str(sunset) + ".")
    elif "wind speed" in command:
        talk("The wind speed in Oakville is " + str(wind_speed) + " meters per second.")
    elif "alarm" in command:
        try:
            time_num = re.findall(r'\d+', command)
            if len(time_num) == 2:
                alarmHour = int(time_num[0])
                alarmMinute = int(time_num[1])
            else:
                alarmHour = int(time_num[0])
                alarmMinute = 0
            if "a.m." in command:
                ampm = "a.m."
                talk("Sure thing! Setting alarm for " + str(alarmHour) + " " + str(alarmMinute) + " " + ampm)
                alarmHour -= 12
                talk("Please say stop to exit out of the alarm.")
                while True:
                    if alarmHour == dt.datetime.now().hour and alarmMinute == dt.datetime.now().minute:
                        print("alarm triggered")
                        playsound("alarm.wav")
                        break
                    else:
                        stop_command = take_command()
                        print(stop_command)
                        if "stop" in stop_command:
                            talk("Alarm stopped.")
                            break
            elif "p.m." in command:
                ampm = "p.m."
                talk("Sure thing! Setting alarm for " + str(alarmHour) + " " + str(alarmMinute) + " " + ampm)
                alarmHour += 12
                talk("Please say stop to exit out of the alarm.")
                while True:
                    if alarmHour == dt.datetime.now().hour and alarmMinute == dt.datetime.now().minute:
                        print("alarm triggered")
                        playsound("alarm.wav")
                        break
                    else:
                        stop_command = take_command()
                        print(stop_command)
                        if "stop" in stop_command:
                            talk("Alarm stopped.")
                            break
            else:
                talk("You did not specify if it is a.m. or p.m. Could you please try again?")
        except:
            talk("I don't think I can set an alarm with that. Could you please try again?")
    elif "rap" in command:
        talk("I don't think you'll like it but here it goes. My money don't jiggle jiggle, it folds. I'd like to see you wiggle wiggle, for sure. It makes me wanna dribble dribble, you know. Riding in my Fiat. You really have to see it.")
    elif "thank you" in command:
        talk("Your welcome.")
    else:
        talk("I am not sure if I understood that. Could you please try again?")

# Running Ava
talk("Hi. I am your virtual assistant Ava. How can I help you?")
while True:
    command = take_command()
    if len(command) == 0:
        talk("Shutting down. See you next time.")
        break
    run_ava(command, temp_celsius, feels_like_celcius, humidity, description, sunrise_time, sunrise_time, wind_speed)