import random
from datetime import datetime, timedelta
from dateutil import tz

import components.spotify as spotify
import components.calendar as calendar
import components.google as google
import components.logging as logging

from configuration import config

def build_header_now_playing_column_inner_html():
    template = '''
    <div id="now-playing-metadata" data-track-uri="{track_uri}" data-playlist-uri="{playlist_uri}">
        <div id="now-playing-playlist">{playlist_name}</div>
        <div id="now-playing-song">{track_name}</div>
    </div>
    <div id="now-playing-image-container">
        <div id="now-playing-image-overlay" onclick="spotifyPlaylistRemoveButtonClicked()">
            <img id="now-playing-image" data-destination="{destination}" src="/spotify/now_playing.jpeg" />
        </div>
    </div>
    '''

    tn, turi, pn, puri = spotify.now_playing_info()
    if tn == None:
        tn = 'Not Playing'
    if pn == None:
        pn = '-'
    return template.format(track_uri= turi, playlist_uri=puri, playlist_name=pn, track_name=tn, destination=random.randint(1, 100_000_000))

def build_spotify_add_to_playlist_inner_html():
    template = '''
    <div id="spotify-add-to-playlist" class="container-single-row">
        <select id="spotify-playlist-selection" onchange="spotifyPlaylistSelectionChanged()">
            {options}
        </select>
        <div id="spotify-playlist-selection-button" onclick="spotifyPlaylistAddButtonClicked()">ADD</div>
    </div>
    '''

    playlists = spotify.all_playlists()
    if len(playlists) == 0:
        return None

    option_template = '<option value="{uri}">{name}</option>\n'
    options_html = ''
    for playlist in playlists:
        options_html += option_template.format(uri=playlist['uri'], name=playlist['name'])
    return template.format(options=options_html)

def build_theatre_component():
    events = calendar.fetch_events()['A.Theatre']
    return _build_calendar_component('A.THEATRE', events, 'static', 'single-date-day')

def build_life_nu_component():
    events = calendar.fetch_events()
    all_events = events['Life'] + events['NU'] + events['andrewfinke2021@u.northwestern.edu']
    all_events = sorted(all_events, key = lambda i: i['start']) 

    now = datetime.today()
    events_two_weeks = []
    for event in all_events:
        event_start = datetime.fromtimestamp(event['start'])
        if (event_start - now).days < 14:
            events_two_weeks.append(event)

    return _build_calendar_component('LIFE + NU', events_two_weeks, 'static', 'single-date-day')

def build_homework_component():
    events = google.fetch_homework()
    events = sorted(events, key = lambda i: i['start'])

    now = datetime.today()
    events_week = []
    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if (event_start - now).days < 7:
            events_week.append(event)

    return _build_calendar_component('UPCOMING ASSIGNMENTS', events_week, 'static', 'single-date-day')

def _build_calendar_component(name, events, data_type, date_format):
    template = '''
     <div class="component-container">
        <div class="component-container-title">{name}</div>
        <div class="component-container-tableview">
            {inner_html}
        </div>
    </div>
    '''
    
    event_template = '''
    <div class="component-container-tableview-row">
        <div class="component-container-tableview-row-title">
            {title}
        </div>
        <div class="component-container-tableview-row-detail"
            data-type="{data_type}" data-start-date="{start_date}"
            data-end-date="{end_date}" data-date-format="{date_format}">
            12:50 - 12:00 PM
        </div>
    </div>

    '''

    if len(events) == 0:
        return None

    inner_html = ''
    for event in events:
        inner_html += event_template.format(title=event['name'], start_date=event['start'], end_date=event['end'], data_type=data_type, date_format=date_format)
    return template.format(name=name, inner_html=inner_html)


def build_classes_component():
    events_today = []
    events = calendar.fetch_events()['NU Classes']

    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if event_start.date() == datetime.today().date():
            events_today.append(event)
    
    return _build_calendar_component('CLASSES', events_today, 'countdown', 'hour-range')

def build_office_hours_component():
    events_today = []
    events = calendar.fetch_events()['NU OH']

    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if event_start.date() == datetime.today().date():
            event['name'] = event['name'].replace(': OH', '')
            events_today.append(event)
    
    return _build_calendar_component('OFFICE HOURS', events_today, 'countdown', 'hour-range')

def build_l4a_component():
    events = calendar.fetch_events()['L4A']
    return _build_calendar_component('L4A', events, 'static', 'single-date-day')

def build_weather_component_inner_html():
    template = '''
    <div class="container-single-row weather-container" data-latitude="{latitude}" data-longitude="{longitude}" data-api-key="{API_KEY}">
        <div class="container-single-row-title"></div>
        <div class="container-single-row-detail"></div>
    </div>
    '''

    return template.format(latitude=42.045071, longitude=-87.687698, API_KEY=config.WEATHER_API_KEY)