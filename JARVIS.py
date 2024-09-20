import pyautogui
import time
import threading
import psutil
import os
import webbrowser
import wikipedia
import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import pyjokes
import logging
import schedule
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
            CPU_THRESHOLD = 90
            MEMORY_THRESHOLD = 85
            DISK_THRESHOLD = 90

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


class Search:
    def __init__(self, speaker):
        self.speaker = speaker
        self.wiki_cache = {}

    def open_browser(self, query):
        self.speaker.say('Opening ' + query)
        url = f"https://www.{query}.com"
        webbrowser.open(url)

    def search_wikipedia(self, query):
        try:
            if query in self.wiki_cache:
                result = self.wiki_cache[query]
            else:
                result = wikipedia.summary(query, sentences=2)
                self.wiki_cache[query] = result

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


class Jarvis:
    def __init__(self):
        self.responses_file = 'memory/response/response.json'
        self.reminders_file = 'memory/data/Reminders.json'
        os.makedirs(os.path.dirname(self.responses_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)
        self.speak = Speak()
        self.recognizer = sr.Recognizer()
        self.search = Search(self.speak)
        self.automation = Task(self.speak)
        self.tasks = {}
        self.reminders = []
        self.load_reminders()
        self.reminder_lock = threading.Lock()

    def load_reminders(self):
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r') as f:
                self.reminders = json.load(f)

    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f)

    def task_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def reminder_checker(self):
        while True:
            self.check_reminders()
            time.sleep(60)

    def check_reminders(self):
        current_time = datetime.now().strftime("%H:%M")
        with self.reminder_lock:
            for reminder in self.reminders:
                if reminder['time'] == current_time:
                    print(f"Reminder: {reminder['reminder']}")
                    self.speak.say(f"Reminder: {reminder['reminder']}")

    def greet(self):
        now = datetime.now()
        if now.hour < 12:
            self.speak.say('Good Morning! sir')
        elif now.hour >= 12 and now.hour < 18:
            self.speak.say('Good Afternoon! sir')
        else:
            self.speak.say('Good Evening! sir')

    def listen(self):
        with sr.Microphone() as source:
            print('Listening...')
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
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

    def run(self):
        self.greet()

        task_thread = threading.Thread(target=self.task_scheduler)
        task_thread.start()

        reminder_thread = threading.Thread(target=self.reminder_checker)
        reminder_thread.start()

        while not self.sleep_mode:
            self.automation.monitor_system()
            command = self.listen()
            if command:
                self.process_command(command)


if __name__ == '__main__':
    Jarvis().run()
