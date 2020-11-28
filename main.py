# Python 3.8

# Imports

import sys
import socket
import os
from data_collection_tools import ip_finder


class DataCollectionTool:

    def __init__(self, _ip='', _domain=''):
        self.domain = _domain
        self.ip = _ip
        self.data = dict()

        self._complete_data()

    def _complete_data(self):
        if self.domain != "" and self.ip == "":
            self.ip = socket.gethostbyname(self.domain)
        elif self.ip != "" and not self.domain == "":
            self.domain = socket.gethostbyaddr(self.ip)[0]

    def collect(self):
        # get all ip addresses
        self.data['ip-address'] = ip_finder.IPFinder(self.ip, self.domain).collect()

        # get all server types based on ip addresses

        # get the location of all server

        # get all (sub)domains

        pass

    def present(self):
        pass


def print_help():
    print("Inputs couldn't be parsed correctly\nUsage: python main.py -ip [ip-address] -d [domain]")


def check_ip(x):
    v = x.split('.')
    if len(v) != 4:
        print_help()
        exit(1)


def check_domain(x):
    v = x.split('.')
    if len(v) < 2:
        print_help()
        exit(1)


if __name__ == '__main__':

    # User Info
    OUTPUT = True
    if OUTPUT: os.system('clear')

    # check amount of parameters
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print_help()
        exit(1)

    # get system parameters
    _pre_ip = ""
    _pre_domain = ""
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-ip':
            _pre_ip = sys.argv[i + 1]
            check_ip(_pre_ip)
        elif sys.argv[i] in ['-d', '-domain']:
            _pre_domain = sys.argv[i + 1]
            check_domain(_pre_domain)

    # create DataCollectionTool
    if OUTPUT: print(f'[ dct ] Create DataCollectionTool')
    tool = DataCollectionTool(_pre_ip, _pre_domain)

    # complete ip and domain

    # collect data
    if OUTPUT: print(f'[ dct ] Collecting data based on: \n\t[  ip  ]\t{_pre_ip if _pre_ip != "" else "-"}\n\t[domain]\t{_pre_domain if _pre_domain != "" else "-"}')
    tool.collect()

    # present collected data
    if OUTPUT: print(f'[ dct ] Present the collected data')
    tool.present()
