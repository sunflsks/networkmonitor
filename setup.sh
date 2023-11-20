#!/bin/sh

sudo /usr/bin/qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=TFDATA" --client-no-release-cid
sudo ip link set dev wwan0 up
sudo udhcpc -q -f -i wwan0
