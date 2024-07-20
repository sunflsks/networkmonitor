## This project has both a server and a device component (the code structure is indicative of this)

Device:
- Written in Python and is designed to run on a Raspberry Pi with an attached modem accessible through ModemManager. 
- Continuously polls the modem for the current network strength, location, and other relevant data and upload it to the server

Server
- Written in Node.js and is designed to run on any Unix-like machine with a Postgres db running. 
- Collects, collates, and presents it to the user using OpenStreetMap and Leaflet.

# TODO:

## DEVICE
SWITCH TO MODEMMANAGER, WILL PROBABLY BE WAY EASIER TO MANAGE (Done!)

## SERVER
- Optimization- different colors for each provider (Done)
- Toggle layers (Done)
- Postgres? (Done)
- See if thread immediately quits if cannot upload? if so, fix! (Done)
- Switch to using PostGIS instead of dealing with the coordinates directly
- **BIG: consolidate points so the client doesn't download every single datapoint in a given window**

## NOTES

- When soldering modem to rpi, make sure that you solder on the BOTTOM, where the pogo pins come into contact with the pi. (basically making new pads for 5v and GND GPIO pins). don't try to solder through the top, it won't work
