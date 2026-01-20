# wsgi.py

from logging_config import setup_logging
import logging

# Setup logging config to be used over the whole app
setup_logging()

# Initialize logger for WSGI module
log = logging.getLogger(__name__)

log.info("Starting WSGI server...")

# Import the Flask app from main.py
from main import app
