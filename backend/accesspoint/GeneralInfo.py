#!/usr/bin/python3
import re
import subprocess


class GeneralInfo:
    def __init__(self):
        self._status_ap = ''
        self._runtime_rp = 0
        self._runtime_ap = 0
        self._clients_count = 0

        self.update_general_info()

    @property
    def status_ap(self):
        return self._status_ap

    @property
    def runtime_rp(self):
        return self._runtime_rp

    @property
    def runtime_ap(self):
        return self._runtime_ap

    @property
    def clients_count(self):
        return self._clients_count

    def __get_status_ap(self):
        command = 'systemctl is-active hostapd'
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        match = re.match(".*?(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}).*?",
                         process.stdout.read().decode('ascii').replace('\n', ''))
        self._status_ap = match.group(1)

    def __get_runtime_rp(self):
        command = 'uptime -s'
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._runtime_rp = process.stdout.read().decode('ascii').replace('\n', '')

    def __get_runtime_ap(self):
        command = 'systemctl show hostapd --property=ActiveEnterTimestamp --value'
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._runtime_ap = process.stdout.read().decode('ascii').replace('\n', '').replace(' CET', '')

    def __get_clients(self):
        command = 'iw dev wlan0 station dump | grep Station | wc -l'.split(' | ')
        iw = subprocess.Popen(command[0].split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        grep = subprocess.Popen(command[1].split(' '), stdin=iw.stdout, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        wc = subprocess.Popen(command[2].split(' '), stdin=grep.stdout, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        self._clients_count = int(wc.stdout.read().decode('ascii').replace('\n', ''))

    def update_general_info(self):
        self.__get_status_ap()
        self.__get_runtime_rp()
        self.__get_runtime_ap()
        self.__get_clients()

    def get_as_dict(self):
        return {
            'status': self._status_ap,
            'runtime': {
                'pi': self._runtime_rp,
                'AP': self._runtime_ap
            },
            'clients': self._clients_count
        }


if __name__ == '__main__':
    asdasd = GeneralInfo()
    print(asdasd.get_as_dict())
