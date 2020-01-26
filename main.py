import argparse, requests, threading
from flask import Flask, render_template, request

import config

import components.applescript as applescript
import components.weather as weather
import components.launch_app as launch_app
import components.logging as logging

import background.displays as displays

app = Flask(__name__)

@app.route('/')
def template_home():
    return render_template('today.html')

# weather.fetch()

def _configure_for_connected_display():
    displays.configure_for_connected_display()
    threading.Timer(5.0, _configure_for_connected_display).start()

logger = logging.setup_logger(
    'heartbeat', config.LOGGING_DATA_PATH + '/heartbeat.log')

def _heartbeat():
    logger.info('beat')
    threading.Timer(5.0, _heartbeat).start()
    

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    # _configure_for_connected_display()

    parser = argparse.ArgumentParser(description='Today at Me')
    # parser.add_argument('-is', action="store_true", dest='ICLOUD_REQUIRES_SETUP', default=config.ICLOUD_REQUIRES_SETUP)
    # parser.add_argument('-lp', action="store_true", dest='LOCATION_PROCESSING_ONLY_MODE', default=True)
    args = parser.parse_args()
    
    _configure_for_connected_display()
    print('done')