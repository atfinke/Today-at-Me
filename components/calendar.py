import objc

from CalendarStore import CalCalendarStore, CalEvent, CalTask
from Cocoa import NSDate

from datetime import datetime, timedelta
from dateutil import tz

import json
import time
import config

from components import logging

logger = logging.setup_logger(
    'calendar', config.CALENDAR_LOGGING_PATH)

memory_cache = None

def fetch_events():
    global memory_cache

    logger.info('fetch_events: called')

    existing_cache = memory_cache
    if existing_cache:
        logger.info('fetch_events: checking memory cache')
    else:
        logger.info('fetch_events: checking disk cache')
        existing_cache = _fetch_cache_events()

    if existing_cache:
        date = existing_cache[config.CACHE_DATE_KEY]
        if int(time.time()) < date + config.CALENDAR_CACHE_LIFETIME:
            logger.info('fetch_events: using cache')
            return existing_cache[config.CALENDAR_CALENDARS_KEY]
        else:
            logger.info('fetch_events: cache too old {}'.format(int(time.time()) - date))


    store = CalCalendarStore.defaultCalendarStore()
    cals = []
    for cal in store.calendars():
        if cal.title() in config.CALENDAR_CALENDARS:
            cals.append(cal)
        logger.info(cal.title())

    cst = tz.gettz('America/Chicago')
    today = datetime.utcnow().date()
    start_dt = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc()).astimezone(cst)
    end_dt = start_dt + timedelta(30)

    start_int = int(start_dt.strftime("%s"))
    end_int = int(end_dt.strftime("%s"))
    start = NSDate.dateWithTimeIntervalSince1970_(start_int)
    end = NSDate.dateWithTimeIntervalSince1970_(end_int)

    formatted_results = {}

    for cal in cals:
        events = []
        pred = CalCalendarStore.eventPredicateWithStartDate_endDate_calendars_(start, end, [cal])
        for event in store.eventsWithPredicate_(pred):
            s = event._.startDate.timeIntervalSince1970()
            e = event._.endDate.timeIntervalSince1970()
            events.append({'name': event._.title, 'start': s, 'end': e})
        formatted_results[cal.title()] = events

    cache_dict = {
        config.CACHE_DATE_KEY: int(time.time()),
        config.CALENDAR_CALENDARS_KEY: formatted_results
    }
    _cache_events(cache_dict)
    return formatted_results


def _fetch_cache_events():
    global memory_cache
    logger.info('_fetch_cache_events: called')
    try:
        with open(config.CALENDAR_CACHE_PATH) as data:
            cache = json.load(data)
            memory_cache = cache
            return cache
    except:
        return None


def _cache_events(cache_dict):
    global memory_cache
    logger.info('_cache_events: called')
    memory_cache = cache_dict
    with open(config.CALENDAR_CACHE_PATH, 'w', encoding='utf-8') as data:
        json.dump(cache_dict, data)
