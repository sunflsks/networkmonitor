#!/usr/bin/env python3

import sys
import time
import constants
from upload import upload_data
from gps import get_gps_position
from utils import LockableObject, RepeatedTimer
from cellular import ping, check_network_is_up

ping_results = LockableObject([])

if __name__ == "__main__":
    if not check_network_is_up(constants.INTERFACE):
        print("Network is not available, maybe run setup script? Exiting...")
        sys.exit(1)

    print("Starting...")

    _ = RepeatedTimer(60, upload_data, ping_results)

    while True:
        result = ping(constants.INTERFACE, constants.PING_ADDRESS)
        with ping_results:
            print(result)

        gpsinfo = get_gps_position()
        if gpsinfo.success:
            result.gpsinfo = gpsinfo
        else:
            print("GPS failed, skipping this attempt")
            result = None

        if result is not None:
            ping_results.value.append(result)
        time.sleep(3)
