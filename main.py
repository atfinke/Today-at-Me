import argparse
import requests
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

import background.displays as displays

from configuration import config

WSGIRequestHandler.protocol_version = "HTTP/1.1"
app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def today():
    return render_template('today.html', 
    header_now_playing_column_inner_html=builders.build_header_now_playing_column_inner_html(), 
    spotify_add_to_playlist_inner_html=builders.build_spotify_add_to_playlist_inner_html(), 
    classes_component_html=builders.build_classes_component(), 
    office_hours_component_html=builders.build_office_hours_component(),
    life_nu_component_html=builders.build_life_nu_component(),
    l4a_component_html=builders.build_l4a_component(),
    lastfm_component_html=builders.build_lastfm_component(),
    homework_component_html=builders.build_homework_component(),
    theatre_component_html=builders.build_theatre_component(),
    monitor_component_html=builders.build_monitor_component(),
    weather_inner_html=builders.build_weather_component_inner_html())


@app.route("/monitor/now", methods=["GET"])
def monitor_now():
    return jsonify(monitor.fetch_stats()), 200

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

@app.route("/spotify/play_track", methods=["POST"])
def spotify_play_track():
    track_name = request.args.get('track_name')
    artist = request.args.get('artist')
    return spotify.play_track(track_name, artist)

def _configure_for_connected_display():
    displays.configure_for_connected_display()
    # threading.Timer(5.0, _configure_for_connected_display).start()

def _prep_caches():
    spotify.all_playlists()
    google.fetch_homework()
    calendar.fetch_events()
    lastfm.fetch_tracks()
    # threading.Timer(120.0, _prep_caches).start()

spotify.auth()
google.auth()
_prep_caches()

if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Today at Me')
    # # parser.add_argument('-sa', action="store_true", dest='FORCE_SPOTIFY_AUTH', default=False)
    # # parser.add_argument('-lp', action="store_true", dest='LOCATION_PROCESSING_ONLY_MODE', default=True)
    # args = parser.parse_args()

    # # spotify.all_playlist_names()
    # _configure_for_connected_display()
    app.run(host='127.0.0.1', port=8080, debug=True)
