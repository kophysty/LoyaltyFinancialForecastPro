import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create a logger
    logger = logging.getLogger("loyalty_model")
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler - daily rotating log file
    today = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f"logs/loyalty_model_{today}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create a global logger instance
logger = setup_logger()

def log_error(error, context=None):
    """Log an error with optional context"""
    error_message = f"Error: {str(error)}"
    if context:
        error_message += f"\nContext: {context}"
    logger.error(error_message, exc_info=True)

def log_warning(message, context=None):
    """Log a warning with optional context"""
    warning_message = message
    if context:
        warning_message += f"\nContext: {context}"
    logger.warning(warning_message)

def log_info(message):
    """Log an info message"""
    logger.info(message)

def log_debug(message):
    """Log a debug message"""
    logger.debug(message)
