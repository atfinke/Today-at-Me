import csv, os, threading
from pathlib import Path

from components import icloud, logging
import config

Path(config.BACKGROUND_TASKS_DATA_PATH).mkdir(parents=True, exist_ok=True)
logger = logging.setup_logger(
    'location-processing', config.LOCATION_PROCESSING_LOGGING_PATH)

def start():
    logger.info('start: called')
    if not os.path.exists(config.LOCATION_PROCESSING_CSV_PATH):
        logger.info('start: creating new csv')
        try:
            with open(config.LOCATION_PROCESSING_CSV_PATH, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(
                    ['timestamp', 'battery-level', 'latitiude', 'longitude'])
        except:
            logger.error('start: failed to create csv')
            return
    else:
        logger.info('start: csv exists')
    __fetch()
    threading.Timer(config.LOCATION_PROCESSING_REFRESH_INTERVAL, __fetch).start()


def __fetch():
    logger.info('__fetch: called')
    devices = icloud.fetch_devices()
    device = None
    for d in devices:
        if d[config.ICLOUD_DEVICE_NAME_KEY] == config.LOCATION_PROCESSING_DEVICE_NAME:
            device = d
            break

    if device is None or config.ICLOUD_DEVICE_TIME_KEY not in device:
        logger.info('__fetch: no device')
        return
    else:
        logger.info('__fetch: found device')

    last_timestamp = None
    try:
        with open(config.LOCATION_PROCESSING_CSV_PATH, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                last_timestamp = row[0]
    except:
        logger.error('__fetch: failed to read from csv')
        return

    if last_timestamp == device[config.ICLOUD_DEVICE_TIME_KEY]:
        logger.info('__fetch: same timestamp as csv {}'.format(last_timestamp))
        return
    else:
        logger.info('__fetch: diff timestamp from csv')

    try:
        with open(config.LOCATION_PROCESSING_CSV_PATH, 'a+', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([device[config.ICLOUD_DEVICE_TIME_KEY], device[config.ICLOUD_DEVICE_BATTERY_KEY],
                                 device[config.ICLOUD_DEVICE_LAT_KEY], device[config.ICLOUD_DEVICE_LON_KEY]])
    except:
        logger.error('__fetch: failed to write to csv')
    logger.info('__fetch: saved to csv')
