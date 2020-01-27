import json
import objc

from datetime import datetime, timedelta
from dateutil import tz

from CalendarStore import CalCalendarStore, CalEvent, CalTask
from Cocoa import NSDate

from components import cache, logging
from configuration import config

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
        existing_cache = cache.fetch(config.CALENDAR_CACHE_PATH)

    content = cache.content(existing_cache, config.CALENDAR_CACHE_LIFETIME)
    if content:
        return content


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
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: formatted_results
    }

    cache.save(cache_dict, config.CALENDAR_CACHE_PATH)
    memory_cache = cache_dict

    return formatted_results