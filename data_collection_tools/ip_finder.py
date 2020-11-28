# Python 3.8

import subprocess
import shlex


class IPFinder:

    def __init__(self, _main_ip, _main_domain):
        self.ip = _main_ip
        self.domain = _main_domain

    def collect(self):
        ips = [self.ip]

        cmd = f'host {self.domain}'

        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode('utf-8').split("\n")
        print(out)
        return ips
