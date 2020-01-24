import logging

def setup_logger(name, log_file):
    handler = logging.FileHandler(log_file)  
    logger = logging.getLogger(name)      
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(log_file))
    return logger