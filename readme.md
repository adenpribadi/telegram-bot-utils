# Telegram Bot for System Control and Capture

This Telegram bot provides various system control commands and functionalities for remote control over a device. The bot can be used to control the system, capture images/videos, record audio, retrieve system information, and more. It uses the `telebot` library for interaction with the Telegram API.

## Features

### System Control
- **Shutdown**: Initiates system shutdown after a 5-second countdown.
- **Restart**: Restarts the system after a 5-second countdown.
- **Hibernate**: Puts the system into hibernation.
- **Lock**: Locks the computer screen.
- **Say**: Converts text to speech and reads it aloud.

### System Information
- **Battery**: Displays battery status, charging status, and time remaining.
- **CPU**: Displays CPU usage percentage.
- **RAM**: Displays RAM usage percentage.
- **IP**: Retrieves the public IP address.
- **Whoami**: Retrieves user and system information (username, hostname, OS, version).

### Capture Commands
- **Capture**: Captures a screenshot from the specified source (`desktop`, `webcam`).
- **Records**: Records a video or audio from webcam or microphone. Duration can be specified.
- **Share Screen**: Starts or stops screen sharing. (Requires a WebSocket server to handle screen sharing.)
- **Keylogger**: Starts or stops capturing keystrokes from the device. The keylogger logs every key pressed, including special keys (e.g., space, enter, backspace), and saves them with timestamps in a log file for later review.

### AI Integration
- **Ask**: The bot can answer questions using AI integration (powered by your `ask_question` function).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/adenpribadi/telegram-bot-utils.git
   cd telegram-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:
   - Ensure you have a valid Telegram bot token. You can obtain this by creating a bot via [BotFather](https://core.telegram.org/bots#botfather).
   - Place your token in the script where `self.bot = telebot.TeleBot(token)` is defined.

4. Start the bot:
   ```bash
   python app.py
   ```

5. Optionally, run a WebSocket server for screen sharing. Modify the IP address in the `share_screen` function if necessary.

## Usage

Once the bot is running, you can interact with it on Telegram using the following commands:

- `/shutdown`: Shut down the system after a 5-second countdown.
- `/restart`: Restart the system after a 5-second countdown.
- `/hibernate`: Put the system into hibernation.
- `/lock`: Lock the computer screen.
- `/say <text>`: Convert the provided text to speech.
- `/ask <question>`: Ask the bot a question and get an AI-generated answer.
- `/capture <source>`: Capture a screenshot from either `desktop` or `webcam`.
- `/records <source> <duration>`: Record a video or audio from the webcam or microphone. The duration is optional and defaults to 5 seconds.
- `/battery`: Get the battery status.
- `/cpu`: Get the current CPU usage.
- `/ram`: Get the current RAM usage.
- `/ip`: Get the public IP address of the system.
- `/whoami`: Get the current user's information (username, hostname, OS).

### Screen Sharing
- `/sharescreen start`: Starts sharing the screen (requires WebSocket server).
- `/sharescreen stop`: Stops screen sharing.

### Keylogger
- `/keylogger start`: Starts recording keystrokes from the device, logging every key pressed with timestamps.
- `/keylogger stop`: Stops recording keystrokes and ends the logging process.

## Notes
- Some commands may require administrative privileges on the system.
- Screen sharing functionality requires a WebSocket server. Please ensure it's properly configured.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- `psutil` for system information.
- `telebot` for interacting with the Telegram API.
- `Flask` and other dependencies for web and server functionalities.


### What to do next:
1. **Dependencies**: List all the required dependencies like `telebot`, `psutil`, `requests`, etc., in a `requirements.txt` file for easy installation. You can create this file by running:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Update with Your Information**: If you have any custom links, project-specific information, or additional instructions, feel free to modify the `README.md` content.

3. **Optional Features**: If you're adding more features or modifying existing ones, remember to update the `README.md` accordingly!


## Warning
The Keylogger feature and other features in this application are designed for educational and personal experimentation purposes only. Using this application for other purposes, especially for monitoring or collecting data without consent, may violate privacy laws and regulations.

**Important to note**:

- `Privacy and Security`: Using a keylogger or any other feature to monitor someone else's device without their consent is illegal in many countries. You must ensure that this application is used only in a legal environment and with explicit permission from all parties involved.
- `Misuse of the Application`: I, as the creator of this application, am not responsible for any damage or misuse resulting from the use of this application. The user is solely responsible for how this application is used and ensuring that it is used ethically and in compliance with applicable laws.
**Use this application wisely and responsibly.**
