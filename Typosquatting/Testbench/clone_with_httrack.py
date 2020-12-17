# Python3.8

import os

# get url
url = input('[ url ] ')

# extract url
domain = url.split('https://')[1].split('/')[0]

# use httrack for copying the url
os.system(f'httrack {url} -O httrack_{domain}')