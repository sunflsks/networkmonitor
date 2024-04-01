#!/usr/bin/env python3

import sqlite3
import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Function to parse and format timestamp
def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')

# Function to extract and convert RSSI to integer
def convert_rssi(rssi_str):
    # Extract the numeric part and convert to integer
    return int(rssi_str.split()[0])

# Function to transform data
def transform_data(row):
    formatted_timestamp = format_timestamp(row[0])
    rssi = row[3]
    # Convert packet_dropped to boolean
    packet_dropped = row[4] == 1
    # Convert latitude and longitude to point
    coordinates = f"({row[5]}, {row[6]})"
    return (formatted_timestamp,) + row[1:3] + (row[3],) + (packet_dropped, coordinates)


# Connect to SQLite database
sqlite_conn = sqlite3.connect('db.db')
cursor = sqlite_conn.cursor()

# Fetch data from SQLite database
cursor.execute("SELECT timestamp, ip_address, latency, rssi, packet_dropped, latitude, longitude FROM results")
sqlite_data = cursor.fetchall()

# Close the SQLite connection
sqlite_conn.close()

# Transform data
sqlite_data = [x for x in sqlite_data if x[5]]
transformed_data = [transform_data(row) for row in sqlite_data]

# Connect to PostgreSQL database
postgres_conn = psycopg2.connect(
    dbname="networkmonitor",
    user="postgres",
    password="postgres"
)
postgres_cursor = postgres_conn.cursor()

# Insert data into PostgreSQL database
insert_query = sql.SQL("""
    INSERT INTO results (timestamp, ip_address, latency, rssi, packet_dropped, coordinates)
    VALUES (%s, %s, %s, %s, %s, %s)
""")
postgres_cursor.executemany(insert_query, transformed_data)

# Commit changes and close the PostgreSQL connection
postgres_conn.commit()
postgres_cursor.close()
postgres_conn.close()

print("Data migration completed successfully.")
