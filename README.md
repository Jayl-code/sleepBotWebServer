# Sleep Bot

Sleep Bot, gamify sleep.

## About

Sleep Bot is a way of gamifying sleep into something you can get a high score in. 

## Features

- Habit tracking gives bonus points or higher streaks
- Streaks of consecutive compleated days to increase multiplier
- Clockout feature ensures you are off your phone at a set time

## Installation

Steps to install and set up the project:

1. On pi via SSH
```bash
git clone https://github.com/Jayl-code/sleepBotWebServer.git
cd ~/sleepBotWebServer
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
deactivate
gunicorn -w 1 -b 0.0.0.0:8000 wsgi:app
```
2. Then on microcontroller with correct I/O attached
```
-Copy the content of CONTROLLER_CODE/client.py to a new python file on a Pi pico.

-Update the required information in the file such as SSID, password and server IP address

-Save the file as main.py so it runs on boot
```
3. On iPhone in the Shortcuts app
```
-In the automation tab add new automation 

-Select NFC and scan the tag, select run immediately then next

-Create new shortcut

-Add 'Get Battery Status' block and change it to 'Is connected to charger'

-Add 'if' block

-Under 'if Battery State' add 'Get contents of URL'

-Set the URL to http://(IP of the server):8000/clockout
```
## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.  
See the [LICENSE](LICENSE) file for details.