from typing import List
import sqlite3
from cellular import PingResult
from utils import LockableObject
import constants


def insert_points(results: List[PingResult]) -> None:
    if results == []:
        print("No data to insert into local DB.")
        return

    conn = sqlite3.connect(constants.SQLITE_DB_PATH)
    c = conn.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS results (timestamp DATETIME, ip_address TEXT, latency REAL, rssi REAL, packet_dropped INTEGER, latitude REAL, longitude REAL)"
    )
    for result in results:
        c.execute(
            "INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                result.timestamp,
                result.ip_address,
                result.latency,
                result.rssi,
                result.packet_dropped,
                result.gpsinfo.latitude,
                result.gpsinfo.longitude,
            ),
        )

    conn.commit()
    conn.close()
