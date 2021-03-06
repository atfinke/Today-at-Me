import json
import urllib.request
from datetime import datetime

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from components import cache, logging
from configuration import config

logger = logging.setup_logger('spotify', config.SPOTIFY_LOGGING_PATH)
sp = None
last_downloaded_image_url = None
memory_playlists_cache = None
destinations_with_image = []
playlist_uri_to_name = {}

def auth():
    logger.info('auth: called')

    global sp
    scope = 'user-read-playback-state user-modify-playback-state playlist-modify-public user-read-currently-playing playlist-read-private playlist-modify-private user-top-read'
    token = util.prompt_for_user_token(config.SPOTIFY_USERNAME, scope, client_id=config.SPOTIFY_CLIENT_ID,
                                       client_secret=config.SPOTIFY_CLIENT_SECRET, redirect_uri=config.SPOTIFY_REDIRECT_URI, cache_path=config.SPOTIFY_AUTH_CACHE_PATH)
    sp = spotipy.Spotify(auth=token)
    logger.info('auth: done')


def now_playing_info():
    auth()
    global sp, playlist_uri_to_name
    try:
        track = sp.currently_playing()
        if not track:
            return None, None, None, None
    except:
        return None, None, None, None

    item = track['item']
    all_images = sorted(item['album']['images'], key=lambda k: k['height'])
    for image in all_images:
        if image['height'] >= 300:
            download_now_playing_image_if_needed(image['url'])
            break

    playlist_uri = None
    playlist_name = '-'

    if 'context' in track and track['context'] and 'uri' in track['context'] and 'type' in track['context'] and track['context']['type'] == 'playlist':
        playlist_uri = track['context']['uri']
        if playlist_uri in playlist_uri_to_name:
            playlist_name = playlist_uri_to_name[playlist_uri]
        else:
            result = sp.playlist(playlist_uri)
            if 'name' in result:
                playlist_name = result['name']
                playlist_uri_to_name[playlist_uri] = playlist_name
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


def fetch_playlists(request_from_server=False):
    auth()

    global memory_playlists_cache, sp
    logger.info('fetch_playlists: called')

    if memory_playlists_cache:
        logger.info('fetch_playlists: checking memory cache')
    else:
        logger.info('fetch_playlists: checking disk cache')
        memory_playlists_cache = cache.fetch(config.SPOTIFY_PLAYLISTS_CACHE_PATH)

    content = cache.content(memory_playlists_cache, config.SPOTIFY_PLAYLISTS_CACHE_LIFETIME, request_from_server)
    if content:
        return content

    try:
        formatted_playlists = []
        playlists = sp.user_playlists(config.SPOTIFY_USERNAME)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == config.SPOTIFY_USERNAME:
                formatted_playlists.append(
                    {'name': playlist['name'], 'uri': playlist['uri']})

        logger.info('fetch_playlists: got {} playlists'.format(
            len(formatted_playlists)))

        memory_playlists_cache = cache.save(formatted_playlists, config.SPOTIFY_PLAYLISTS_CACHE_PATH)
        return formatted_playlists
    except:
        return []


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
    _, turi, _, _ = now_playing_info()

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


def play_track(track, artist):
    global sp
    logger.info('play_track: called')
    result = sp.search(q="artist:{} track:{}".format(artist, track), type="track", limit=1)
    if 'tracks' in result:
        logger.info('got tracks result')
        item = result['tracks']['items'][0]['uri']
        sp.start_playback(uris=[item])
        return 'Done', 200
    else:
        logger.info('no tracks result')
        return 'Error', 500


def invalidate_memory_cache():
    logger.info('invalidate_memory_cache: called')

    global memory_playlists_cache
    memory_playlists_cache = None
