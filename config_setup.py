# config_setup.py

# Imports
import json
import logging

log = logging.getLogger(__name__)

# File paths
config_file = 'config.json'

# Creates config file with default settings if it doesn't exist
def setup_config(file_path=config_file):
    defaults = {
    "alarm_time": "00:00",
    "clockout_time": "00:00",
    "alarm_days": {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": True,
        "sunday": True
    },
    "light_control": False
}
    
    try:
        with open(file_path, 'x') as file:
            json.dump(defaults, file, indent=4)
            log.info("Config file created with default settings.")
    except FileExistsError:
        # File already exists
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if not content:  # empty file so fill with defaults
                log.info("Config file was empty, writing default settings.")
                with open(file_path, "w") as f:
                    json.dump(defaults, f, indent=4)
            else:
                log.info("Config file already exists.")

    return
