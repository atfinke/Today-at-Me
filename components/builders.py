import random
from datetime import datetime, timedelta
from dateutil import tz

import components.spotify as spotify
import components.calendar as calendar
import components.google as google
import components.lastfm as lastfm
import components.theme_parks as theme_parks
import components.stocks as stocks
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
        tn = '-'
    if pn == None:
        pn = '-'
    return template.format(track_uri= turi, playlist_uri=puri, playlist_name=pn, track_name=tn, destination=random.randint(1, 100_000_000))

def build_spotify_add_to_playlist_html():
    template = '''
    <div class="component-container">      
        <div id="spotify-add-to-playlist" class="container-single-row">
            <select id="spotify-playlist-selection" onchange="spotifyPlaylistSelectionChanged()">
                {options}
            </select>
            <div id="spotify-playlist-selection-button" onclick="spotifyPlaylistAddButtonClicked()">ADD</div>
        </div>
    </div>
    '''

    playlists = spotify.fetch_playlists()
    if not playlists or len(playlists) == 0:
        return None

    option_template = '<option value="{uri}">{name}</option>\n'
    options_html = ''
    for playlist in playlists:
        options_html += option_template.format(uri=playlist['uri'], name=playlist['name'])
    return template.format(options=options_html)

def build_theatre_component():
    events = calendar.fetch_events()['A.Theatre']
    return _build_calendar_component('A.THEATRE', events, 'static', 'https://www.andrewfinke.com/theatre')

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

    return _build_calendar_component('LIFE + NU', events_two_weeks, 'static', 'iCal://')

def build_homework_component():
    events = google.fetch_homework()
    events = sorted(events, key = lambda i: i['start'])

    if not events or len(events) == 0:
        return None

    now = datetime.today()
    events_week = []
    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if (event_start - now).days <= 7:
            events_week.append(event)

    return _build_calendar_component('UPCOMING ASSIGNMENTS', events_week, 'static', 'single-date-day', 'https://docs.google.com/document/d/1RtAUOrqs8wJgkiYOi4mYyfAiA823Mhcc8X4JWMlf5wk/edit')

def build_lastfm_component():
    template = '''
     <div class="component-container">
        <div class="component-container-title cursor-element" onclick="window.open(\'https://www.last.fm/user/andrewfinke/listening-report/week\',\'_self\')">{name}</div>
        <div class="component-container-tableview">
            {inner_html}
        </div>
    </div>
    '''
    
    track_template = '''
    <div id="{id}" class="component-container-tableview-row cursor-element" data-name="{data_name}" data-artist="{data_artist}" onClick="lastfmRowClicked(this.id)">
        <div class="component-container-tableview-row-title">
            {name}
        </div>
        <div class="component-container-tableview-row-detail container-row-detail-grey-blue">
            {count}
        </div>
    </div>

    '''

    tracks = lastfm.fetch_tracks()
    if not tracks or len(tracks) == 0:
        return None

    inner_html = ''
    for track in tracks:
        id = random.randint(1, 100_000_000)
        inner_html += track_template.format(id=id, name=track['name'], count=track['count'], data_name=track['name'], data_artist=track['artist'])
    return template.format(name='TOP TRACKS LAST WEEK', inner_html=inner_html)

def build_stocks_component():
    template = '''
     <div class="component-container cursor-element" onclick="window.open(\'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#summary',\'_self\')"'>
        <div class="component-container-tableview">
            {inner_html}
        </div>
    </div>
    '''
    
    stock_template = '''
    <div class="component-container-tableview-row">
        <div class="component-container-tableview-row-title">
            {symbol}
        </div>
        <div class="component-container-tableview-row-detail stock-detail" data-symbol="{symbol}"></div>
    </div>

    '''

    fetched_stocks = stocks.fetch_stocks()
    if not fetched_stocks or len(fetched_stocks) == 0:
        return None

    inner_html = ''
    for stock in fetched_stocks:
        inner_html += stock_template.format(symbol=stock['name'])
    return template.format(inner_html=inner_html)

