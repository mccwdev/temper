#
# Small script to import data from TEMPer sensor and export it to Domoticz
#
# This program needs to be run as root, for instance with crontab
#

import requests
from temper import Temper


# Domoticz settings
DOMOTICZ_HOST = "domoticz"
DOMOTICZ_DEVICE_IDX = 7027  # Fill in your Domoticz device ID
DOMOTICZ_DEVICE_IDX_EXT = 7026  # Device ID for external temperature Sensor
DOMOTICZ_URL = "http://%s:8080" % DOMOTICZ_HOST
TEMP_CORRECTION = 0
TEMP_EXT_CORRECTION = 2
HUM_CORRECTION = 0


def main():
    temper = Temper()
    temper_data = temper.read()

    # for device in temper_data:
    device = temper_data[0]
    temp = device.get('internal temperature')
    temp_ext = device.get('external temperature')
    hum = device.get('internal humidity')
    temp_str = None
    temp_ext_str = None
    if temp and hum:
        temp_str = str(temp+TEMP_CORRECTION) + ';' + str(hum+HUM_CORRECTION) + ';0'
    elif temp:
        temp_str = str(temp+TEMP_CORRECTION)
    if temp_ext:
        temp_ext_str = str(temp_ext+TEMP_EXT_CORRECTION)


    # Update device in Domoticz
    if temp_str:
        url = "%s/json.htm?type=command&param=udevice&idx=%d&nvalue=0&svalue=%s" % \
              (DOMOTICZ_URL, DOMOTICZ_DEVICE_IDX, temp_str)
        print(url)
        resp = requests.get(url)
        print(resp.text)
    else:
        print("Unknown or no response from device %s" % device)

    # Update external temperature device in Domoticz (if available)
    if DOMOTICZ_DEVICE_IDX_EXT and temp_ext_str:
        url = "%s/json.htm?type=command&param=udevice&idx=%d&nvalue=0&svalue=%s" % \
              (DOMOTICZ_URL, DOMOTICZ_DEVICE_IDX_EXT, temp_ext_str)
        print(url)
        resp = requests.get(url)
        print(resp.text)



# Run the main function when the script is executed
if __name__ == "__main__":
    main()
