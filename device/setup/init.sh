#!/usr/bin/env bash

if [ $UID -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

sleep 15

echo none > /sys/class/leds/ACT/trigger
echo none > /sys/class/leds/PWR/trigger

MODEM_PATH=$(mmcli --list-modems | awk '{print $1}')

mmcli -m "$MODEM_PATH" --enable
mmcli -m "$MODEM_PATH" --simple-connect="apn=TFDATA"
mmcli -m "$MODEM_PATH" --location-enable-gps-raw --location-enable-gps-nmea --location-enable-agps-msb
mmcli -m "$MODEM_PATH" --signal-setup=5
udhcpc -q -f -i wwan0
