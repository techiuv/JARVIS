# Jarvis - Your Personal Assistant

Jarvis is a voice-activated personal assistant built using Python. It can perform various tasks such as taking notes, fetching system statistics, tracking location, and more. This project is currently under development, and new features are being added regularly.

## Features

- **Note Management**: Add, retrieve, and delete notes.
- **System Information**: Get CPU usage, memory usage, and disk usage.
- **Location Tracking**: Get your current location based on your IP address.
- **Time**: Retrieve the current time.
- **Browser Control**: Open websites in your default web browser.
- **Screenshot**: Take and save screenshots.
- **Battery Check**: Check the battery status of your device.
- **Jokes**: Tell a random joke.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or higher installed on your system. You also need to install the following Python packages:

- `pyttsx3` - Text-to-Speech engine
- `speech_recognition` - Speech recognition library
- `psutil` - System and process utilities
- `geocoder` - Geocoding library
- `pyautogui` - GUI automation library
- `pyjokes` - Python package for jokes

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```
## Setting Up
### Clone the repository:

```bash
git clone https://github.com/techiuv/JARVIS.git
cd JARVIS
```
### Ensure that the required directories exist:

- `memory/data/notes.txt` - For storing notes.
- `data/` - For storing screenshots.

**You may need to create these directories if they do not exist:**
```bash\
mkdir -p memory/data
mkdir -p data
```

### Running the Application
To start Jarvis, run the `jarvis.py` script:
```bash
python JARVIS.py
```
Jarvis will greet you and start listening for your commands. You can interact with it using voice commands such as "take a note", "get notes", "check CPU usage", "tell me a joke", etc.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or find bugs.

### How to Contribute
- Fork the repository.
- Create a feature branch (git checkout -b feature/new-feature).
- Commit your changes (git commit -am 'Add new feature').
- Push to the branch (git push origin feature/new-feature).
- Create a new Pull Request.

## License
This project is licensed under the `MIT License` - see the LICENSE file for details.

## Status
**Under Development:** This project is actively being developed. Features are being added, and improvements are ongoing. If you encounter any issues or have suggestions, please let us know!

## Contact
For any questions or suggestions, feel free to open an issue or contact me directly at mail.yuvraj0317@gmail.com.
