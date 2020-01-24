from pyicloud import PyiCloudService

from components import logging
import config

logger = logging.setup_logger(
    'icloud', config.ICLOUD_LOGGING_PATH)

api = PyiCloudService(config.ICLOUD_USERNAME, config.ICLOUD_PASSWORD)


def fetch_devices():
    logger.info('fetch_devices: called')
    my_devices = [d for d in api.devices if d[config.ICLOUD_DEVICE_NAME_KEY].startswith(
        config.ICLOUD_DEVICE_NAME_PREFIX) and d[config.ICLOUD_DEVICE_TYPE_KEY] not in config.ICLOUD_FILTERED_DEVICE_TYPES]
    my_devices = sorted(
        my_devices, key=lambda i: i[config.ICLOUD_DEVICE_NAME_KEY])
    logger.info('fetch_devices: got {} devices'.format(len(my_devices)))

    formatted_devices = []
    for device in my_devices:
        location = device.location()
        formatted_device = {}
        formatted_device[config.ICLOUD_DEVICE_NAME_KEY] = device[config.ICLOUD_DEVICE_NAME_KEY]
        formatted_device[config.ICLOUD_DEVICE_BATTERY_KEY] = device[config.ICLOUD_DEVICE_BATTERY_KEY]
        formatted_device[config.ICLOUD_DEVICE_TYPE_KEY] = device[config.ICLOUD_DEVICE_TYPE_KEY]
        if location:
            formatted_device[config.ICLOUD_DEVICE_LAT_KEY] = location[config.ICLOUD_DEVICE_LAT_KEY]
            formatted_device[config.ICLOUD_DEVICE_LON_KEY] = location[config.ICLOUD_DEVICE_LON_KEY]
            formatted_device[config.ICLOUD_DEVICE_TIME_KEY] = location[config.ICLOUD_DEVICE_TIME_KEY]
        formatted_devices.append(formatted_device)

    return formatted_devices


def setup():
    logger.info('setup: called')

    import click
    import sys
    logger.info("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        logger.info("  %s: %s" % (i, device.get('deviceName',
                                                "SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        logger.error("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        logger.error("Failed to verify verification code")
        sys.exit(1)
