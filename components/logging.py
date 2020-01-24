import logging
from pathlib import Path

import config

def setup_logger(name, log_file):
    Path(config.LOGGING_DATA_PATH).mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(log_file) 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)      
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(log_file))

    streamer = logging.StreamHandler()
    streamer.setLevel(logging.DEBUG)
    streamer.setFormatter(formatter)
    logger.addHandler(streamer)

    return logger