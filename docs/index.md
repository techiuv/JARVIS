
# JARVIS Documentation

## Overview
JARVIS is a voice-activated assistant that performs various tasks like web searches, system checks, note-taking, and more. It leverages several Python libraries to deliver functionality, using text-to-speech, speech recognition, system monitoring, and web automation. This assistant is designed to interact with the user via voice commands and provide relevant outputs, all while running background tasks like battery monitoring.

## Libraries Used

| Library               | Purpose                                                  |
|-----------------------|----------------------------------------------------------|
| **pyautogui**          | Captures screenshots and saves them to disk.             |
| **psutil**             | Monitors CPU, memory, disk usage, and battery status.    |
| **pyttsx3**            | Converts text into spoken words.                         |
| **speech_recognition** | Recognizes voice commands using Googleâ€™s API.            |
| **wikipedia**          | Fetches Wikipedia summaries for user queries.            |
| **webbrowser**         | Opens web pages for searches or specific URLs.           |
| **geocoder**           | Detects the userâ€™s location based on their IP address.   |
| **requests**           | Sends HTTP requests for web scraping.                    |
| **BeautifulSoup**      | Parses HTML for scraping weather data and news.          |

## Approach

### Voice Interaction
JARVIS interacts with the user through voice commands, using the `speech_recognition` library to capture audio input and `pyttsx3` to provide audio feedback. 

### Task Automation
Using libraries such as `pyautogui`, `psutil`, and custom methods, JARVIS can perform tasks like saving screenshots, checking system performance, and monitoring battery status. These tasks can be triggered by specific commands recognized from the userâ€™s voice.

### Web Search and Data Fetching
JARVIS utilizes `webbrowser` to perform Google searches and `wikipedia` for querying information directly from Wikipedia. The combination of `requests` and `BeautifulSoup` allows it to scrape weather information or fetch news from external sources.

### System Monitoring
The assistant continuously monitors the battery status in a separate thread using `psutil`, alerting the user when the battery is low.

### Notes Handling
Users can take notes via voice commands, which are stored locally as text files. JARVIS can also retrieve or delete these notes based on the userâ€™s requests.
