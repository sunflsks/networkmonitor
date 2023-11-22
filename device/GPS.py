#!/usr/bin/python
# -*- coding:utf-8 -*-

# credit to waveshare

from os import times
import RPi.GPIO as GPIO

import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)
ser.flushInput()

power_key = 6
rec_buff = ""
rec_buff2 = ""
time_count = 0


class SerialResponse:
    success = False
    buffer: str = ""

    def __init__(self, success, buffer):
        self.success = success
        self.buffer = buffer


class GPSPosition:
    success = False
    latitude = None
    longitude = None
    altitude = None
    speed = None
    course = None
    timestamp = None

    def __init__(
        self, success, latitude, longitude, altitude, speed, course, timestamp
    ):
        self.success = success
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.course = course
        self.timestamp = timestamp


def send_at(command, back, timeout):
    rec_buff = ""
    ser.write((command + "\r\n").encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != "":
        if back not in rec_buff.decode():
            return SerialResponse(False, rec_buff.decode())
        else:
            return SerialResponse(True, rec_buff.decode())
    else:
        return SerialResponse(False, "none")


def get_gps_position() -> GPSPosition:
    obtaining_lock = True
    answer = 0
    response = send_at("AT+CGPS=1", "OK", 1)
    time.sleep(2)

    while obtaining_lock:
        response = send_at("AT+CGPSINFO", "+CGPSINFO: ", 1)
        if response.success:
            if ",,,,,," in response.buffer:
                print("GPS is not ready yet, will retry in 1 second")
                obtaining_lock = True
                time.sleep(1)
            else:
                return parse_gps_position(response.buffer)

        else:
            print(f"error")
            send_at("AT+CGPS=0", "OK", 1)
            return GPSPosition(False, None, None, None, None, None, None)
        time.sleep(1.5)


def parse_gps_position(gps_info):
    # Remove "+CGPSINFO:" and then split the string by comma
    parts = gps_info.replace("+CGPSINFO: ", "").split(",")

    # Extract latitude and longitude values
    lat_value, lat_direction = parts[0], parts[1]
    lon_value, lon_direction = parts[2], parts[3]

    print(f"{lat_value}, {lon_value}")

    # Convert to decimal format
    lat_decimal = convert_to_decimal(lat_value, lat_direction, True)
    lon_decimal = convert_to_decimal(lon_value, lon_direction, False)

    return GPSPosition(True, lat_decimal, lon_decimal, None, None, None, None)


def convert_to_decimal(value, direction, islat):
    # for some reason there is a random newline. idc why, no longer
    value = value.strip()

    # Divide the string into degrees and minutes
    index = 2 if islat == True else 3
    degrees = int(value[:index])
    minutes = float(value[index:])

    # Convert to decimal
    decimal = degrees + minutes / 60

    # Adjust for South or West coordinates
    if direction in ["S", "W"]:
        decimal *= -1

    return decimal
