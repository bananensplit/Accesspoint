#!/usr/bin/python3
import sys
import subprocess

def start_hostapd():
    command =  'sudo ip link set wlan0 up ; sudo systemctl start hostapd'
    command =  'sudo systemctl start hostapd'
    process = subprocess.run(command.split(' '))
    return process.returncode

def stop_hostapd():
    command =  'sudo systemctl stop hostapd ; sudo ip link set wlan0 down'
    command =  'sudo systemctl stop hostapd'
    process = subprocess.run(command.split(' '))
    return process.returncode


if int(sys.argv[1]) == 1:
    print(start_hostapd())
elif int(sys.argv[1]) == 0:
    print(stop_hostapd())