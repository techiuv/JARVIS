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
import geocoder
import spacy
import math
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


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
            self.speaker.say('Sir! Note added successfully.')
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

    def open_application(self, app_name):
        try:
            if os.name == 'nt':  # For Windows
                os.startfile(app_name)
            elif os.name == 'posix':  # For macOS/Linux
                subprocess.call(["open", app_name])
            print(f"Application {app_name} opened.")
        except Exception as e:
            print(f"Error opening application: {e}")

    def close_application(self, process_name):
        try:
            if os.name == 'nt':  # For Windows
                os.system(f"taskkill /f /im {process_name}")
            elif os.name == 'posix':  # For macOS/Linux
                os.system(f"pkill {process_name}")
            print(f"Application {process_name} closed.")
        except Exception as e:
            print(f"Error closing application: {e}")

    def set_volume(self, volume_level):
        try:
            if os.name == 'nt':  # For Windows
                os.system(f"nircmd.exe setsysvolume {volume_level}")
            elif os.name == 'posix':  # For macOS/Linux
                os.system(f"osascript -e 'set volume output volume {volume_level}'")
            print(f"Volume set to {volume_level}.")
        except Exception as e:
            print(f"Error setting volume: {e}")

    def manage_files(self, action, file_path, new_file_path=None):
        try:
            if action == "create":
                with open(file_path, "w") as f:
                    f.write("")
                print(f"File {file_path} created.")
            elif action == "delete":
                os.remove(file_path)
                print(f"File {file_path} deleted.")
            elif action == "rename" and new_file_path:
                os.rename(file_path, new_file_path)
                print(f"File renamed from {file_path} to {new_file_path}.")
        except Exception as e:
            print(f"Error in file management: {e}")

    def system_control(self, action):
        try:
            if action == "shutdown":
                if os.name == 'nt':  # For Windows
                    os.system("shutdown /s /t 1")
                elif os.name == 'posix':  # For macOS/Linux
                    os.system("sudo shutdown -h now")
            elif action == "restart":
                if os.name == 'nt':  # For Windows
                    os.system("shutdown /r /t 1")
                elif os.name == 'posix':  # For macOS/Linux
                    os.system("sudo reboot")
            elif action == "logoff":
                if os.name == 'nt':  # For Windows
                    os.system("shutdown /l")
                elif os.name == 'posix':  # For macOS/Linux
                    os.system("logout")
            print(f"System {action} initiated.")
        except Exception as e:
            print(f"Error in system control: {e}")

    def web_scrape(self, url, element):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find_all(element)
            print(f"Extracted data: {result}")
        except Exception as e:
            print(f"Error in web scraping: {e}")

    def copy_to_clipboard(self, text):
        try:
            pyperclip.copy(text)
            print("Text copied to clipboard.")
        except Exception as e:
            print(f"Error copying to clipboard: {e}")

    def paste_from_clipboard(self):
        try:
            text = pyperclip.paste()
            print(f"Text pasted from clipboard: {text}")
            return text
        except Exception as e:
            print(f"Error pasting from clipboard: {e}")

    def set_reminder(self, message, time_in_minutes):
        try:
            reminder_time = datetime.now() + timedelta(minutes=time_in_minutes)
            self.reminders[reminder_time] = message
            print(f"Reminder set for {time_in_minutes} minutes: {message}")
        except Exception as e:
            print(f"Error setting reminder: {e}")

    def check_reminders(self):
        try:
            now = datetime.now()
            for reminder_time, message in list(self.reminders.items()):
                if now >= reminder_time:
                    print(f"Reminder: {message}")
                    del self.reminders[reminder_time]
        except Exception as e:
            print(f"Error checking reminders: {e}")

    def calculate_equation(self, equation: str):
        try:
            allowed_functions = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'sqrt': math.sqrt,
                'log': math.log,
                'pow': math.pow,
                'exp': math.exp,
                'pi': math.pi,
                'e': math.e
            }
            result = eval(equation, {"__builtins__": None}, allowed_functions)
            return result
        except Exception as e:
            return f"Error calculating equation: {str(e)}"

    def close_browser(self):
        try:
            if os.name == 'nt':  # Windows OS
                subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
                subprocess.call(["taskkill", "/IM", "firefox.exe", "/F"])
                subprocess.call(["taskkill", "/IM", "msedge.exe", "/F"])
                return "Browser closed successfully."
            else:
                print("Unsupported operating system.")
        except Exception as e:
            return f"{str(e)}"


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
                self.speaker.say('Sorry! No news found.')
                print('No news found.')
        except Exception as e:
            error_message = str(e)
            self.speaker.say('Sorry, I couldn\'t retrieve the news. ' + error_message)
            print('Error:', error_message)


