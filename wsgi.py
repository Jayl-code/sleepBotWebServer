from main import app
from logging_config import setup_logging
import logging

setup_logging()

log = logging.getLogger(__name__)

# Main starting point for gunicorn 
if __name__ == "__main__":
    log.debug("Starting app with gunicorn")
    app.run()