import logging
import os

from .constants import LOG_FILE, REPORT_DIR

# Ensure the reports directory exists for logs
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', REPORT_DIR)
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, LOG_FILE)

def setup_logging():
    """Sets up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),  # Log to file
            logging.StreamHandler()  # Log to console
        ]
    )
    logging.info("Logging setup complete.")

# Initialize logging when this module is imported
setup_logging()

logger = logging.getLogger(__name__)