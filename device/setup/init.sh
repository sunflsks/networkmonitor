#!/usr/bin/env bash

if [ $UID -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

echo none > /sys/class/leds/ACT/trigger

MODEM_PATH=$(mmcli --list-modems | awk '{print $1}')

mmcli -m "$MODEM_PATH" --enable
mmcli -m "$MODEM_PATH" --simple-connect="apn=TFDATA"
udhcpc -q -f -i wwan0
