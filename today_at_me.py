import requests
import os
import threading
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.serving import WSGIRequestHandler

import components.logging as logging
import components.spotify as spotify
import components.calendar as calendar
import components.google as google
import components.monitor as monitor
import components.lastfm as lastfm
import components.builders as builders
import components.theme_parks as theme_parks
import components.stocks as stocks

import background.displays as displays

from configuration import config

WSGIRequestHandler.protocol_version = "HTTP/1.1"
app = Flask(__name__)

@app.route('/')
def today():
    header_now_playing_column_inner_html = builders.build_header_now_playing_column_inner_html()
    spotify_add_to_playlist_html = builders.build_spotify_add_to_playlist_html()
    life_component_html = builders.build_life_component()
    l4a_component_html = builders.build_l4a_component()
    lastfm_component_html = builders.build_lastfm_component()
    theme_park_component_html = builders.build_theme_park_component()
    stocks_component_html = builders.build_stocks_component()
    monitor_component_html = builders.build_monitor_component()
    weather_component_html = builders.build_weather_component_html()
    
    return render_template('today.html',
                           header_now_playing_column_inner_html=header_now_playing_column_inner_html,
                           spotify_add_to_playlist_html=spotify_add_to_playlist_html,
                           life_component_html=life_component_html,
                           l4a_component_html=l4a_component_html,
                           lastfm_component_html=lastfm_component_html,
                           theme_park_component_html=theme_park_component_html,
                           stocks_component_html=stocks_component_html,
                           monitor_component_html=monitor_component_html,
                           weather_component_html=weather_component_html)


@app.route("/clear_cache", methods=["POST"])
def clear_cache():
    os.remove(config.CALENDAR_CACHE_PATH)
    os.remove(config.GOOGLE_CACHE_PATH)
    os.remove(config.LASTFM_CACHE_PATH)
    os.remove(config.SPOTIFY_PLAYLISTS_CACHE_PATH)
    os.remove(config.THEME_PARKS_CACHE_PATH)

    calendar.invalidate_memory_cache()
    google.invalidate_memory_cache()
    lastfm.invalidate_memory_cache()
    spotify.invalidate_memory_cache()
    theme_parks.invalidate_memory_cache()
    monitor.invalidate_memory_cache()
    return 'DONE', 200


@app.route("/monitor/now", methods=["GET"])
def monitor_now():
    return jsonify(monitor.fetch_stats()), 200


@app.route("/stocks/now", methods=["GET"])
def stocks_now():
    return jsonify(stocks.fetch_stocks()), 200


@app.route("/spotify/now_playing", methods=["GET"])
def spotify_now_playing():
    tn, turi, pn, puri = spotify.now_playing_info()
    return jsonify({'tn': tn, 'turi': turi, 'pn': pn, 'puri': puri}), 200


@app.route("/spotify/now_playing.jpeg", methods=["GET"])
def spotify_now_playing_image():
    destination = request.args.get('destination')
    if spotify.prepare_to_send_image(destination):
        return send_file(config.SPOTIFY_IMAGE_PATH, mimetype='image/jpeg')
    else:
        return "Unchanged", 304


@app.route("/spotify/add_track", methods=["POST"])
def spotify_add_track():
    now_playing_track_uri = request.args.get('now_playing_track_uri')
    selected_playlist_uri = request.args.get('selected_playlist_uri')
    return spotify.add_now_playing_to_playlist(now_playing_track_uri, selected_playlist_uri)


@app.route("/spotify/remove_track", methods=["POST"])
def spotify_remove_track():
    now_playing_track_uri = request.args.get('now_playing_track_uri')
    now_playing_playlist_uri = request.args.get('now_playing_playlist_uri')
    return spotify.remove_now_playing_from_current_playlist(now_playing_track_uri, now_playing_playlist_uri)

@app.route("/spotify/remove_now_playing_track", methods=["POST"])
def spotify_remove_now_playing_track():
    _, turi, _, puri = spotify.now_playing_info()
    return spotify.remove_now_playing_from_current_playlist(turi, puri)


@app.route("/spotify/play_track", methods=["POST"])
def spotify_play_track():
    track_name = request.args.get('track_name')
    artist = request.args.get('artist')
    return spotify.play_track(track_name, artist)


def _configure_for_connected_display():
    displays.configure_for_connected_display()

    display_thread = threading.Timer(
        config.CHECK_DISPLAY_INTERVAL, _configure_for_connected_display)
    display_thread.name = "display check"
    display_thread.daemon = True
    display_thread.start()


def _prep_fast_fetch_caches():
    spotify.fetch_playlists(request_from_server=True)
    lastfm.fetch_tracks(request_from_server=True)
    theme_parks.fetch_wait_times(request_from_server=True)

    fast_fetch_cache_thread = threading.Timer(config.CHECK_CACHE_INTERVAL, _prep_fast_fetch_caches)
    fast_fetch_cache_thread.name = "fast cache"
    fast_fetch_cache_thread.daemon = True
    fast_fetch_cache_thread.start()


def _prep_slow_fetch_caches():
    calendar.fetch_events(request_from_server=True)
    google.fetch_homework(request_from_server=True)

    slow_fetch_cache_thread = threading.Timer(config.CHECK_CACHE_INTERVAL / 2, _prep_slow_fetch_caches)
    slow_fetch_cache_thread.name = "slow cache"
    slow_fetch_cache_thread.daemon = True
    slow_fetch_cache_thread.start()

def _prep_one_off_inits():
    _ = monitor.fetch_stats()
    _ = stocks.fetch_stocks()
    _ = spotify.now_playing_info()

_prep_one_off_inits()
_prep_slow_fetch_caches()
_prep_fast_fetch_caches()

if __name__ == '__main__':
    if not monitor.is_mac_pro():
        _configure_for_connected_display()

    app.run(host='127.0.0.1', port=8080, debug=False)
    print('DONE')
