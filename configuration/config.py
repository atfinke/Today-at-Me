from configuration import secrets

CACHE_DATE_KEY = 'date'

TODAY_DATA_PATH = './user-data'
LOGGING_DATA_PATH = TODAY_DATA_PATH + '/logging'
CACHE_DATA_PATH = TODAY_DATA_PATH + '/cache'

DISPLAYS_LOGGING_PATH = LOGGING_DATA_PATH + '/displays.log'

GOOGLE_ASSIGNMENTS_KEY = 'assignments'
GOOGLE_CACHE_PATH = CACHE_DATA_PATH + '/homework.json'
GOOGLE_CACHE_LIFETIME = 120
GOOGLE_AUTH_PATH = CACHE_DATA_PATH + '/google_auth'
GOOGLE_CREDIENTALS_PATH = 'secrets-google-credentials.json'
GOOGLE_LOGGING_PATH = LOGGING_DATA_PATH + '/google.log'
GOOGLE_HOMEWORK_DOC_ID = '1RtAUOrqs8wJgkiYOi4mYyfAiA823Mhcc8X4JWMlf5wk'
GOOGLE_HOMEWORK_DOC_REPLACEMENT = {
    'COMP_SCI 336-0 - Design & Analysis of Algorithms:\n': '<class>CS 336',
    'COMP_SCI 340-0 - Introduction to Networking:\n': '<class>CS 340',
    'COMP_SCI 349-0 - Machine Learning:\n': '<class>CS 349',
    'PHYSICS 136-2 - General Physics Laboratory:\n': '<class>PHYSICS 136',
}

CALENDAR_CACHE_PATH = CACHE_DATA_PATH + '/calendar.json'
CALENDAR_CACHE_LIFETIME = 120
CALENDAR_LOGGING_PATH = LOGGING_DATA_PATH + '/calendar.log'
CALENDAR_CALENDARS_KEY = 'calendars'
CALENDAR_EVENTS_KEY = 'events'
CALENDAR_EVENT_NAME_KEY = 'name'
CALENDAR_EVENT_START_DATE_KEY = 'start'
CALENDAR_EVENT_END_DATE_KEY = 'end'
CALENDAR_CALENDARS = ['Life', 'NU', 'NU Classes', 'L4A', 'NU OH', 'A.Theatre', 'andrewfinke2021@u.northwestern.edu']

SPOTIFY_CLIENT_ID = secrets.SPOTIPY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = secrets.SPOTIPY_CLIENT_SECRET
SPOTIFY_USERNAME = 'j3d1_warr10r'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback/'
SPOTIFY_LOGGING_PATH = LOGGING_DATA_PATH + '/spotify.log'
SPOTIFY_IMAGE_PATH = CACHE_DATA_PATH + '/spotify.jpeg'
SPOTIFY_PLAYLISTS_CACHE_PATH = CACHE_DATA_PATH + '/spotify_playlists.json'
SPOTIFY_PLAYLISTS_KEY = 'playlists'
SPOTIFY_PLAYLISTS_CACHE_LIFETIME = 60
SPOTIFY_AUTH_CACHE_PATH = CACHE_DATA_PATH + '/spotify_auth'

WEATHER_API_KEY = secrets.WEATHER_API_KEY