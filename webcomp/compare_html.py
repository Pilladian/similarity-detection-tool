# Python 3.7

import sys
import requests
import copy
import os
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
    w = requests.get(url)  # website html
    psb = w.content  # page source as bytes
    pss = psb.decode()  # page source as string
    psl = pss.split('\n')  # list of all lines split by '\n'
    ps_rhtml = _remove_html(psl)  # html markup removed

    return ps_rhtml


def _calculate_score(l1, l2):
    same1 = 0
    same2 = 0

    for element in l1:
        if element in l2:
            same1 += 1

    for element in l2:
        if element in l1:
            same2 += 1

    return float((same1 + same2) / (len(l1) + len(l2)))


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

    return _calculate_score(u1_components, u2_components)


def _compare_content(url1, url2):
    psl1 = _crawl_website(url1)
    psl2 = _crawl_website(url2)

    return _calculate_score(psl1, psl2)


def _get_hrefs(url):
    w = requests.get(url)  # website html
    psb = w.content  # page source as bytes
    pss = psb.decode()  # page source as string

    soup = BeautifulSoup(pss, features="html5lib")
    href_list = [a['href'] for a in soup.find_all('a', href=True)]

    return href_list


def _compare_hrefs(url1, url2):
    url1_refs = [a for a in _get_hrefs(url1) if a != '#']
    url2_refs = [a for a in _get_hrefs(url2) if a != '#']

    return _calculate_score(url1_refs, url2_refs)


def _get_image_components(url):
    ol = url.split('/')
    nl = [a for a in ol if a != '']

    return nl


def _get_image_urls(url):
    w = requests.get(url)  # website html
    psb = w.content  # page source as bytes
    pss = psb.decode()  # page source as string

    soup = BeautifulSoup(pss, features="html5lib")
    img_list = [a['src'] for a in soup.find_all('img')]
    img_list = [_get_components(url) + _get_image_components(a) for a in img_list]

    return img_list


def _compare_image_sources(url1, url2):
    image_l1 = _get_image_urls(url1)
    image_l2 = _get_image_urls(url2)

    va = 0.0
    for a in image_l1:
        for b in image_l2:
            va += _calculate_score(a, b)

    try:
        return va / (len(image_l1) * len(image_l2))
    except:
        return 0.0


def _compare(url1, url2):
    # comparing values
    _values = [_compare_content(url1, url2),
               _compare_domain(url1, url2),
               _compare_hrefs(url1, url2),
               _compare_image_sources(url1, url2)]

    return _values


def _calc(val, threshold, max_points, percentage=0.2):
    if val == 0.0:
        return 0.0

    rounds = 0
    for points in range(2 * max_points, -1, -1):
        if val > threshold - (rounds * (threshold * percentage)):
            return float(points / 2)
        rounds += 1

    return 0.0


def _calculate_similarity_score(c, d, h, iu, _C_TH, _D_TH, _H_TH, _IU_TH):
    scores = [(_calc(c, _C_TH, 2), 2.0),
              (_calc(d, _D_TH, 2), 2.0),
              (_calc(h, _H_TH, 3), 3.0),
              (_calc(iu, _IU_TH, 3), 3.0)]

    return scores


def _output(url1, url2, value_list, score_list, threshold_list):
    os.system('clear')
    testcases = ['Content', 'Domain', 'Hrefs', 'Image-Urls']
    print()
    print(f'Check similarity for {url1} and {url2}')
    print()
    print('\tTest\t\tAchieved Score\t Similarity\tThreshold\n')
    for ind in range(len(testcases)):
        print(f'\t{testcases[ind]}'
              f'{" " * (10 - len(testcases[ind]))}\t{score_list[ind][0]} / {score_list[ind][1]}'
              f'\t {value_list[ind]:.2f}'
              f'{" " * (10 - len(str(threshold_list[ind])))}\t{threshold_list[ind]}')

    print()
    print()
    print(f'Final Similarity Score: {sum([a[0] for a in score_list])} / 10.0\n')


if __name__ == '__main__':
    u1 = sys.argv[1]
    u2 = sys.argv[2]

    values = _compare(u1, u2)

    # calculate final similarity score
    content, domain, hrefs, img_urls = values
    thc, thd, thh, thiu = 0.25, 0.66, 0.02, 0.05
    final_values = _calculate_similarity_score(content, domain, hrefs, img_urls,
                                               _C_TH=thc, _D_TH=thd, _H_TH=thh, _IU_TH=thiu)

    # output
    _output(u1, u2, values, final_values, [thc, thd, thh, thiu])
