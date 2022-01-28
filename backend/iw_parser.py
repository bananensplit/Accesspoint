import re
from functools import cache

import pandas as pd


def parse_station_dump(output):
    lines = output.strip("\n").split("\n")
    mac_address = re.search(r'([0-9a-fA-F]:?){12}', lines[0]).group()

    lines = [re.sub(r"\s", "", line) for line in lines[1:]]
    lines = [line.split(":") for line in lines]
    lines = {line[0]: line[1] for line in lines}

    return {
        'mac': mac_address,
        'vendor': get_vendor_name(mac_address),
        'rx-bitrate': lines["rxbitrate"],
        'tx-bitrate': lines["txbitrate"],
        'connected-time': lines["connectedtime"][:-7],
    }


@cache
def get_mac_addresses(file="resources/mac_addresses_28-01-2022.csv"):
    return pd.read_csv(file, sep=";", encoding_errors='ignore')


@cache
def get_vendor_name(mac_address):
    """
        mac_address format: 
            AA-BB-CC-DD-EE-FF
            AA:BB:CC:DD:EE:FF
    """
    macs = get_mac_addresses()
    mac = re.sub(r"[-:]", "", mac_address)[0:6].upper()
    erg = macs.loc[macs["Assignment"] == mac, "Organization Name"].values
    return None if len(erg) >= 0 else erg[0]
