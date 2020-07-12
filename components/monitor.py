import psutil
from math import floor
from datetime import datetime
from subprocess import Popen, PIPE, run

from components import cache, logging
from configuration import config

logger = logging.setup_logger(
    'monitor', config.MONITOR_LOGGING_PATH)

memory_cache = None
battery_cache = None
powermetrics_cache = None

def fetch_stats(force_cache=False):
    global memory_cache
    logger.info('fetch_stats: called')

    if memory_cache:
        logger.info('fetch_stats: checking memory cache')
        if force_cache:
            logger.info('fetch_stats: force cache')
            return memory_cache[config.CACHE_CONTENT_KEY]

    content = cache.content(memory_cache, config.MONITOR_CACHE_LIFETIME, False)
    if content:
        return content

    formatted_results = {
        config.MONITOR_CPU_KEY: floor(psutil.cpu_percent()),
        config.MONITOR_MEMORY_KEY: floor(dict(psutil.virtual_memory()._asdict())['percent']),
    }

    try:
        battery = _fetch_battery()
        if battery:
            formatted_results[config.MONITOR_BATTERY_KEY] = battery
    except:
        pass

    for key, value in _fetch_powermetrics().items():
        formatted_results[key] = value

    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: formatted_results
    }
    memory_cache = cache_dict

    return formatted_results

def _fetch_battery():
    global battery_cache
    logger.info('_fetch_battery: called')

    if battery_cache:
        logger.info('_fetch_battery: checking memory cache')

    content = cache.content(battery_cache, config.MONITOR_BATTERY_CACHE_LIFETIME, False)
    if content:
        return content

    ps = Popen('pmset -g batt|grep -Eo "\d+%"', shell=True, stdout=PIPE)
    battery = int(ps.communicate()[0][:-2].decode("utf-8"))
    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: battery
    }
    battery_cache = cache_dict

    return battery



def _fetch_powermetrics():
    global powermetrics_cache
    logger.info('_fetch_powermetrics: called')

    if powermetrics_cache:
        logger.info('_fetch_powermetrics: checking memory cache')

    content = cache.content(powermetrics_cache, config.MONITOR_POWERMETRICS_CACHE_LIFETIME, False)
    if content:
        return content

    sudo_password = config.MONITOR_POWERMETRICS_PASSWORD
    command = 'sudo powermetrics -i 200 -n1 --samplers smc'
    command = command.split()

    cmd1 = Popen(['echo', sudo_password], stdout=PIPE)
    cmd2 = Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=PIPE)

    output = cmd2.stdout.read().decode()
    lines = output.split('\n')

    results = {}
    for line in lines:
        for index, key in enumerate([config.MONITOR_POWERMETRICS_FAN_KEY, config.MONITOR_POWERMETRICS_CPU_TEMP_KEY, config.MONITOR_POWERMETRICS_GPU_TEMP_KEY]):
            if line.startswith(key):
                value = line.split(key)[1]
                if index == 0:
                    value = str(floor(float(value.split(' ')[0]))) + ' RPM'
                else:
                    celsius = float(value.split(' ')[0])
                    value = str(int((celsius * 9/5) + 32)) + ' F'
                results[key] = value
    
    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: results
    }
    powermetrics_cache = cache_dict
    return results

def is_mac_pro():
    logger.info('is_mac_pro: called')
    hmm = "system_profiler SPHardwareDataType | grep 'Model Name' | awk -F ': ' '{print $2}'"
    result = run(hmm, stdout=PIPE, shell=True)
    mac_pro = b"Mac Pro" in result.stdout
    logger.info('is_mac_pro: result: {}'.format(mac_pro))
    return mac_pro

def invalidate_memory_cache():
    logger.info('invalidate_memory_cache: called')

    global battery_cache, powermetrics_cache, memory_cache
    battery_cache = None
    powermetrics_cache = None
    memory_cache = None