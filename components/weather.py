from pprint import pprint
import requests

import config

def fetch():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(config.WEATHER_CURRENT_CITY, config.WEATHER_API_KEY))
    pprint(r.json())