import json
import urllib.request
from datetime import datetime

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from components import logging
from configuration import config

logger = logging.setup_logger('spotify', config.SPOTIFY_LOGGING_PATH)
sp = None
last_downloaded_image_url = None
memory_playlists_cache = None
destinations_with_image = []

def auth():
    logger.info('auth: called')

    global sp
    scope = 'user-read-playback-state user-modify-playback-state playlist-modify-public user-read-currently-playing playlist-read-private playlist-modify-private'
    token = util.prompt_for_user_token(config.SPOTIFY_USERNAME, scope, client_id=config.SPOTIFY_CLIENT_ID,
                                       client_secret=config.SPOTIFY_CLIENT_SECRET, redirect_uri=config.SPOTIFY_REDIRECT_URI, cache_path=config.SPOTIFY_AUTH_CACHE_PATH)
    sp = spotipy.Spotify(auth=token)
    logger.info('auth: done')


def now_playing_info():
    global sp
    track = sp.currently_playing()
    if not track:
        return None, None, None, None
    item = track['item']
    all_images = sorted(item['album']['images'], key=lambda k: k['height'])
    for image in all_images:
        if image['height'] >= 300:
            download_now_playing_image_if_needed(image['url'])
            break

    playlist_uri = track['context']['uri']
    playlist_name = sp.playlist(playlist_uri)['name']
    return item['name'], item['uri'], playlist_name, playlist_uri


def download_now_playing_image_if_needed(url):
    global last_downloaded_image_url
    if last_downloaded_image_url == url:
        return

    response = urllib.request.urlopen(url)
    with open(config.SPOTIFY_IMAGE_PATH, 'wb') as file:
        file.write(response.read())

    global destinations_with_image
    destinations_with_image = []
    last_downloaded_image_url = url


def prepare_to_send_image(destination):
    global destinations_with_image
    if destination not in destinations_with_image:
        destinations_with_image.append(destination)
        return True
    else:
        return False


def all_playlists():
    global memory_playlists_cache, sp
    logger.info('all_playlists: called')

    existing_cache = memory_playlists_cache
    if existing_cache:
        logger.info('all_playlists: checking memory cache')
    else:
        logger.info('all_playlists: checking disk cache')
        existing_cache = _fetch_cache_playlists()

    if existing_cache:
        date = existing_cache[config.CACHE_DATE_KEY]
        if datetime.now().timestamp() < date + config.SPOTIFY_PLAYLISTS_CACHE_LIFETIME:
            logger.info('all_playlists: using cache')
            return existing_cache[config.SPOTIFY_PLAYLISTS_KEY]
        else:
            logger.info('all_playlists: cache too old {}'.format(datetime.now().timestamp() - date))

    formatted_playlists = []
    playlists = sp.user_playlists(config.SPOTIFY_USERNAME)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == config.SPOTIFY_USERNAME:
            formatted_playlists.append(
                {'name': playlist['name'], 'uri': playlist['uri']})

    logger.info('all_playlists: got {} playlists'.format(
        len(formatted_playlists)))

    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.SPOTIFY_PLAYLISTS_KEY: formatted_playlists
    }
    _cache_playlists(cache_dict)
    return formatted_playlists


def remove_now_playing_from_current_playlist(now_playing_track_uri, now_playing_playlist_uri):
    logger.info('remove_now_playing_from_current_playlist: called')
    global sp
    _, turi, _, puri = now_playing_info()

    if now_playing_track_uri != turi or now_playing_playlist_uri != puri:
        logger.error(
            'remove_now_playing_from_current_playlist: not playing same track or playlist ')
        return 'not playing same track', 400

    result = sp.user_playlist_remove_all_occurrences_of_tracks(
        config.SPOTIFY_USERNAME, puri, [turi])
    if "snapshot_id" in result:
        sp.next_track()
        return 'Done', 200
    else:
        return 'Error', 500


def add_now_playing_to_playlist(now_playing_uri, playlist_uri):
    logger.info('add_now_playing_to_playlist: called')

    global sp
    _, turi, _, puri = now_playing_info()

    if now_playing_uri != turi:
        logger.error('add_now_playing_to_playlist: not playing same track {} {}'.format(
            now_playing_uri, turi))
        return 'not playing same track', 400

    result = sp.user_playlist_add_tracks(
        config.SPOTIFY_USERNAME, playlist_uri, [turi])
    if "snapshot_id" in result:
        return 'Done', 200
    else:
        return 'Error', 500


def _fetch_cache_playlists():
    global memory_playlists_cache
    logger.info('_fetch_cache_playlists: called')
    try:
        with open(config.SPOTIFY_PLAYLISTS_CACHE_PATH) as data:
            cache = json.load(data)
            memory_playlists_cache = cache_dict
            return cache
    except:
        return None


def _cache_playlists(cache_dict):
    global memory_playlists_cache
    logger.info('_fetch_cache_playlists: called')
    memory_playlists_cache = cache_dict
    with open(config.SPOTIFY_PLAYLISTS_CACHE_PATH, 'w', encoding='utf-8') as data:
        json.dump(cache_dict, data)
