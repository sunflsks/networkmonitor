#!/usr/bin/env python3

from operator import itemgetter
import subprocess
import datetime
import sqlite3
import time
import sys
import re

QMICLI_GET_INFO = "/usr/local/bin/qmicli-get-info"

# Database setup
db_connection = sqlite3.connect("ping_results.db")
cursor = db_connection.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS results (
    timestamp DATETIME,
    ip_address TEXT,
    latency REAL,
    packet_dropped INTEGER
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
        # Replace 'google.com' with your target
        ping_output = subprocess.check_output(
            ["ping", "-c", "1", "-I", interface, "google.com"], stderr=subprocess.STDOUT
        )
        qmi_output = subprocess.check_output(
            ["./qmicli_get_info"], stderr=subprocess.STDOUT
        )
        ping_result = ping_output.decode("utf-8")
        qmi_result = qmi_output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        sys.exit(1)

    hostname, ip_address, latency, packet_dropped = itemgetter(
        "hostname", "ip_address", "latency", "packet_dropped"
    )(extract_ping_details(ping_result))

    rssi = itemgetter("RSSI")(extract_qmi_values(qmi_result))

    # Inserting result into database
    cursor.execute(
        "INSERT INTO results (timestamp, ip_address, latency, packet_dropped) VALUES (CURRENT_TIMESTAMP, ?, ?, ?)",
        (ip_address, latency, packet_dropped),
    )
    db_connection.commit()

    print(
        f"PING RESULTS: {ip_address}@{datetime.datetime.now()}: {latency} milliseconds, was packet dropped? {packet_dropped}. RSSI: {rssi}"
    )


if __name__ == "__main__":
    interface = "wwan0"  # Replace with your network interface
    while True:
        ping_and_save(interface)
        time.sleep(5)

# Don't forget to close the database connection when you're done
db_connection.close()
