# Pyhton 3.7

# Imports

import sys
import data_collection_tools


class DataCollectionTool:

    def __init__(self, _ip='', _domain=''):
        self.domain = _domain
        self.ip = _ip

    def collect(self):
        data = dict()
        # here add scripts
        return data

    def present(self, collected_data):
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

    # check amount of parameters
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print_help()
        exit(1)

    # get system parameters
    ip = ""
    domain = ""
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-ip':
            ip = sys.argv[i + 1]
            check_ip(ip)
        elif sys.argv[i] == '-d':
            domain = sys.argv[i + 1]
            check_domain(domain)

    # create DataCollectionTool
    tool = DataCollectionTool()

    # collect data
    d = tool.collect()

    # present collected data
    tool.present(d)
