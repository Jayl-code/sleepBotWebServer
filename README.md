# Sleep Bot

Sleep Bot — gamify your sleep.

## About

Sleep Bot is a system that tracks sleep-related habits and rewards consistency through streaks, multipliers, and clock-out enforcement.

## Features

- Habit tracking gives bonus points or higher streaks
- Streaks of consecutive completed days increase score multipliers
- Clock-out feature ensures you are off your phone at a set time

## Installation
### 1. Web Server (Raspberry Pi via SSH)
```bash
git clone https://github.com/Jayl-code/sleepBotWebServer.git
cd ~/sleepBotWebServer

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

gunicorn -w 1 -b 0.0.0.0:8000 wsgi:app
```

Requirements:

- Python 3.10 or newer

- Local network access for connected devices

### 2. Microcontroller (Raspberry Pi Pico)

- Copy the contents of `CONTROLLER_CODE/client.py` into a new Python file on the Pi Pico

- Update the following values in the file:

  - Wi-Fi SSID

  - Wi-Fi password

  - Server IP address

- Save the file as `main.py` so it runs on boot

### 3. iPhone (Apple Shortcuts App)

- Install both of the Apple shortcuts linked below and **set them up correctly.** (Instructions written in each shortcut, start with Clockout shortcut)

  - Clockout shortcut `https://www.icloud.com/shortcuts/89e42f065e2440089f876fa15507fd86`

  - Clockout Fail Check shortcut `https://www.icloud.com/shortcuts/2447c12af3424ac6bc879eb5c448a6af`

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See the [LICENSE](LICENSE) file for details.