#!/usr/bin/python3
import json
import subprocess

def get_hostapd_status():
    command = 'systemctl is-active hostapd'
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process.stdout.read().decode('ascii').replace('\n', '')

def get_runtime():
    command = 'uptime -s'
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process.stdout.read().decode('ascii').replace('\n', '')

def get_runtimeAP():
    command = 'systemctl show hostapd --property=ActiveEnterTimestamp --value'
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process.stdout.read().decode('ascii').replace('\n', '').replace(' CET', '')

def get_clients():
    command = 'iw dev wlan0 station dump | grep Station | wc -l'.split(' | ')
    iw = subprocess.Popen(command[0].split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    grep = subprocess.Popen(command[1].split(' '), stdin=iw.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    wc = subprocess.Popen(command[2].split(' '), stdin=grep.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return int(wc.stdout.read().decode('ascii').replace('\n', ''))


json = json.dumps({'status': get_hostapd_status(), 'runtime': {'pi': get_runtime(), 'AP': get_runtimeAP()}, 'clients': get_clients()})
print(json)
