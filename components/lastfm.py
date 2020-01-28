import urllib.request, json 
from datetime import datetime

from components import cache, logging
from configuration import config

logger = logging.setup_logger(
    'lastfm', config.LASTFM_LOGGING_PATH)
memory_cache = None

def fetch_tracks(request_from_server=False):
    global memory_cache
    logger.info('fetch_tracks: called')

    if memory_cache:
        logger.info('fetch_tracks: checking memory cache')
    else:
        logger.info('fetch_tracks: checking disk cache')
        memory_cache = cache.fetch(config.LASTFM_CACHE_PATH)

    content = cache.content(memory_cache, config.LASTFM_CACHE_LIFETIME, request_from_server)
    if content:
        return content

    formatted_tracks = []
    endpoint = 'https://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&period=7day&format=json&limit=5&user=' + config.LASTFM_USERNAME + '&api_key=' + config.LASTFM_API_KEY 
    with urllib.request.urlopen(endpoint) as url:
        tracks = json.loads(url.read().decode())['toptracks']['track']
        for track in tracks:
            formatted_tracks.append({'name': track['name'], 'count': track['playcount'], 'artist': track['artist']['name']})
    
    memory_cache = cache.save(formatted_tracks, config.LASTFM_CACHE_PATH)
    return formatted_tracks

def invalidate_memory_cache():
    logger.info('invalidate_memory_cache: called')

    global memory_cache
    memory_cache = None