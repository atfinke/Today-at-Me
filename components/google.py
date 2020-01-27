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

from components import cache, logging
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
            creds = flow.run_console()
        with open(config.GOOGLE_AUTH_PATH, 'wb') as token:
            pickle.dump(creds, token)


def fetch_homework():
    auth()

    global creds, memory_cache
    logger.info('fetch_homework: called')

    existing_cache = memory_cache
    if existing_cache:
        logger.info('fetch_homework: checking memory cache')
    else:
        logger.info('fetch_homework: checking disk cache')
        existing_cache = cache.fetch(config.GOOGLE_CACHE_PATH)

    content = cache.content(existing_cache, config.GOOGLE_CACHE_LIFETIME)
    if content:
        return content

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
        config.CACHE_CONTENT_KEY: formatted_assignments
    }
    cache.save(cache_dict, config.GOOGLE_CACHE_PATH)
    memory_cache = cache_dict

    return formatted_assignments

def invalidate_memory_cache():
    global memory_cache
    memory_cache = None