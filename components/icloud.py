from pyicloud import PyiCloudService
from pprint import pprint
import config

api = PyiCloudService(config.ICLOUD_USERNAME, config.ICLOUD_PASSWORD)


def fetch_devices():
    my_devices = [d for d in api.devices if d[config.ICLOUD_DEVICE_NAME_KEY].startswith(
        config.ICLOUD_DEVICE_NAME_PREFIX) and d[config.ICLOUD_DEVICE_TYPE_KEY] not in config.ICLOUD_FILTERED_DEVICE_TYPES]
    my_devices = sorted(
        my_devices, key=lambda i: i[config.ICLOUD_DEVICE_NAME_KEY])

    formatted_devices = []
    for device in my_devices:
        location = device.location()
        formatted_device = {}
        formatted_device[config.ICLOUD_DEVICE_NAME_KEY] = device[config.ICLOUD_DEVICE_NAME_KEY]
        formatted_device[config.ICLOUD_DEVICE_BATTERY_KEY] = device[config.ICLOUD_DEVICE_BATTERY_KEY]
        formatted_device[config.ICLOUD_DEVICE_TYPE_KEY] = device[config.ICLOUD_DEVICE_TYPE_KEY]
        formatted_device[config.ICLOUD_DEVICE_LAT_KEY] = location[config.ICLOUD_DEVICE_LAT_KEY]
        formatted_device[config.ICLOUD_DEVICE_LON_KEY] = location[config.ICLOUD_DEVICE_LON_KEY]
        formatted_devices.append(formatted_device)

    pprint(formatted_devices)


def setup():
    import click
    import sys
    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print("  %s: %s" % (i, device.get('deviceName',
                                          "SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)


# def fetch_events(calendar_name):
#     calendar_api = api.calendar
#     calendars = calendar_api.calendars()
#     calender = None
#     for c in calendars:
#         if c['title'] == calendar_name:
#             calender = c
#             break

#     if not calender:
#         raise SystemError('no calendar with name {}'.format(calendar_name))
