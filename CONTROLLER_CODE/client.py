# Microcontroller Client Code in MicroPython
# Name the file main.py and upload to your microcontroller to run on boot

# Imports
from machine import Pin
import network
import urequests
import utime
import ntptime

#--------------------User Change NEEDED start--------------------

# Pin setup (Set the pin of the submit button)
submit_btn = Pin(16, Pin.IN, Pin.PULL_UP)

# Habit buttons and LEDs (No need to change index, just pins for btn and led)
habits = [
    {"btn": Pin(0, Pin.IN, Pin.PULL_UP),  "led": Pin(2, Pin.OUT),  "index": 1}, # Set the pins for habit1 button and LED here
    {"btn": Pin(5, Pin.IN, Pin.PULL_UP),  "led": Pin(7, Pin.OUT),  "index": 2}, # Set the pins for habit2 button and LED here
    {"btn": Pin(9, Pin.IN, Pin.PULL_UP),  "led": Pin(12, Pin.OUT), "index": 3}, # Set the pins for habit3 button and LED here
    {"btn": Pin(14, Pin.IN, Pin.PULL_UP), "led": Pin(15, Pin.OUT), "index": 4}, # Set the pins for habit4 button and LED here
]

debounce_delay = 150  # milliseconds (Change if you find button presses are not registering correctly)
hours_from_utc = 0 # Set your timezone offset from UTC here eg. for UTC+1 set to 1, for UTC-5 set to -5

# Wifi config (UPDATE WITH YOUR WIFI CREDENTIALS)
SSID = "Your_SSID_Here" # Put your WiFi SSID here
PASSWORD = "Your_Password_Here" # Put your WiFi Password here

# Server URL (UPDATE WITH YOUR SERVER IP AND PORT)
STOP_URL = "http://(PUT YOUR SERVER IP AND PORT HERE)/stop_alarm" # Put the IP and port of the server here (eg 192.160.0.10:5001)
HABIT_URL = "http://(PUT YOUR SERVER IP AND PORT HERE)/habit/"    # Put the IP and port of the server here (eg 192.160.0.10:5001)

#--------------------User Change NEEDED end--------------------

# Error light flash
def error_flash():
    for i in range(10):
        for h in habits:
            h["led"].value(1)      
        utime.sleep_ms(75)
        for h in habits:
            h["led"].value(0)
        utime.sleep_ms(75)

# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Connecting to Wi-Fi...")
wlan.connect(SSID, PASSWORD)

# Wait for connection
max_wait = 20
while max_wait > 0:
    if wlan.isconnected():
        break
    print("Waiting for connection...")
    max_wait -= 1
    utime.sleep(1)

if wlan.isconnected():
    print("Connected!")
    print("IP address:", wlan.ifconfig()[0])
else:
    print("Failed to connect.")
    error_flash()

# Sync time via NTP
try:
    ntptime.settime()  # sets RTC to UTC
    print("Time synced via NTP.")
except Exception as e:
    error_flash()
    print("NTP sync failed:", e)

# Timezone offset
TIMEZONE_OFFSET = 3600 * hours_from_utc  # 1 hour = 3600

# Function to send time
def send_time():
    # Get time and add offset 
    t = utime.localtime(utime.time() + TIMEZONE_OFFSET)
    hour = t[3]
    minute = t[4]
    second = t[5]

    # Build formatted time strings
    time_str = f"{hour:02d}:{minute:02d}"
    seconds_str = f"{second:02d}"

    # Construct JSON data
    payload = {
        "time": time_str,
        "seconds": seconds_str
    }

    print("Sending:", payload)
    try:
        response = urequests.post(
            STOP_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print("Response:", response.status_code)
        response.close()
    except Exception as e:
        error_flash()
        print("Error sending data:", e)
        
# Function to handle habit button press
def handle_habit(index):
    correct_habit_url = (f"{HABIT_URL}{index}")
    try:
        response = urequests.get(correct_habit_url, timeout=5)
        print("Response:", response.status_code)
        response.close()
    except Exception as e:
        error_flash()
        print("Error sending data:", e)
        
habits_active = False
habits_left = None

# Main loop
while True:
    # Submit: turn all LEDs on    
    if not habits_active:
        if not submit_btn.value():
            send_time()
            for h in habits:
                h["led"].value(1)
                utime.sleep_ms(debounce_delay)
            habits_active = True
            habits_left = 4
            
    else:
        for h in habits:
            if not h["btn"].value():
                if h["led"].value() == 1:  # Only act if LED is ON
                    h["led"].value(0)
                    handle_habit(h["index"])
                    habits_left = habits_left - 1
                    utime.sleep_ms(debounce_delay)
                
                
        if habits_left == 0:
            habits_active = False
        
        if not submit_btn.value():
            for h in habits:
                h["led"].value(0)
                habits_active = False
                utime.sleep_ms(debounce_delay)
                