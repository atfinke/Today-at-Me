import urllib.request, json 
from datetime import datetime

from components import cache, logging
from configuration import config

logger = logging.setup_logger(
    'theme-park', config.THEME_PARKS_LOGGING_PATH)
memory_cache = None

def fetch_wait_times():
    global memory_cache
    logger.info('fetch_wait_times: called')

    if memory_cache:
        logger.info('fetch_wait_times: checking memory cache')
    else:
        logger.info('fetch_wait_times: checking disk cache')
        memory_cache = cache.fetch(config.THEME_PARKS_CACHE_PATH)

    content = cache.content(memory_cache, config.THEME_PARKS_CACHE_LIFETIME)
    if content:
        return content

    rides = []
    with urllib.request.urlopen(config.THEME_PARKS_DLR_URL) as url:
        for park_rides in list(json.loads(url.read().decode()).values()):
            rides.extend(park_rides)
    with urllib.request.urlopen(config.THEME_PARKS_WDW_URL) as url:
        for park_rides in list(json.loads(url.read().decode()).values()):
            rides.extend(park_rides)

    logger.info('fetch_wait_times: got {} rides'.format(len(rides)))

    memory_cache = cache.save(rides, config.THEME_PARKS_CACHE_PATH)
    return rides

def invalidate_memory_cache():
    logger.info('invalidate_memory_cache: called')

    global memory_cache
    memory_cache = None