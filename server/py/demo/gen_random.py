#!/usr/bin/env python3

import sqlite3
import random

# Database setup
db_connection = sqlite3.connect("ping_results_sample.db")
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


for i in range(1000):
    # Get some random GPS coordinates within the range of 33, -97.2 to 32.5, -96.5
    latitude = random.uniform(32.5, 33)
    longitude = random.uniform(-97.2, -96.5)

    # Generate a random RSSI value between -50 and -100
    rssi = random.randint(-100, -50)

    # Get some random ping values between 0 and 20
    latency = random.uniform(0, 20)

    # Insert the results into the database
    cursor.execute(
        "INSERT INTO results (timestamp, ip_address, latency, rssi, packet_dropped, latitude, longitude) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)",
        ("0.0.0.0", latency, rssi, 0, latitude, longitude),
    )

db_connection.commit()

print("Done bullshitting the database!")
