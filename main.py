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

weather.fetch()

def _external_display_checker():
    if displays.isConnectedToExternalDisplay:
        applescript.run_sync('tell application "System Events" to set the autohide of the dock preferences to false')
    else:
        applescript.run_sync('tell application "System Events" to set the autohide of the dock preferences to true')
    threading.Timer(5.0, _external_display_checker).start()


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    # app.run(host='127.0.0.1', port=8080, debug=True)
    # _external_display_checker()
    print(1)