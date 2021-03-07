# Python

import socket
import requests

with open('top-50-websites.txt', 'r') as wf:
    websites = wf.readlines()

with open('top-50-urls2.txt', 'w') as uf:

    for a in websites:
        a = a[:-1]
        print(f'checking {a}')
        try:
            x = requests.get(f'http://{a}').url
            uf.write(f'{x}\n')
        except:
            pass
