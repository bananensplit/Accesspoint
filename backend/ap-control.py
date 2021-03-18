#!/usr/bin/python3
import argparse
import sys
import subprocess


def start_hostapd():
    command = 'sudo systemctl start hostapd'
    process = subprocess.run(command.split(' '))
    return process.returncode


def stop_hostapd():
    command = 'sudo systemctl stop hostapd'
    process = subprocess.run(command.split(' '))
    return process.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--start', help='start the accesspoint', action='store_true')
    group.add_argument('--stop', help='stop the accesspoint', action='store_true')
    args = parser.parse_args()

    if args.start:
        # print('start')
        print(start_hostapd())
    elif args.stop:
        # print('stop')
        print(stop_hostapd())
    else:
        parser.print_help(sys.stdout)
