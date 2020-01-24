
import requests, threading
from pathlib import Path
from flask import Flask, render_template, request

import config

import components.applescript as applescript
import components.weather as weather
import components.icloud as icloud
import components.launch_app as launch_app

import background.displays as displays
import background.location_processing as location_processing

Path(config.LOGGING_DATA_PATH).mkdir(parents=True, exist_ok=True)
Path(config.BACKGROUND_TASKS_DATA_PATH).mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

@app.route('/')
def template_home():
    return render_template('home.html')

# weather.fetch()
# icloud.fetch_my_devices()


def _configure_for_connected_display():
    displays.configure_for_connected_display()
    threading.Timer(5.0, _configure_for_connected_display).start()


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    # app.run(host='127.0.0.1', port=8080, debug=True)
    # _configure_for_connected_display()
    

    if config.LOCATION_PROCESSING_ONLY_MODE:
        location_processing.start()
    print(1)