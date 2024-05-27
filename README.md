# TODO:

## DEVICE
SWITCH TO MODEMMANAGER, WILL PROBABLY BE WAY EASIER TO MANAGE

sudo systemctl start ModemManager
sudo mmcli -m 0 --enable
mmcli -m 0 --simple-connect="apn=TFDATA"

get modemmanager running on startup
see if modemmanager setup needs to be run once or on each startup
get running with NetworkManager as well, so udhcpcd does not need to be run on each startup

## SERVER
optimization- different colors for each provider
- toggle layers
- mongodb?
- see if thread immediately quits if cannot upload? if so, fix!


## NOTES
- when soldering modem to rpi, make sure that you solder on the BOTTOM, where the pogo pins come into contact with the pi. (basically making new pads for 5v and GND GPIO pins). don't try to solder through the top, it won't work
