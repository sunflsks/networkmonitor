#!/bin/bash

if [ $UID -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi
# get rid of me sometime pls
sleep 10
/usr/bin/qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=TFDATA" --client-no-release-cid
ip link set dev wwan0 up
udhcpc -q -f -i wwan0
