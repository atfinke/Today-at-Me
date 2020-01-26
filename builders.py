import components.spotify as spotify
import components.calendar as calendar
import config

import datetime
from components import logging

from datetime import datetime, timedelta
from dateutil import tz


def build_header_now_playing_column_inner_html():
    template = '''
    <div id="now-playing-metadata" data-track-uri="{track_uri}" data-playlist-uri="{playlist_uri}">
        <div id="now-playing-playlist">{playlist_name}</div>
        <div id="now-playing-song">{track_name}</div>
    </div>
    <div id="now-playing-image-container">
        <div id="now-playing-image-overlay" onclick="spotifyPlaylistRemoveButtonClicked()">
            <img id="now-playing-image" src="/spotify/now_playing.jpeg" />
        </div>
    </div>
    '''

    tn, turi, pn, puri = spotify.now_playing_info()
    return template.format(track_uri= turi, playlist_uri=puri, playlist_name=pn, track_name=tn)

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

def build_theatre_component_inner_html():
    template = '''
    <div class="component-container-tableview-row">
        <div class="component-container-tableview-row-title">
            {title}
        </div>
        <div class="component-container-tableview-row-detail container-row-detail-grey"
            data-type="static" data-start-date="{date}"
            data-date-format="single-date-day"></div>
    </div>

    '''

    events = calendar.fetch_events()['A.Theatre']
    if len(events) == 0:
        return None

    inner_html = ''
    for event in events:
        inner_html += template.format(title=event['name'], date=event['start'])
    return inner_html


def build_classes_component_inner_html():
    template = '''
    <div class="component-container-tableview-row">
        <div class="component-container-tableview-row-title">
            {title}
        </div>
        <div class="component-container-tableview-row-detail"
            data-type="countdown" data-start-date="{start_date}"
            data-end-date="{end_date}" data-date-format="hour-range">
            12:50 - 12:00 PM
        </div>
    </div>

    '''

    events_today = []
    events = calendar.fetch_events()['NU Classes']

    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if event_start.date() == datetime.today().date():
            events_today.append(event)
    

    if len(events_today) == 0:
        return None

    inner_html = ''
    for event in events_today:
        inner_html += template.format(title=event['name'], start_date=event['start'], end_date=event['end'])
    return inner_html
   
def build_weather_component_inner_html():
    template = '''
    <div class="container-single-row weather-container" data-latitude="{latitude}" data-longitude="{longitude}" data-api-key="{API_KEY}">
        <div class="container-single-row-title"></div>
        <div class="container-single-row-detail"></div>
    </div>
    '''

    return template.format(latitude=42.045071, longitude=-87.687698, API_KEY=config.WEATHER_API_KEY)