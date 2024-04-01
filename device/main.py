#!/usr/bin/env python3

import sys
import time
import constants
from upload import upload_data
from db import insert_points
from gps import get_gps_position
from utils import LockableObject, RepeatedTimer, blink_led
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
    blink_led("PWR", 10, 0.1)

    if not check_network_is_up(constants.INTERFACE):
        print("Network is not available, maybe run setup script? Exiting...")
        blink_led("PWR", 2, 0.5)
        blink_led("ACT", 2, 0.5)
        sys.exit(1)

    print("Starting...")

    _ = RepeatedTimer(10, upload_and_insert_data)

    while True:
        time.sleep(3)
        result = ping(constants.INTERFACE, constants.PING_ADDRESS)
        if result is None:
            print("Ping failed, skipping this attempt")
            blink_led("PWR", 2, 0.5)
            continue

        gpsinfo = get_gps_position()
        if gpsinfo.success:
            result.gpsinfo = gpsinfo
        else:
            print("GPS failed, skipping this attempt")
            blink_led("PWR", 2, 0.5)
            continue

        print(result)

        blink_led("ACT", 1, 0.5)
        ping_results.value.append(result)
