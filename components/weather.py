import requests

import config
from components import logging

logger = logging.setup_logger(
    'weather', config.WEATHER_LOGGING_PATH)

def fetch():
    logger.info('fetch: called')
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(config.WEATHER_CURRENT_CITY, config.WEATHER_API_KEY))
    except:
        logger.error('fetch: failed to get weather')
        return []
    logger.info('fetch: got weather')
    return r.json()