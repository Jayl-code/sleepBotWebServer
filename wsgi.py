# wsgi.py

# Imports
from logging_config import setup_logging
import logging

# Import the Flask app from main.py
from main import app

# Setup logging config to be used over the whole app
setup_logging()

# Initialize logger
log = logging.getLogger(__name__)

# Main starting point for gunicorn 
if __name__ == "__main__":
    app.run()
    log.info("WSGI server started")