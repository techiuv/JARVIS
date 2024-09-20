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
import schedule
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
            logging.error(f'Error saving screenshot: {e}')
            self.speaker.say('Sorry, I couldn\'t save the screenshot.')

    def monitor_system(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            
            
            CPU_THRESHOLD = 90  # 90% CPU usage
            MEMORY_THRESHOLD = 85  # 85% memory usage
            DISK_THRESHOLD = 90  # 90% disk usage

            # Check if any threshold is crossed
            if cpu_usage > CPU_THRESHOLD:
                alert_msg = f'Warning: High CPU usage detected at {cpu_usage}%.'
                print(alert_msg)
                self.speaker.say(alert_msg)

            if memory_info.percent > MEMORY_THRESHOLD:
                alert_msg = f'Warning: High memory usage detected at {memory_info.percent}%.'
                print(alert_msg)
                self.speaker.say(alert_msg)

            if disk_info.percent > DISK_THRESHOLD:
                alert_msg = f'Warning: High disk usage detected at {disk_info.percent}%.'
                print(alert_msg)
                self.speaker.say(alert_msg)
            
        
            return {
                'cpu': cpu_usage,
                'memory': memory_info.percent,
                'disk': disk_info.percent
            }

        except Exception as e:
            logging.error(f'Error monitoring system: {e}')
           # self.speaker.say('Sorry, I couldn\'t monitor the system.')
    

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
            logging.error(f'Error checking battery: {e}')
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
            logging.error(f'Error checking system performance: {e}')
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
            logging.error(f'Error taking note: {e}')
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
            logging.error(f'Error retrieving notes: {e}')
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
            logging.error(f'Error deleting notes: {e}')
            self.speaker.say('Sorry, I couldn\'t delete the notes.')
    def add_task(self, task_name, task_time):
        self.tasks[task_name] = task_time
        print(f"Task '{task_name}' added for {task_time}.")
        self.schedule_task(task_name, task_time)

    def schedule_task(self, task_name, task_time):
        schedule.every().day.at(task_time).do(self.execute_task, task_name)

    def execute_task(self, task_name):
        print(f"Executing Task: {task_name}")
        # Add actual task execution logic here

    def task_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Reminders
    def add_reminder(self, reminder, time_to_remind):
        self.reminders.append({'reminder': reminder, 'time': time_to_remind})
        self.save_reminders()
        print(f"Reminder '{reminder}' set for {time_to_remind}.")

    def check_reminders(self):
        current_time = datetime.now().strftime("%H:%M")
        for reminder in self.reminders:
            if reminder['time'] == current_time:
                print(f"Reminder: {reminder['reminder']}")

    def load_reminders(self):
        if os.path.exists('reminders.json'):
            with open('reminders.json', 'r') as f:
                self.reminders = json.load(f)

    def save_reminders(self):
        with open('reminders.json', 'w') as f:
            json.dump(self.reminders, f)

    def reminder_checker(self):
        while True:
            self.check_reminders()
            time.sleep(60)
    def extract_task_name(self, command):
        match = re.search(r'add task (.+)', command)
        return match.group(1) if match else "Unnamed Task"

    def extract_task_time(self, command):
        match = re.search(r'at (\d{2}:\d{2})', command)
        return match.group(1) if match else "00:00"

    def extract_reminder(self, command):
        match = re.search(r'remind me to (.+)', command)
        return match.group(1) if match else "No Reminder"

    def extract_reminder_time(self, command):
        match = re.search(r'at (\d{2}:\d{2})', command)
        return match.group(1) if match else "00:00"

 

class Search:
    def __init__(self, speaker):
        self.speaker = speaker
        self.wiki_cache = {}  

    def open_browser(self, query):
        self.speaker.say('Opening' + query)
        url = f"https://www.{query}.com"
        webbrowser.open(url)

    def search_wikipedia(self, query):
        try:
            # Check if query is already in cache
            if query in self.wiki_cache:
                result = self.wiki_cache[query]
            else:
                result = wikipedia.summary(query, sentences=2)
                self.wiki_cache[query] = result  # Cache the result

            print('According to Wikipedia, ' + result)
            self.speaker.say('According to Wikipedia, ' + result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speaker.say('The search term is too ambiguous. Please be more specific.')
            logging.error(f'DisambiguationError: {e}')
        except wikipedia.exceptions.PageError as e:
            self.speaker.say('The page does not exist. Please try another query.')
            logging.error(f'PageError: {e}')
        except Exception as e:
            error_message = str(e)
            self.speaker.say('Sorry, I couldn\'t find any information on Wikipedia. ' + error_message)
            logging.error(f'Error: {error_message}')

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
            logging.error(f'Error retrieving location: {e}')
            self.speaker.say('Sorry, I couldn\'t retrieve your location. ' + str(e))

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
            logging.error(f'Error retrieving weather information: {e}')
            self.speaker.say('Sorry, I couldn\'t retrieve the weather information. ' + str(e))

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
            logging.error(f'Error retrieving news: {e}')
            self.speaker.say('Sorry, I couldn\'t retrieve the news. ' + str(e))

class Jarvis:
    def __init__(self):
        self.responses_file = 'memory/response/response.json'
        self.reminders_file = 'memory/data/Reminders.json
        os.makedirs(os.path.dirname(self.responses_file), exist_ok=True)  # Ensure directory exists
        os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)  
        self.speak = Speak()
        self.recognizer = sr.Recognizer()
        self.sleep_mode = False
        self.search = Search(self.speak)
        self.automation = Task(self.speak)
        self.tasks = {}
        self.reminders = []
        self.load_reminders()

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

    def listen(self):
        with sr.Microphone() as source:
            print('Listening...')
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                print(f'You said: {text}')
                return text.lower()
            except sr.UnknownValueError:
                self.speak.say('Sorry, I could not understand what you said.')
                return None
            except sr.RequestError as e:
                logging.error(f'Error with the speech recognition service: {e}')
                self.speak.say('Sorry, the service is unavailable at the moment.')
                return None

    def process_command(self, command):
        if re.search(r'\btake notes?\b', command):
            self.speak.say('What would you like me to note down?')
            note = self.listen()
            if note:
                self.automation.take_notes(note)

        elif re.search(r'\bdelete notes?\b', command):
            self.automation.delete_notes()

        elif re.search(r'\bcheck notes?\b', command):
            self.automation.get_notes()

        elif re.search(r'\bbattery\b', command):
            self.automation.check_battery()

        elif re.search(r'\bscreenshot\b', command):
            self.automation.save_screenshot()

        elif re.search(r'\bopen\b', command):
            browser_match = re.search(r'open\s(\w+)', command)
            if browser_match:
                site = browser_match.group(1)
                self.search.open_browser(site)

        elif re.search(r'\bwikipedia\b', command):
            search_match = re.search(r'wikipedia\s(.+)', command)
            if search_match:
                query = search_match.group(1)
                self.search.search_wikipedia(query)

        elif re.search(r'\bgoogle\b', command):
            search_match = re.search(r'google\s(.+)', command)
            if search_match:
                query = search_match.group(1)
                self.search.search_google(query)

        elif re.search(r'\blocation\b', command):
            self.search.get_location()

        elif re.search(r'\bweather\b', command):
            location_match = re.search(r'weather in (.+)', command)
            if location_match:
                location = location_match.group(1)
                self.search.search_weather(location)

        elif re.search(r'\bnews\b', command):
            topic_match = re.search(r'news about (.+)', command)
            if topic_match:
                topic = topic_match.group(1)
                self.search.search_news(topic)

        elif re.search(r'\bperformance\b', command):
            self.automation.check_system_performance()

        elif re.search(r'\bjoke\b', command):
            self.tell_jokes()

    def run(self):
    self.greet()

    task_thread = threading.Thread(target=self.task_scheduler)
    task_thread.start()

    reminder_thread = threading.Thread(target=self.reminder_checker)
    reminder_thread.start()

    health_check_thread = threading.Thread(target=self.health_check_periodic)
    health_check_thread.start()


    while not self.sleep_mode:
        self.automation.monitor_system()  # Check system health
        command = self.listen()
        if command:
            self.process_command(command)


if __name__ == '__main__':
    Jarvis().run()
