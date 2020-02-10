from configuration import secrets

CACHE_DATE_KEY = 'date'
CACHE_CONTENT_KEY = 'content'
CACHE_EARLY_SERVER_REFRESH_MULTIPLIER = 0.6

CHECK_CACHE_INTERVAL = 120
CHECK_DISPLAY_INTERVAL = 5

TODAY_DATA_PATH = './user-data'
LOGGING_DATA_PATH = TODAY_DATA_PATH + '/logging'
CACHE_DATA_PATH = TODAY_DATA_PATH + '/cache'

DISPLAYS_LOGGING_PATH = LOGGING_DATA_PATH + '/displays.log'

CALENDAR_CACHE_PATH = CACHE_DATA_PATH + '/calendar.json'
CALENDAR_CACHE_LIFETIME = 60 * 10
CALENDAR_LOGGING_PATH = LOGGING_DATA_PATH + '/calendar.log'
CALENDAR_EVENT_NAME_KEY = 'name'
CALENDAR_EVENT_START_DATE_KEY = 'start'
CALENDAR_EVENT_END_DATE_KEY = 'end'
CALENDAR_CALENDARS = ['Life', 'NU', 'NU Classes', 'L4A', 'NU OH', 'A.Theatre', 'andrewfinke2021@u.northwestern.edu']
CALENDAR_LIFE_EVENT_DAY_RANGE = 7

GOOGLE_CACHE_PATH = CACHE_DATA_PATH + '/homework.json'
GOOGLE_CACHE_LIFETIME = 60 * 10
GOOGLE_AUTH_PATH = CACHE_DATA_PATH + '/google_auth'
GOOGLE_CREDIENTALS_PATH = 'configuration/secrets-google-credentials.json'
GOOGLE_LOGGING_PATH = LOGGING_DATA_PATH + '/google.log'
GOOGLE_HOMEWORK_DOC_ID = '1RtAUOrqs8wJgkiYOi4mYyfAiA823Mhcc8X4JWMlf5wk'
GOOGLE_HOMEWORK_DOC_REPLACEMENT = {
    'COMP_SCI 336-0 - Design & Analysis of Algorithms:\n': '<class>CS 336',
    'COMP_SCI 340-0 - Introduction to Networking:\n': '<class>CS 340',
    'COMP_SCI 349-0 - Machine Learning:\n': '<class>CS 349',
    'PHYSICS 136-2 - General Physics Laboratory:\n': '<class>PHYSICS 136',
}

LASTFM_CACHE_PATH = CACHE_DATA_PATH + '/lastfm.json'
LASTFM_CACHE_LIFETIME = 60 * 60 * 1
LASTFM_LOGGING_PATH = LOGGING_DATA_PATH + '/lastfm.log'
LASTFM_USERNAME = 'andrewfinke'
LASTFM_API_KEY = secrets.LASTFM_API_KEY

STOCKS_CACHE_LIFETIME = 10
STOCKS_LOGGING_PATH = LOGGING_DATA_PATH + '/stocks.log'
STOCKS_SYMBOLS = ['AAPL', 'AMZN', 'DIS', 'GOOG', 'MSFT', 'TSLA']

MONITOR_CACHE_LIFETIME = 5
MONITOR_BATTERY_CACHE_LIFETIME = 60 * 5
MONITOR_LOGGING_PATH = LOGGING_DATA_PATH + '/monitor.log'
MONITOR_INFO_KEY = 'info'
MONITOR_CPU_KEY = 'cpu'
MONITOR_MEMORY_KEY = 'mem'
MONITOR_BATTERY_KEY = 'bat'

MONITOR_POWERMETRICS_CACHE_LIFETIME = 20
MONITOR_POWERMETRICS_FAN_KEY = 'Fan: '
MONITOR_POWERMETRICS_CPU_TEMP_KEY = 'CPU die temperature: '
MONITOR_POWERMETRICS_GPU_TEMP_KEY = 'GPU die temperature: '
MONITOR_POWERMETRICS_PASSWORD = secrets.MONITOR_POWERMETRICS_PASSWORD
MONITOR_ORDER = [MONITOR_CPU_KEY, MONITOR_MEMORY_KEY, MONITOR_BATTERY_KEY, MONITOR_POWERMETRICS_CPU_TEMP_KEY, MONITOR_POWERMETRICS_GPU_TEMP_KEY, MONITOR_POWERMETRICS_FAN_KEY]

MONITOR_MAPPING_NAME_KEY = 'name'
MONITOR_MAPPING_ID_KEY = 'id'
MONITOR_MAPPING_PRIORITY_KEY = 'priority'

MONITOR_MAPPING = {
    MONITOR_CPU_KEY: {
        MONITOR_MAPPING_NAME_KEY: 'CPU',
        MONITOR_MAPPING_ID_KEY: 'monitor-cpu',
        MONITOR_MAPPING_PRIORITY_KEY: 1
    },
    MONITOR_MEMORY_KEY: {
        MONITOR_MAPPING_NAME_KEY: 'Memory',
        MONITOR_MAPPING_ID_KEY: 'monitor-mem',
        MONITOR_MAPPING_PRIORITY_KEY: 2
    },
    MONITOR_BATTERY_KEY: {
        MONITOR_MAPPING_NAME_KEY: 'Battery',
        MONITOR_MAPPING_ID_KEY: 'monitor-bat',
        MONITOR_MAPPING_PRIORITY_KEY: 3
    },
    MONITOR_POWERMETRICS_CPU_TEMP_KEY: {
        MONITOR_MAPPING_NAME_KEY: 'CPU Temp',
        MONITOR_MAPPING_ID_KEY: 'monitor-cpu-temp',
        MONITOR_MAPPING_PRIORITY_KEY: 4
    },
    MONITOR_POWERMETRICS_GPU_TEMP_KEY: {
        MONITOR_MAPPING_NAME_KEY: 'GPU Temp',
        MONITOR_MAPPING_ID_KEY: 'monitor-gpu-temp',
        MONITOR_MAPPING_PRIORITY_KEY: 5
    },
    MONITOR_POWERMETRICS_FAN_KEY: {
        MONITOR_MAPPING_NAME_KEY: 'Fan',
        MONITOR_MAPPING_ID_KEY: 'monitor-fan',
        MONITOR_MAPPING_PRIORITY_KEY: 6
    }
}

SPOTIFY_CLIENT_ID = secrets.SPOTIPY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = secrets.SPOTIPY_CLIENT_SECRET
SPOTIFY_USERNAME = 'j3d1_warr10r'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback/'
SPOTIFY_LOGGING_PATH = LOGGING_DATA_PATH + '/spotify.log'
SPOTIFY_IMAGE_PATH = CACHE_DATA_PATH + '/spotify.jpeg'
SPOTIFY_PLAYLISTS_CACHE_PATH = CACHE_DATA_PATH + '/spotify_playlists.json'
SPOTIFY_PLAYLISTS_CACHE_LIFETIME = 60 * 30
SPOTIFY_AUTH_CACHE_PATH = CACHE_DATA_PATH + '/spotify_auth'

THEME_PARKS_CACHE_PATH = CACHE_DATA_PATH + '/theme-parks.json'
THEME_PARKS_CACHE_LIFETIME = 60 * 15
THEME_PARKS_LOGGING_PATH = LOGGING_DATA_PATH + '/theme-parks.log'
THEME_PARKS_DLR_URL = secrets.THEME_PARKS_DLR_URL
THEME_PARKS_WDW_URL = secrets.THEME_PARKS_WDW_URL
THEME_PARKS_MAX_RIDES = 5

WEATHER_API_KEY = secrets.WEATHER_API_KEY
