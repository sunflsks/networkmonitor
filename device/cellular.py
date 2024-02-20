from operator import itemgetter
from pydantic import BaseModel
import RPi.GPIO as GPIO
import subprocess
import datetime
import sqlite3
import constants
import netifaces
import time
import sys
import re
import os
from gps import GPSPosition


class PingResult(BaseModel):
    rssi: int
    gpsinfo: GPSPosition = None  # type: ignore
    hostname: str
    ip_address: str
    latency: int
    packet_dropped: bool
    timestamp: int = 0
    success: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = time.time_ns() // 1000000


def extract_qmi_values(text):
    pattern = r"(\w+):\s'(-?\d+\.?\d* dBm?)'"
    matches = re.findall(pattern, text)
    return {key: value for key, value in matches}


def extract_ping_details(ping_output):
    ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    hostname_regex = r"PING\s+(\S+)"
    latency_regex = r"time=(\d+\.?\d*)\s*ms"

    ip_address_match = re.search(ip_regex, ping_output)
    ip_address = ip_address_match.group(0) if ip_address_match else None

    hostname_match = re.search(hostname_regex, ping_output)
    hostname = hostname_match.group(1) if hostname_match else None

    latency_match = re.search(latency_regex, ping_output)
    latency = float(latency_match.group(1)) if latency_match else None

    packet_dropped = 1 if latency is None else 0

    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "latency": latency,
        "packet_dropped": packet_dropped,
    }


def ping(interface, ip):
    try:
        ping_output = subprocess.check_output(
            ["ping", "-c", "1", "-I", interface, ip], stderr=subprocess.STDOUT
        )
        qmi_output = subprocess.check_output(
            [constants.QMICLI_GET_INFO], stderr=subprocess.STDOUT
        )
        ping_result = ping_output.decode("utf-8")
        qmi_result = qmi_output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Got error {e}: exiting")
        sys.exit(1)

    ping_details = extract_ping_details(ping_result)
    ping_details["rssi"] = int(
        itemgetter("RSSI")(extract_qmi_values(qmi_result)).split(" ")[0]
    )

    return PingResult(**ping_details)


def check_network_is_up(interface):
    # Check if interface exists
    if not os.path.exists(f"/sys/class/net/{interface}"):
        print("Interface does not exist")
        return False

    # Check if interface is up (only administrative; does not check if there is a connection)
    with open(f"/sys/class/net/{interface}/flags", "r") as f:
        flags = f.read()
        if int(flags, base=16) & 1 == 0:
            print("Interface is down")
            return False

    # Check if interface has *a* IP address assigned to it
    try:
        ip_address = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]
    except KeyError:
        print("No IP address assigned to interface")
        return False

    # Final check: ping address to see if we have a connection
    try:
        subprocess.check_output(
            ["ping", "-c", "1", constants.PING_ADDRESS, "-I", interface]
        )
    except subprocess.CalledProcessError:
        print(f"Could not ping {constants.PING_ADDRESS}")
        return False

    return True
