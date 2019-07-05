#
# Small script to import data from TEMPer sensor and export it to Domoticz
#
# This program needs to be run as root, for instance with crontab
#

import requests
from temper import Temper


# Domoticz settings
DOMOTICZ_HOST = "domoticz"
DOMOTICZ_DEVICE_IDX = 6505  # Fill in your Domoticz device ID
DOMOTICZ_URL = "http://%s:8080" % DOMOTICZ_HOST
TEMP_CORRECTION = -1.8
HUM_CORRECTION = 0
DEVICE_ID = 0

def main():
    temper = Temper()
    temper_data = temper.read()

    # for device in temper_data:
    device = temper_data[DEVICE_ID]
    #from pprint import pprint; pprint(temper_data)
    temp = device['internal temperature']
    hum = 0
    try:
        hum = device['internal humidity']
    except:
        pass
    temp_hum = str(temp+TEMP_CORRECTION) + ';' + str(hum+HUM_CORRECTION) + ';0'

    # Update device in Domoticz
    url = "%s/json.htm?type=command&param=udevice&idx=%d&nvalue=0&svalue=%s" % \
          (DOMOTICZ_URL, DOMOTICZ_DEVICE_IDX, temp_hum)
    print(url)
    resp = requests.get(url)
    print(resp.text)


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
