import pyautogui
import time
import threading
import psutil
import os
import webbrowser
import wikipedia
import geocoder
import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import pyjokes
import sys
import logging
from bs4 import BeautifulSoup
from datetime import datetime

class Speak:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 180)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class Task:
    def __init__(self, speaker):
        self.speaker = speaker

    def save_screenshot(self):
        try:
            ss = pyautogui.screenshot()
            os.makedirs('memory/data', exist_ok=True)
            ss.save('memory/data/screenshot.png')
            print('Screenshot saved')
            self.speaker.say('Screenshot saved successfully.')
        except Exception as e:
            print(f'Error saving screenshot: {e}')
            self.speaker.say('Sorry, I couldn\'t save the screenshot.')

    def check_battery(self):
        try:
            battery = psutil.sensors_battery()
            if battery is not None:
                percent = battery.percent
                plugged = 'plugged in' if battery.power_plugged else 'not plugged in'
                battery_status = f'Battery is at {percent}% and is {plugged}.'
            else:
                battery_status = 'Battery information not available.'
            print(battery_status)
            self.speaker.say(battery_status)
        except Exception as e:
            print(f'Error checking battery: {e}')
            self.speaker.say('Sorry, I couldn\'t retrieve battery information.')

    def check_system_performance(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')

            performance_status = (
                f'CPU Usage: {cpu_usage}%\n'
                f'Memory Usage: {memory_info.percent}%\n'
                f'Disk Usage: {disk_info.percent}%'
            )
            
            print(performance_status)
            self.speaker.say(performance_status)
        except Exception as e:
            print(f'Error checking system performance: {e}')
            self.speaker.say('Sorry, I couldn\'t retrieve system performance information.')

    def take_notes(self, note):
        try:
            os.makedirs('memory/data', exist_ok=True)
            with open('memory/data/notes.txt', 'a') as f:
                f.write('Note: ')
                f.write(note)
                f.write('\n')
            self.speaker.say('Note added successfully.')
        except Exception as e:
            print(f'Error taking note: {e}')
            self.speaker.say('Sorry, I couldn\'t save the note.')

    def get_notes(self):
        try:
            if os.path.exists('memory/data/notes.txt'):
                with open('memory/data/notes.txt', 'r') as f:
                    notes = f.read()
                print(notes)
                self.speaker.say('Here are your notes: ' + notes)
            else:
                self.speaker.say('No notes found.')
                print('No notes found.')
        except Exception as e:
            print(f'Error retrieving notes: {e}')
            self.speaker.say('Sorry, I couldn\'t retrieve the notes.')

    def delete_notes(self):
        try:
            if os.path.exists('memory/data/notes.txt'):
                os.remove('memory/data/notes.txt')
                self.speaker.say('Notes deleted successfully.')
                print('Notes deleted successfully.')
            else:
                self.speaker.say('No notes to delete.')
                print('No notes to delete.')
        except Exception as e:
            print(f'Error deleting notes: {e}')
            self.speaker.say('Sorry, I couldn\'t delete the notes.')

class Search:
    def __init__(self, speaker):
        self.speaker = speaker

    def open_browser(self, query):
        self.speaker.say('Opening' + query)
        url = f"https://www.{query}.com"
        webbrowser.open(url)

    def search_wikipedia(self, query):
        try:
            self.speaker.say('Searching Wikipedia for ' + query)
            result = wikipedia.summary(query, sentences=2)
            print('According to Wikipedia, ' + result)
            self.speaker.say('According to Wikipedia, ' + result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speaker.say('The search term is too ambiguous. Please be more specific.')
            print('DisambiguationError:', e)
        except wikipedia.exceptions.PageError as e:
            self.speaker.say('The page does not exist. Please try another query.')
            print('PageError:', e)
        except Exception as e:
            error_message = str(e)
            self.speaker.say('Sorry, I couldn\'t find any information on Wikipedia. ' + error_message)
            print('Error:', error_message)

    def search_google(self, query):
        self.speaker.say('Opening Google for ' + query)
        url = "https://www.google.com/search?q=" + query
        webbrowser.open(url)

    def get_location(self):
        try:
            loc = geocoder.ip('me')
            location_info = f'Your location is {loc.city}, {loc.state}, {loc.country}'
            self.speaker.say(location_info)
            print(location_info)
        except Exception as e:
            self.speaker.say('Sorry, I couldn\'t retrieve your location. ' + str(e))
            print('Error:', e)

    def search_weather(self, query):
        try:
            search_url = f"https://www.weather.com/en-IN/search/{query}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            weather_section = soup.find('div', class_='CurrentConditions--primary--2SVPh')
            if weather_section:
                temp = weather_section.find('span', class_='CurrentConditions--tempValue--3a50n').text
                desc = weather_section.find('div', class_='CurrentConditions--phraseValue--2xXSr').text
                weather_info = f'The weather in {query} is currently {desc} with a temperature of {temp}.'
                self.speaker.say(weather_info)
                print(weather_info)
            else:
                self.speaker.say('Weather information not found.')
                print('Weather information not found.')
        except Exception as e:
            error_message = str(e)
            self.speaker.say('Sorry, I couldn\'t retrieve the weather information. ' + error_message)
            print('Error:', error_message)

    def search_news(self, query):
        try:
            search_url = f"https://news.google.com/search?q={query}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            headlines = soup.find_all('article', limit=5)
            news_list = []
            for article in headlines:
                headline = article.find('a', class_='DY5T1d').text
                news_list.append(headline)
            
            if news_list:
                news_info = 'Top news headlines: ' + ', '.join(news_list)
                self.speaker.say(news_info)
                print(news_info)
            else:
                self.speaker.say('No news found.')
                print('No news found.')
        except Exception as e:
            error_message = str(e)
            self.speaker.say('Sorry, I couldn\'t retrieve the news. ' + error_message)
            print('Error:', error_message)

class Jarvis:
    def __init__(self):
        self.responses_file = 'memory/response/response.json'
        os.makedirs(os.path.dirname(self.responses_file), exist_ok=True)  # Ensure directory exists
        self.speak = Speak()
        self.recognizer = sr.Recognizer()
        self.sleep_mode = False
        self.search = Search(self.speak)
        self.automation = Task(self.speak)

    def greet(self):
        now = datetime.now()
        if now.hour < 12:
            self.speak.say('Good Morning! sir')
        elif now.hour >= 12 and now.hour < 18:
            self.speak.say('Good Afternoon! sir')
        else:
            self.speak.say('Good Evening! sir')

    def tell_jokes(self):
        joke = pyjokes.get_joke()
        print(joke)
        self.speak.say(joke)

    def save_response(self, query, response_text):
        response_data = {
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'user_query': query,
            'ai_response': response_text
        }

        try:
            # Read existing responses
            with open(self.responses_file, 'r') as file:
                responses = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            responses = []

        # Append new response
        responses.append(response_data)

        try:
            # Save updated responses
            with open(self.responses_file, 'w') as file:
                json.dump(responses, file, indent=4)
        except IOError as e:
            print(f'Error writing to file: {e}')
            self.speak.say('Sorry, I couldn\'t save the response.')

    def recognize_audio(self):
        with sr.Microphone() as source:
            self.speak.say('Listening for your command...')
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print(f'You said: {command}')
                return command
            except sr.UnknownValueError:
                self.speak.say('Sorry, I did not understand.')
                return None
            except sr.RequestError:
                self.speak.say('Sorry, there was an issue with the speech recognition service.')
                return None

    def process_command(self, query):
        query = query.lower()

        greetings_pattern = re.compile(r'(hello|hi|hey|good\s+morning|good\s+afternoon|good\s+evening)', re.IGNORECASE)
        time_pattern = re.compile(r'what\s+time\s+is\s+it', re.IGNORECASE)
        date_pattern = re.compile(r'what\s+date\s+is\s+it', re.IGNORECASE)
        search_pattern = re.compile(r'search\s+for\s+(.*)', re.IGNORECASE)
        battery_pattern = re.compile(r'check\s+battery', re.IGNORECASE)
        quit_pattern = re.compile(r'quit|exit|close', re.IGNORECASE)

        response_text = ''

        if re.search(greetings_pattern, query):
            response_text = 'Hello! How can I help you today?'
            self.speak.say(response_text)

        elif re.search(time_pattern, query):
            now = datetime.now()
            time_str = now.strftime('%H:%M')
            response_text = f'The current time is {time_str}.'
            self.speak.say(response_text)

        elif re.search(date_pattern, query):
            today = datetime.now()
            date_str = today.strftime('%Y-%m-%d')
            response_text = f'Today\'s date is {date_str}.'
            self.speak.say(response_text)

        elif re.search(search_pattern, query):
            search_query = re.search(search_pattern, query).group(1)
            response_text = f'Searching for {search_query}.'
            self.speak.say(response_text)
            self.search.search_google(search_query)  # You can change this to other search methods if needed

        elif re.search(battery_pattern, query):
            self.automation.check_battery()

        elif re.search(quit_pattern, query):
            response_text = 'Goodbye!'
            self.speak.say(response_text)
            sys.exit()

        else:
            response_text = 'Sorry, I did not understand that command.'
            self.speak.say(response_text)

        self.save_response(query, response_text)

    def monitor_battery(self):
        while True:
            battery = psutil.sensors_battery()
            if battery is not None and battery.percent < 30:
                self.speak.say(f'Warning: Battery is at {battery.percent}%. Please charge your device.')
            time.sleep(60)  # Check battery status every minute

    def run(self):
        self.greet()
        self.speak.say('Jarvis is now running. How can I assist you?')

        # Start the battery monitoring in a separate thread
        threading.Thread(target=self.monitor_battery, daemon=True).start()

        while True:
            if not self.sleep_mode:
                command = self.recognize_audio()
                if command:
                    self.process_command(command)

if __name__ == '__main__':
    Jarvis().run()
