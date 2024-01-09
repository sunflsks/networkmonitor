#!/usr/bin/python
# -*- coding:utf-8 -*-

# credit to waveshare

from os import times
import RPi.GPIO as GPIO
from pydantic import BaseModel

import serial
import time
import re

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


class GPSPosition(BaseModel):
    success: bool = False
    latitude: int
    longitude: int

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
            return GPSPosition(success=False, latitude=0, longitude=0)
        time.sleep(1.5)

def get_gps_position_test() -> GPSPosition:
    return GPSPosition(success=True, latitude=0, longitude=0)

def extract_between_digits(s):
    # Find the first digit
    first_digit_match = re.search(r'\d', s)
    if not first_digit_match:
        return None  # No digits found

    # Find the last digit
    last_digit_match = re.search(r'\d(?=[^\d]*$)', s)
    if not last_digit_match:
        return None  # This shouldn't happen if the first digit is found

    # Extract everything between the first and last digit
    start = first_digit_match.start()
    end = last_digit_match.end()
    return s[start:end]

def parse_gps_position(gps_info):
    # Remove "+CGPSINFO:" and then split the string by comma
    parts = extract_between_digits(gps_info).split(",")

    # Extract latitude and longitude values
    lat_value, lat_direction = parts[0], parts[1]
    lon_value, lon_direction = parts[2], parts[3]

    # Convert to decimal format
    lat_decimal = convert_to_decimal(lat_value, lat_direction, True)
    lon_decimal = convert_to_decimal(lon_value, lon_direction, False)

    return GPSPosition(success=True, latitude=lat_decimal, longitude=lon_decimal)


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
