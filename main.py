import logging
import requests
from flask import Flask, render_template, request

import components.applescript as applescript
import components.displays as displays
import components.weather as weather
import components.icloud as icloud

import threading

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
    _configure_for_connected_display()
    print(1)