class Jarvis:
    def __init__(self):
        self.responses_file = 'memory/response/response.json'
        self.reminders_file = 'memory/data/reminders.json'
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
        self.nlp = spacy.load('en_core_web_sm')

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
            with open(self.responses_file, 'r') as file:
                responses = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            responses = []

        responses.append(response_data)

        try:
            with open(self.responses_file, 'w') as file:
                json.dump(responses, file, indent=4)
        except IOError as e:
            print(f'Error writing to file: {e}')
            self.speak.say('Sorry, I couldn\'t save the response.')

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
        doc = self.nlp(command)

        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        print(f"Extracted Entities: {entities}")
        print(f"Extracted Verbs: {verbs}")
        print(f"Extracted Nouns: {nouns}")

        def match_intent(verb_list, noun_list):
            if 'take' in verb_list and 'note' in noun_list:
                return 'take_note'
            if 'delete' in verb_list and 'note' in noun_list:
                return 'delete_note'
            if 'get' in verb_list and 'location' in noun_list:
                return 'get_location'
            if 'take' in verb_list and 'screenshot' in noun_list:
                return 'take_screenshot'
            if 'search' in verb_list and 'weather' in noun_list:
                return 'search_weather'
            if 'tell' in verb_list and 'joke' in noun_list:
                return 'tell_joke'
            if 'search' in verb_list and 'wikipedia' in noun_list:
                return 'search_wikipedia'
            if 'search' in verb_list and 'google' in noun_list:
                return 'search_google'
            if 'read' in verb_list and 'news' in noun_list:
                return 'search_news'
            return None

        intent = match_intent(verbs, nouns)

        if intent == 'take_note':
            self.speak.say('What would you like me to note down?')
            note = self.listen()
            if note:
                self.automation.take_notes(note)
                self.save_response(note, 'Note added.')

        elif intent == 'delete_note':
            self.automation.delete_notes()
            self.save_response(command, 'Notes deleted.')

        elif intent == 'get_location':
            self.search.get_location()
            self.save_response(command, 'Location retrieved.')

        elif intent == 'take_screenshot':
            self.automation.save_screenshot()
            self.save_response(command, 'Screenshot taken.')

        elif intent == 'search_weather':
            self.speak.say('Which city or location?')
            city = self.listen()
            if city:
                self.search.search_weather(city)
                self.save_response(command, 'Weather searched.')

        elif intent == 'tell_joke':
            self.tell_jokes()
            self.save_response(command, 'Joke told.')

        elif intent == 'search_wikipedia':
            search_match = re.search(r'wikipedia\s(.+)', command)
            if search_match:
                query = search_match.group(1)
                self.search.search_wikipedia(query)
                self.save_response(command, 'Wikipedia searched.')

        elif intent == 'search_google':
            search_match = re.search(r'google\s(.+)', command)
            if search_match:
                query = search_match.group(1)
                self.search.search_google(query)
                self.save_response(command, 'Google search initiated.')

        elif intent == 'search_news':
            self.speak.say('Which topic or region do you want news for?')
            news_topic = self.listen()
            if news_topic:
                self.search.search_news(news_topic)
                self.save_response(command, 'News searched.')

        else:
            self.speak.say("I'm sorry, I didn't understand that.")
            self.save_response(command, 'Command not understood.')

    def run(self):
        self.greet()

        task_thread = threading.Thread(target=self.task_scheduler)
        task_thread.start()

        reminder_thread = threading.Thread(target=self.reminder_checker)
        reminder_thread.start()

        while True:
            self.automation.monitor_system()
            command = self.listen()
            if command:
                self.process_command(command)


if __name__ == '__main__':
    Jarvis().run()
