import psutil
from math import floor
from datetime import datetime
from subprocess import Popen, PIPE

from components import logging
from configuration import config

logger = logging.setup_logger(
    'monitor', config.MONITOR_LOGGING_PATH)

memory_cache = None
battery_cache = None

def fetch_stats():
    global memory_cache
    logger.info('fetch_stats: called')

    existing_cache = memory_cache
    if existing_cache:
        logger.info('fetch_stats: checking memory cache')

    if existing_cache:
        date = existing_cache[config.CACHE_DATE_KEY]
        if datetime.now().timestamp() < date + config.MONITOR_CACHE_LIFETIME:
            logger.info('fetch_stats: using cache')
            return existing_cache[config.CACHE_CONTENT_KEY]
        else:
            logger.info('fetch_stats: cache too old {}'.format(datetime.now().timestamp() - date))

    formatted_results = {
        config.MONITOR_CPU_KEY: floor(psutil.cpu_percent()),
        config.MONITOR_MEMORY_KEY: floor(dict(psutil.virtual_memory()._asdict())['percent']),
        config.MONITOR_BATTERY_LEVEL_KEY: fetch_battery()
    }

    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: formatted_results
    }
    memory_cache = cache_dict

    return formatted_results

def fetch_battery():
    global battery_cache
    logger.info('fetch_battery: called')

    existing_cache = battery_cache
    if existing_cache:
        logger.info('fetch_battery: checking memory cache')

    if existing_cache:
        date = existing_cache[config.CACHE_DATE_KEY]
        if datetime.now().timestamp() < date + config.MONITOR_BATTERY_CACHE_LIFETIME:
            logger.info('fetch_battery: using cache')
            return existing_cache[config.MONITOR_INFO_KEY]
        else:
            logger.info('fetch_battery: cache too old {}'.format(datetime.now().timestamp() - date))

    ps = Popen('pmset -g batt|grep -Eo "\d+%"', shell=True, stdout=PIPE)
    battery = int(ps.communicate()[0][:-2].decode("utf-8"))
    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.MONITOR_INFO_KEY: battery
    }
    battery_cache = cache_dict

    return battery
    
def invalidate_memory_cache():
    logger.info('invalidate_memory_cache: called')

    global battery_cache
    battery_cache = None