#!/usr/bin/python
# -*- coding:utf-8 -*-

# credit to waveshare

from os import times
from constants import MMCLI_WRAPPER
from utils import blink_led, get_modem_path
import RPi.GPIO as GPIO
from pydantic import BaseModel

import serial
import time
import re
import subprocess

class GPSPosition(BaseModel):
    success: bool = False
    latitude: float = False
    longitude: float = False

def get_gps_position() -> GPSPosition:  # type: ignore
    path = get_modem_path()

    if path == "":
        return GPSPosition()

    try:
        result = subprocess.run(
            [MMCLI_WRAPPER, path, "gps"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        output = result.stdout

        if "latitude: " not in output or "longitude: " not in output:
            return GPSPosition()

        output_cleaned = [x.strip(' |-') for x in output.splitlines()]
        gpsposition = GPSPosition()

        for x in output_cleaned:
            if x.startswith("latitude: "):
                gpsposition.latitude = float(x.replace("latitude: ", "").strip())

            if x.startswith("longitude: "):
                gpsposition.longitude = float(x.replace("longitude: ", "").strip())

        gpsposition.success=True
        return gpsposition

    except subprocess.CalledProcessError as e:
        print(f"Error running mmcli command: {e}")

    return GPSPosition(success=False)
