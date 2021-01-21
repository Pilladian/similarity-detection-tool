# Python 3.7

import sys
import requests
import copy
from bs4 import BeautifulSoup


def _remove_html(line_list):
    removed_list = []

    for line in line_list:
        brackets = 0
        new_line = ""
        for char in line:
            if char == '<':
                brackets += 1
            elif char == '>':
                brackets -= 1
            elif brackets == 0:
                new_line += char

        test = new_line.split(' ')
        new = []
        for e in test:
            if e != '':
                new.append(e)

        removed_list.append(' '.join(new))

    for e in copy.deepcopy(removed_list):
        if e == '' or e == '\t':
            removed_list.remove(e)

    return removed_list


def _crawl_website(url):
    w = requests.get(url)               # website html
    psb = w.content                     # page source as bytes
    pss = psb.decode()                  # page source as string
    psl = pss.split('\n')               # list of all lines split by '\n'
    ps_rhtml = _remove_html(psl)        # html markup removed

    return ps_rhtml


def _get_components(url):
    cs = url.split('https://')
    cs = ''.join(cs).split('http://')
    cs = ''.join(cs).split('www.')
    cs = ''.join(cs).split('.de')
    cs = ''.join(cs).split('.com')
    cs = ''.join(cs).split('.org')
    cs = ''.join(cs).split('.to')
    cs = ''.join(cs).split('#')[0]
    cs = ''.join(cs).split('/')[0]
    cs = ''.join(cs).split('.')

    return cs


def _compare_domain(url1, url2):
    u1_components = _get_components(url1)
    u2_components = _get_components(url2)

    same1 = 0
    same2 = 0

    for element in u1_components:
        if element in u2_components:
            same1 += 1

    for element in u2_components:
        if element in u1_components:
            same2 += 1

    return float((same1 + same2) / (len(u1_components) + len(u2_components)))


def _compare_content(url1, url2):
    psl1 = _crawl_website(url1)
    psl2 = _crawl_website(url2)
    same1 = 0
    same2 = 0

    for line in psl1:
        if line in psl2:
            same1 += 1

    for line in psl2:
        if line in psl1:
            same2 += 1

    return float((same1 + same2) / (len(psl1) + len(psl2)))


def _get_hrefs(url):
    w = requests.get(url)   # website html
    psb = w.content         # page source as bytes
    pss = psb.decode()      # page source as string

    soup = BeautifulSoup(pss, features="html5lib")
    hrefs = [a['href'] for a in soup.find_all('a', href=True)]

    return hrefs


def _compare_hrefs(url1, url2):

    url1_refs = _get_hrefs(url1)
    url2_refs = _get_hrefs(url2)

    same1 = 0
    same2 = 0

    for element in url1_refs:
        if element in url2_refs:
            same1 += 1

    for element in url2_refs:
        if element in url1_refs:
            same2 += 1

    return float((same1 + same2) / (len(url1_refs) + len(url2_refs)))


def _compare(url1, url2):
    suspicious = False

    # comparing values
    values = [_compare_domain(url1, url2),
              _compare_content(url1, url2),
              _compare_hrefs(url1, url2)]

    return suspicious, values


def _calculate_similarity_score(c, d, h):
    value = 0.0

    # content
    _C_TH = 0.25
    if c >= _C_TH:
        value += 3.0
    elif c >= _C_TH * 0.9:
        value += 2.5
    elif c >= _C_TH * 0.8:
        value += 2.0
    elif c >= _C_TH * 0.6:
        value += 2.0
    elif c >= _C_TH * 0.5:
        value += 1.5
    elif c >= _C_TH * 0.3:
        value += 1.0
    elif c >= _C_TH * 0.2:
        value += 0.5

    # domain
    _D_TH = 0.66
    if d >= _D_TH:
        value += 3.0
    elif d >= _D_TH * 0.9:
        value += 2.5
    elif d >= _D_TH * 0.8:
        value += 2.0
    elif d >= _D_TH * 0.6:
        value += 2.0
    elif d >= _D_TH * 0.5:
        value += 1.5
    elif d >= _D_TH * 0.3:
        value += 1.0
    elif d >= _D_TH * 0.2:
        value += 0.5

    # hrefs
    _H_TH = 0.1
    if h >= _H_TH:
        value += 4.0
    elif h >= _H_TH * 0.9:
        value += 3.5
    elif h >= _H_TH * 0.8:
        value += 3.0
    elif h >= _H_TH * 0.6:
        value += 2.5
    elif h >= _H_TH * 0.5:
        value += 2.0
    elif h >= _H_TH * 0.3:
        value += 1.5
    elif h >= _H_TH * 0.2:
        value += 1.0
    elif h >= _H_TH * 0.1:
        value += 0.5

    return value


if __name__ == '__main__':

    u1 = sys.argv[1]
    u2 = sys.argv[2]

    sus, vals = _compare(u1, u2)

    # calculate final similarity score
    content, domain, hrefs = vals[1], vals[0], vals[2]
    value = _calculate_similarity_score(content, domain, hrefs)

    # output
    print(f'Similarity Scores:')
    print(f'\t[ Content ] {vals[1]*100:.2f}%\n\t[ Domain  ] {vals[0]*100:.2f}%\n\t[  hrefs  ] {vals[2]*100:.2f}%')
    print(f'Final Similarity Score: {value} / 10.0')
