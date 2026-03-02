# Sleep Bot

Sleep Bot — gamify your sleep.

## About
Link to video about it: [sleepBot video](#todo link once published)

Sleep Bot is a system that tracks sleep-related habits and rewards consistency through streaks, multipliers, and clock-out enforcement. It is NOT plug and play, as it requires a controller be made.

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
```
Then add your Pushover details into a file named **keys.json** (make it yourself) in the sleepBotWebServer directory if you want notifications to be sent to your phone.

Format:
```
{
    "user_key":"USER KEY HERE",
    "app_token":"APP TOKEN HERE"
}
```
You can then test it with:
```
gunicorn -w 1 -b 0.0.0.0:8000 wsgi:app
```
And make a systemd service file for it to run at launch.

Example systemd service file:
```
[Unit]
Description=Sleep Bot Server
After=network.target

[Service]
User={USERNAME}
Group={USERNAME}
WorkingDirectory=/home/{USERNAME}/sleepBotWebServer
Environment="PATH=/home/{USERNAME}/sleepBotWebServer/venv/bin"

ExecStart=/home/{USERNAME}/sleepBotWebServer/venv/bin/gunicorn \
  --workers 1 \
  --worker-class gthread \
  --threads 2 \
  --timeout 30 \
  --keep-alive 2 \
  --bind 0.0.0.0:8000 \
  wsgi:app

Restart=always
RestartSec=3
KillSignal=SIGQUIT
TimeoutStopSec=30
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
```



Requirements:

- Python 3.10 or newer

- Local network access for connected devices

- Audio output device ***correctly*** set up on Pi

### 2. Microcontroller (Raspberry Pi Pico)

- Copy the contents of `CONTROLLER_CODE/client.py` into a new Python file on the Pi Pico

- Update the following values in the file:

  - Wi-Fi SSID

  - Wi-Fi password

  - Server IP address

- Save the file as `main.py` so it runs on boot

### 3. iPhone (Apple Shortcuts App)

- Install both of the Apple shortcuts linked below and **set them up correctly.** (Instructions are written in each shortcut; start with the Clockout shortcut)

  - [Clockout](https://www.icloud.com/shortcuts/d828db62e8924f3683a13e43066be386)

  - [Clockout Fail Check](https://www.icloud.com/shortcuts/9b7c0413d8c0449291d5b9c00977033d)

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See the [LICENSE](LICENSE) file for details.