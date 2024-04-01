# test functions for those that require like volatile external data
from cellular import PingResult
from gps import GPSPosition
import random


def ping_random(_1, _2) -> PingResult:
    return PingResult(
        hostname="example.com",
        ip_address="0.0.0.0",
        latency=int(random.uniform(0, 100)),
        packet_dropped=False,
        rssi=random.randint(-100, 0),
    )


def get_gps_position_random():
    return GPSPosition(success=True, latitude=-100, longitude=100)
