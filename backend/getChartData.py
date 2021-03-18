#!/usr/bin/python3
import argparse
import json

from accesspoint import get_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daysback', type=int, nargs='?', help='number of days to get')
    args = parser.parse_args()

    if args.daysback:
        print('{"data":', json.dumps(get_data(args.daysback)), '}', sep='')
    else:
        print('{"data":', json.dumps(get_data()), '}', sep='')
