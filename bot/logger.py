import logging
import os
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Function to setup a logger with file and stream handlers."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(LOG_DIR / log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
        # Also add a stream handler for console output if not strictly file-only
        # (Usually handled by rich in CLI, so we keep this minimal or rely on CLI tools to output)
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)

    return logger

market_logger = setup_logger('market_order', 'market_order.log')
limit_logger = setup_logger('limit_order', 'limit_order.log')
error_logger = setup_logger('error', 'error.log', level=logging.ERROR)
