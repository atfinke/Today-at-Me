import argparse
import requests
import threading
from flask import Flask, render_template, request, jsonify, send_file

import config
import builders

import components.logging as logging
import components.spotify as spotify

import background.displays as displays
import components.calendar as calendar

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
    header_now_playing_column_inner_html = builders.build_header_now_playing_column_inner_html()
    spotify_add_to_playlist_inner_html = builders.build_spotify_add_to_playlist_inner_html()
    classes_component_inner_html = builders.build_classes_component_inner_html()
    theatre_inner_html = builders.build_theatre_component_inner_html()
    weather_inner_html = builders.build_weather_component_inner_html()
    return render_template('today.html', header_now_playing_column_inner_html=header_now_playing_column_inner_html, spotify_add_to_playlist_inner_html=spotify_add_to_playlist_inner_html, classes_component_inner_html=classes_component_inner_html, theatre_inner_html=theatre_inner_html, weather_inner_html=weather_inner_html)


@app.route("/spotify/now_playing", methods=["GET"])
def spotify_now_playing():
    tn, turi, pn, puri = spotify.now_playing_info()
    return jsonify({'tn': tn, 'turi': turi, 'pn': pn, 'puri': puri}), 200

@app.route("/spotify/now_playing.jpeg", methods=["GET"])
def spotify_now_playing_image():
    if spotify.prepare_to_send_image():
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

# weather.fetch()


def _configure_for_connected_display():
    displays.configure_for_connected_display()
    threading.Timer(5.0, _configure_for_connected_display).start()


logger = logging.setup_logger(
    'heartbeat', config.LOGGING_DATA_PATH + '/heartbeat.log')


def _heartbeat():
    logger.info('beat')
    threading.Timer(5.0, _heartbeat).start()

def _prep_caches():
    spotify.all_playlists()
    theatre.fetch_events()
    threading.Timer(60.0, _prep_caches).start()


spotify.auth()
# _prep_caches()

if __name__ == '__main__':
    
    # parser = argparse.ArgumentParser(description='Today at Me')
    # # parser.add_argument('-sa', action="store_true", dest='FORCE_SPOTIFY_AUTH', default=False)
    # # parser.add_argument('-lp', action="store_true", dest='LOCATION_PROCESSING_ONLY_MODE', default=True)
    # args = parser.parse_args()
    

    # # spotify.all_playlist_names()
    # # _configure_for_connected_display()
    # app.run(host='127.0.0.1', port=8080, debug=True)

    print('done')
