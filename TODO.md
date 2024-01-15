# DEVICE
SWITCH TO MODEMMANAGER, WILL PROBABLY BE WAY EASIER TO MANAGE

sudo systemctl start ModemManager
sudo mmcli -m 0 --enable
mmcli -m 0 --simple-connect="apn=TFDATA"

get modemmanager running on startup
see if modemmanager setup needs to be run once or on each startup
get running with NetworkManager as well, so udhcpcd does not need to be run on each startup

# SERVER
optimization