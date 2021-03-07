# Python

from typosquatting import URLGenerator
from webcomp import Comparer

import requests
import sys
import os
import os.path as path


def _help():
    print()
    print(f'Usage: python3 main.py <domain>')
    print(f'The argument must be a domain. More precisely google.com instead of https://google.com')
    exit(0)


if __name__ == '__main__':

    # get command line inputs
    if len(sys.argv[1:]) != 1:
        _help()

    # URLs
    target_domain = sys.argv[1]
    try:
        target_url = requests.get(f'http://{target_domain}').url
    except Exception as e:
        _help()

    # generate possible malicious domains
    generator = URLGenerator.Generator()
    typo_domains = generator.generate(target_domain, 1)
    
    # append protocol
    typo_urls = []
    connection_error_log = []
    for domain in typo_domains:
        try:
            r = requests.get(f'http://{domain}')
            typo_urls.append(r.url)
        except Exception as e:
            connection_error_log.append((domain, e))

    # compare urls
    scores = []
    comparer = Comparer.Comparer()
    _LOGGING = True

    if _LOGGING:
        # if not already exist: create directory logs
        if not path.exists('logs'):
            os.system('mkdir logs')

        # if not already exist: create directory logs/<target_domain>
        if not path.exists(f'logs/{target_domain}'):
            os.system(f'mkdir logs/{target_domain}')

    for url in typo_urls:
        comparer.set_parameter(target_url, url)
        if _LOGGING:
            comparer.enable_logging(f'logs/{target_domain}/')
        achieved_points, max_points = comparer.compare_websites()
        print(f'{achieved_points} / {max_points} for comparing {target_url} with {url}')
        scores.append((url, achieved_points, max_points))

    # print results into file: ./logs/<target-domain>/results.txt
    with open(f'logs/{target_domain}/results.txt', 'w') as result_file:
        for url, score, max_score in scores:
            result_file.write(f'{score} / {max_score} for [ {url} ]\n')
