#!/usr/bin/env python3

import sys
import time
import constants
from upload import upload_data
from db import insert_points
from gps import get_gps_position
from utils import LockableObject, RepeatedTimer
from cellular import ping, check_network_is_up

ping_results = LockableObject([])


def upload_and_insert_data() -> None:
    with ping_results:
        if ping_results.value == []:
            print("No data to upload.")
            return
        print(ping_results.value)
        upload_data(ping_results.value)
        insert_points(ping_results.value)
        ping_results.value = []


if __name__ == "__main__":
    if not check_network_is_up(constants.INTERFACE):
        print("Network is not available, maybe run setup script? Exiting...")
        sys.exit(1)

    print("Starting...")

    _ = RepeatedTimer(60, upload_and_insert_data)

    while True:
        result = ping(constants.INTERFACE, constants.PING_ADDRESS)

        gpsinfo = get_gps_position()
        if gpsinfo.success:
            result.gpsinfo = gpsinfo
        else:
            print("GPS failed, skipping this attempt")
            result = None

        print(result)

        if result is not None:
            ping_results.value.append(result)
        time.sleep(3)
