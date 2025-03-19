import logging
import os
import time
from logging.handlers import RotatingFileHandler

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
        
    def _initialize_logger(self):
        """Initialize the logger."""
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger('portals2d')
        self.logger.setLevel(logging.DEBUG)
        
        # Log file with timestamp
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        log_file = os.path.join(logs_dir, f'portals2d-{timestamp}.log')
        
        # File handler with rotation
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
        
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
        
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
        
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
        
    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)
