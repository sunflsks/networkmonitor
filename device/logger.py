#!/usr/bin/env python3

import sys
import time
from utils import LockableObject, RepeatedTimer, generate_random_ping
from upload import upload_data
from cellular import ping, check_network_is_up, PingResult, extract_qmi_values

INTERFACE = "wwan0"
PING_ADDRESS = "8.8.8.8"

ping_results = LockableObject([])

if __name__ == "__main__":
    if not check_network_is_up(INTERFACE):
        print("Network is not available, maybe run setup script? Exiting...")
        sys.exit(1)

    print("Starting...")

    _ = RepeatedTimer(60, upload_data, ping_results)

    while True:
        result = ping(INTERFACE, PING_ADDRESS)
        with ping_results:
            print(result)
            ping_results.value.append(result)
        time.sleep(3)

        print(ping_results.value)