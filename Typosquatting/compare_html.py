# Python 3.7

import sys
import requests
import copy


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


def _compare(url1, url2, threshold):
    suspicious = False

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

    value = float((same1 + same2) / (len(psl1) + len(psl2)))

    if value >= threshold:
        suspicious = True

    return suspicious, value


if __name__ == '__main__':
    _THRESHOLD = 0.2
    u1 = sys.argv[1]
    u2 = sys.argv[2]

    sus, val = _compare(u1, u2, _THRESHOLD)
    print(f'{val:.2} >= {_THRESHOLD} --> Suspicious' if val else f'{val} < {_THRESHOLD} --> Not suspicious')
