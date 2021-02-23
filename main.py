# Python

from typosquatting import gen_URL
from webcomp import compare

import requests
import sys
import os
import os.path as path


def _help():
    pass


if __name__ == '__main__':

    # get command line inputs
    if len(sys.argv[1:]) != 1:
        _help()

    # URLs
    target_domain = sys.argv[1]
    target_url = requests.get(f'http://{target_domain}').url

    # generate possible malicious domains
    typo_domains = gen_URL.main(target_domain)

    # append protocol
    typo_urls = []
    connection_error_log = []
    for domain in typo_domains[:2]:
        try:
            r = requests.get(f'http://{domain}')
            typo_urls.append(r.url)
        except Exception as e:
            connection_error_log.append((domain, e))

    # if not already exist: create directory logs
    if not path.exists('logs'):
        os.system('mkdir logs')

    # compare urls
    scores = []
    for url in typo_urls:
        print(f'Comparing: {target_url} with {url}')
        scores.append((url, compare.main(target_url, url, _LOGGING=True)))

    # print results into file: ./logs/results.txt
    with open('./logs/results.txt', 'w') as result_file:
        for url, score in scores:
            result_file.write(f'[ Similarity Score ] {score} / 11.0\t[ URL ] {url}\n')
