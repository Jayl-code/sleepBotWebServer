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

- Open **Shortcuts → Automation**

- Tap **+**

- Select **NFC**

- Scan your NFC tag

- Choose **Run Immediately**

- Create a new shortcut:

  - Add **Get Battery Status**

  - Change it to **Is Connected to Charger**

  - Add an **If** block

  - Inside the `If Battery State` block, add **Get Contents of URL**

  - Set the URL to:
    ``` arduino
    http://<SERVER_IP>:8000/clockout
    ```

This automation triggers the clock-out action when the phone is charging and the NFC tag is scanned.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See the [LICENSE](LICENSE) file for details.