from ics import Calendar
import requests
import arrow
import json
import time
import config

from components import logging

logger = logging.setup_logger(
    'theatre', config.THEATRE_LOGGING_PATH)


def fetch_events():
    logger.info('fetch_events: called')

    existing_cache = _fetch_cache_events()
    if existing_cache:
        date = existing_cache[config.THEATRE_EVENT_DATE_KEY]
        if int(time.time()) < date + config.THEATRE_CACHE_LIFETIME:
            logger.info('fetch_events: using cache')
            return existing_cache[config.THEATRE_EVENTS_KEY]

    c = Calendar(requests.get(config.THEATRE_API_URL).text)

    upcoming_events = list(c.timeline.start_after(arrow.utcnow()))
    logger.info('fetch_events: found {} upcoming events'.format(
        len(upcoming_events)))

    json_events = []
    for upcoming_event in upcoming_events:
        event = {}
        event[config.THEATRE_EVENT_NAME_KEY] = upcoming_event.name
        event[config.THEATRE_EVENT_DATE_KEY] = upcoming_event.begin.to(
            'local').format('M/D h:mm a')
        json_events.append(event)

    cache_json = {
        config.THEATRE_EVENT_DATE_KEY: int(time.time()),
        config.THEATRE_EVENTS_KEY: json_events
    }
    dumped_json = json.dumps(cache_json)
    _cache_events(dumped_json)
    return json_events


def _fetch_cache_events():
    logger.info('_fetch_cache_events: called')
    return {}


def _cache_events(json):
    logger.info('_cache_events: called')
    print(json)
