# Python 3.8

import subprocess
import shlex


# return a list of pairs (subdomain, [all_ips_of_that_domain])
def get_all_ips(subdomain_list):
    ip_addresses = []

    for subdomain in subdomain_list:
        ips = _get_ip(subdomain)
        ip_addresses.append((subdomain, ips))

    return ip_addresses


# returns list of all ips that can be found for a given domain
def _get_ip(domain):
    ips = []
    cmd = f'host {domain}'
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    out, err = proc.communicate()
    out = out.decode('utf-8').split("\n")
    return ips
