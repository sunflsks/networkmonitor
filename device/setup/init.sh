#!/usr/bin/env bash

if [ $UID -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

mmcli -m 0 --enable
mmcli -m 0 --simple-connect="apn=TFDATA"
udhcpc -q -f -i wwan0
