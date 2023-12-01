#!/usr/bin/env bash
# Script for first-time setup
if [ $UID -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# HARDWARE PREREQUISITES:
# SIM installed, modem connected (THRU USB, NOT USB->UART)

USBPATH="/dev/ttyUSB2"

apt install socat

# First, completely disable ModemManager, as it conflicts with qmicli
systemctl unmask ModemManager.service
systemctl disable ModemManager.service

# First, completely reset modem to factory settings
echo "AT&F" | socat - "$USBPATH"
sleep 5
# Set CUSBPIDSWITCH to 9001,1,1 to make modem expose itself over QMI
echo "AT+CUSBPIDSWITCH=9001,1,1" | socat - "$USBPATH"
sleep 5

# Set COPS to 0; should auto-detect and connect to Home
echo "AT+COPS=0" | socat - "$USBPATH"
sleep 5

# Set GPS to be enabled on startup
echo "AT+CGPSAUTO=1" | socat - "$USBPATH"
sleep 5
