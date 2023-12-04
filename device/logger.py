#!/usr/bin/env python3

from operator import itemgetter
import RPi.GPIO as GPIO
import subprocess
import datetime
import sqlite3
import netifaces
import time
import sys
import re
import os
import sys
from gps import get_gps_position, GPSPosition

QMICLI_GET_INFO = "/usr/local/bin/qmicli-get-info"
INTERFACE = "wwan0"
PING_ADDRESS = "8.8.8.8"
DB_LOCATION = "/usr/local/share/ping_results.db"
LED_PIN = 17

# Database setup
db_connection = sqlite3.connect(DB_LOCATION)
cursor = db_connection.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS results (
    timestamp DATETIME,
    ip_address TEXT,
    latency REAL,
    rssi REAL,
    packet_dropped INTEGER,
    latitude REAL,
    longitude REAL
)
"""
)


def extract_qmi_values(text):
    pattern = r"(\w+):\s'(-?\d+\.?\d* dBm?)'"
    matches = re.findall(pattern, text)
    return {key: value for key, value in matches}


def extract_ping_details(ping_output):
    # Regex to match an IP address
    ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

    # Regex to match a hostname
    hostname_regex = r"PING\s+(\S+)"

    # Regex to match latency value (time)
    latency_regex = r"time=(\d+\.?\d*)\s*ms"

    # Find the IP address in the output
    ip_address_match = re.search(ip_regex, ping_output)
    ip_address = ip_address_match.group(0) if ip_address_match else None

    # Find the hostname in the output
    hostname_match = re.search(hostname_regex, ping_output)
    hostname = hostname_match.group(1) if hostname_match else None

    # Find the latency in the output
    latency_match = re.search(latency_regex, ping_output)
    latency = float(latency_match.group(1)) if latency_match else None

    # Determine if the packet was dropped
    packet_dropped = 1 if latency is None else 0

    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "latency": latency,
        "packet_dropped": packet_dropped,
    }


def ping_and_save(interface):
    try:
        ping_output = subprocess.check_output(
            ["ping", "-c", "1", "-I", interface, PING_ADDRESS], stderr=subprocess.STDOUT
        )
        qmi_output = subprocess.check_output(
            [QMICLI_GET_INFO], stderr=subprocess.STDOUT
        )
        ping_result = ping_output.decode("utf-8")
        qmi_result = qmi_output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Got error {e}: exiting")
        sys.exit(1)

    hostname, ip_address, latency, packet_dropped = itemgetter(
        "hostname", "ip_address", "latency", "packet_dropped"
    )(extract_ping_details(ping_result))

    rssi = itemgetter("RSSI")(extract_qmi_values(qmi_result))

    gpsinfo = get_gps_position()

    # Inserting result into database
    cursor.execute(
        "INSERT INTO results (timestamp, ip_address, latency, rssi, packet_dropped, latitude, longitude) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)",
        (
            ip_address,
            latency,
            rssi,
            packet_dropped,
            gpsinfo.latitude,
            gpsinfo.longitude,
        ),
    )
    db_connection.commit()

    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW)

    print(
        f"PING RESULTS: {ip_address}@{datetime.datetime.now()}: {latency} milliseconds, was packet dropped? {packet_dropped}. RSSI: {rssi}. Taken at {gpsinfo.latitude}, {gpsinfo.longitude}"
    )


def check_network_is_up():
    # Check if interface exists
    if not os.path.exists(f"/sys/class/net/{INTERFACE}"):
        print("Interface does not exist")
        return False

    # Check if interface is up (only administrative; does not check if there is a connection)
    with open(f"/sys/class/net/{INTERFACE}/flags", "r") as f:
        flags = f.read()
        if int(flags, base=16) & 1 == 0:
            print("Interface is down")
            return False

    # Check if interface has *a* IP address assigned to it
    try:
        ip_address = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]["addr"]
    except KeyError:
        print("No IP address assigned to interface")
        return False

    # Final check: ping cloudflare to see if we have a connection
    try:
        subprocess.check_output(["ping", "-c", "1", PING_ADDRESS, "-I", INTERFACE])
    except subprocess.CalledProcessError:
        print(f"Could not ping {PING_ADDRESS}")
        return False

    return True


if __name__ == "__main__":
    if not check_network_is_up():
        print("Network is not available, maybe run setup script? Exiting...")
        sys.exit(1)

    print("Starting...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    while True:
        ping_and_save(INTERFACE)
        time.sleep(3)

# Don't forget to close the database connection when you're done
db_connection.close()
