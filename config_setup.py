# Imports
import json

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
    except FileExistsError:
        # File already exists
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if not content:  # empty file
                with open(file_path, "w") as f:
                    json.dump(defaults, f, indent=4)

    return