def build_theme_park_component():
    template = '''
     <div class="component-container">
        <div class="component-container-title">{name}</div>
        <div class="component-container-tableview">
            {inner_html}
        </div>
    </div>
    '''
    
    ride_template = '''
    <div class="component-container-tableview-row">
        <div class="component-container-tableview-row-title">
            {name}
        </div>
        <div class="component-container-tableview-row-detail container-row-detail-{color}">
            {time}
        </div>
    </div>

    '''

    rides = theme_parks.fetch_wait_times()
    rides = sorted(rides, key = lambda i: int(i['waitTime']), reverse=True)[:config.THEME_PARKS_MAX_RIDES] 

    if not rides or len(rides) == 0 or int(rides[-1]['waitTime']) == 0:
        return None

    inner_html = ''
    for ride in rides:
        color = 'red' if ride['waitTime'] > 120 else 'grey'
        inner_html += ride_template.format(name=ride['name'], time=ride['waitTime'], color=color)
    return template.format(name='WAIT TIMES', inner_html=inner_html)

def _build_calendar_component(name, events, data_type, link=None, show_today_on_date=False):
    template = '''
     <div class="component-container {cursor_element}" {on_click}>
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
            data-end-date="{end_date}" data-show-today-on-date="{show_today_on_date}">
            12:50 - 12:00 PM
        </div>
    </div>

    '''

    if not events or len(events) == 0:
        return None

    cursor_element = 'cursor-element' if link else ''
    on_click = 'onclick="window.open(\'{}\',\'_self\')"'.format(link) if link else ''
    show_today_on_date_html = 'True' if show_today_on_date else 'False'
  
    inner_html = ''
    for event in events:
        inner_html += event_template.format(title=event['name'], start_date=event['start'], end_date=event['end'], data_type=data_type, show_today_on_date=show_today_on_date_html)
    return template.format(name=name, inner_html=inner_html, cursor_element=cursor_element, on_click=on_click)


def build_monitor_component():
    return '''
     <div class="component-container">
        <div class="component-container-tableview">
            <div class="component-container-tableview-row">
                <div class="component-container-tableview-row-title">CPU</div>
                <div id="monitor-cpu" class="component-container-tableview-row-detail"></div>
            </div>
            <div class="component-container-tableview-row">
                <div class="component-container-tableview-row-title">Memory</div>
                <div id="monitor-memory" class="component-container-tableview-row-detail"></div>
            </div>
            <div class="component-container-tableview-row">
                <div class="component-container-tableview-row-title">Battery</div>
                <div id="monitor-battery" class="component-container-tableview-row-detail"></div>
            </div>
        </div>
    </div>
    '''

def build_classes_component():
    events_today = []
    events = calendar.fetch_events()['NU Classes']

    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if event_start.date() == datetime.today().date():
            events_today.append(event)
    
    return _build_calendar_component('CLASSES', events_today, 'countdown', 'iCal://')

def build_office_hours_component():
    events_today = []
    events = calendar.fetch_events()['NU OH']

    for event in events:
        event_start = datetime.fromtimestamp(event['start'])
        if event_start.date() == datetime.today().date():
            event['name'] = event['name'].replace(': OH', '')
            events_today.append(event)
    
    return _build_calendar_component('OFFICE HOURS', events_today, 'countdown', 'iCal://')

def build_l4a_component():
    events = calendar.fetch_events()['L4A']
    return _build_calendar_component('L4A', events, 'static', 'iCal://')

def build_weather_component_html():
    template = '''
    <div class="component-container">
        <div class="container-single-row weather-container" data-latitude="{latitude}" data-longitude="{longitude}" data-api-key="{API_KEY}">
            <div class="container-single-row-title"></div>
            <div class="container-single-row-detail"></div>
        </div>        
    </div>
    '''

    return template.format(latitude=42.045071, longitude=-87.687698, API_KEY=config.WEATHER_API_KEY)