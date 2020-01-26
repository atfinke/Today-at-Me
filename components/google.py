import io
import json
import pickle
import os.path
from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from html2text import html2text

from components import logging
from configuration import config

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

logger = logging.setup_logger(
    'google', config.GOOGLE_LOGGING_PATH)
creds = None
memory_cache = None

def auth():
    global creds
    logger.info('auth: called')

    if os.path.exists(config.GOOGLE_AUTH_PATH):
        with open(config.GOOGLE_AUTH_PATH, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info('auth: refreshing')
            creds.refresh(Request())
        else:
            logger.info('auth: starting flow')
            flow = InstalledAppFlow.from_client_secrets_file(
                config.GOOGLE_CREDIENTALS_PATH, SCOPES)
            creds = flow.run_local_server()
        with open(config.GOOGLE_AUTH_PATH, 'wb') as token:
            pickle.dump(creds, token)


def fetch_homework():
    global creds, memory_cache
    logger.info('fetch_homework: called')

    existing_cache = memory_cache
    if existing_cache:
        logger.info('fetch_homework: checking memory cache')
    else:
        logger.info('fetch_homework: checking disk cache')
        existing_cache = _fetch_cache_classes()

    if existing_cache:
        date = existing_cache[config.CACHE_DATE_KEY]
        if datetime.now().timestamp() < date + config.GOOGLE_CACHE_LIFETIME:
            logger.info('fetch_homework: using cache')
            return existing_cache[config.GOOGLE_ASSIGNMENTS_KEY]
        else:
            logger.info('fetch_homework: cache too old {}'.format(datetime.now().timestamp() - date))


    service = build('drive', 'v3', credentials=creds)
    request = service.files().export_media(fileId=config.GOOGLE_HOMEWORK_DOC_ID, mimeType='text/html')
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        logger.info("fetch_homework: Download %d%%." % int(status.progress() * 100))

    html = fh.getvalue().decode('UTF-8')
    raw_text = html2text(html)
    classes = raw_text.split('Flow:')[0]

    for key in config.GOOGLE_HOMEWORK_DOC_REPLACEMENT.keys():
        classes = classes.replace(key, config.GOOGLE_HOMEWORK_DOC_REPLACEMENT[key])

    formatted_assignments = []
    classes = classes.split('<class>')[1:]
    for class_str in classes:
        classes_split = class_str.split('\n')
        class_name = classes_split[0]

        
        for raw_assignment in classes_split[1:]:
            raw_assignment = raw_assignment.replace('  * ', '')
            detail_split = raw_assignment.split('] ')
            if len(detail_split) == 2:
                date = detail_split[0][1:]
                date_split = date.split('/')
                date_dt = datetime(2020, int(date_split[0]), int(date_split[1]))
                name = detail_split[1]
                formatted_assignments.append({'name': class_name + ': ' + name, 'start': date_dt.timestamp(), 'end': date_dt.timestamp()})
    
    logger.info('fetch_homework: fetched {} classes'.format(len(formatted_assignments)))

    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.GOOGLE_ASSIGNMENTS_KEY: formatted_assignments
    }
    _cache_classes(cache_dict)
    return formatted_assignments


def _fetch_cache_classes():
    global memory_cache
    logger.info('_fetch_cache_classes: called')
    try:
        with open(config.GOOGLE_CACHE_PATH) as data:
            cache = json.load(data)
            memory_cache = cache
            return cache
    except:
        return None


def _cache_classes(cache_dict):
    global memory_cache
    logger.info('_cache_classes: called')
    memory_cache = cache_dict
    with open(config.GOOGLE_CACHE_PATH, 'w', encoding='utf-8') as data:
        json.dump(cache_dict, data)
