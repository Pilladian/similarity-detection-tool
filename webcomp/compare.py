# Python 3.8

import requests
import copy
import os
from bs4 import BeautifulSoup
import numpy as np
import cv2
import sys
from PIL import Image
import imgcompare
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from skimage.metrics import structural_similarity


# ------------------------------------------------------------------------------------------------ Compare
def compare(url1, url2):
    # comparing values
    _values = [compare_content(url1, url2),
               compare_domain(url1, url2),
               compare_hrefs(url1, url2),
               compare_image_sources(url1, url2),
               compare_screenshot(url1, url2)
               ]

    return _values


# ------------------------------------------------------------------------------------------------ Content
def compare_content(url1, url2):
    psl1 = _crawl_website(url1)
    psl2 = _crawl_website(url2)

    return _calculate_score(psl1, psl2)


def _crawl_website(url):
    w = requests.get(url)  # website html
    psb = w.content  # page source as bytes
    pss = psb.decode()  # page source as string
    psl = pss.split('\n')  # list of all lines split by '\n'
    ps_rhtml = _remove_html(psl)  # html markup removed

    return ps_rhtml


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


# ------------------------------------------------------------------------------------------------ Domain
def compare_domain(url1, url2):
    u1_components = _get_domain_components(url1)
    u2_components = _get_domain_components(url2)

    return _calculate_score(u1_components, u2_components)


# ------------------------------------------------------------------------------------------------ Hrefs
def compare_hrefs(url1, url2):
    url1_refs = [a for a in _get_hrefs(url1) if a != '#']
    url2_refs = [a for a in _get_hrefs(url2) if a != '#']

    return _calculate_score(url1_refs, url2_refs)


def _get_hrefs(url):
    w = requests.get(url)  # website html
    psb = w.content  # page source as bytes
    pss = psb.decode()  # page source as string

    soup = BeautifulSoup(pss, features="html5lib")
    href_list = [a['href'] for a in soup.find_all('a', href=True)]

    return href_list


# ------------------------------------------------------------------------------------------------ Image URLs
def compare_image_sources(url1, url2):
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


def _get_image_urls(url):
    w = requests.get(url)  # website html
    psb = w.content  # page source as bytes
    pss = psb.decode()  # page source as string

    img_list = []

    try:
        soup = BeautifulSoup(pss, features="html5lib")
        img_list = [a['src'] for a in soup.find_all('img')]
        img_list = [_get_domain_components(url) + _get_image_components(a) for a in img_list]
    except:
        pass

    return img_list


# ------------------------------------------------------------------------------------------------ Website Screenshot
def compare_screenshot(url1, url2):
    _store_screenshots([url1, url2])

    image1 = cv2.imread('sh_website0.png')
    image2 = cv2.imread('sh_website1.png')

    image1, image2 = _scale(image1, image2)

    mse = _mse(image1, image2)
    ssim = structural_similarity(image1, image2, multichannel=True)
    sim = _sim('sh_website0.png', 'sh_website1.png')

    value = 0.0

    if mse < 5000:
        value += 0.33
    if ssim > 0.85:
        value += 0.33
    if sim > 0.96:
        value += 0.33

    # delete created screenshots
    os.system('rm sh_website0.png sh_website1.png')
    return value


def _store_screenshots(urls):
    DRIVER = 'chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
    # driver.set_window_size(4096, 1024)

    for n, url in enumerate(urls):
        driver.get(url)
        driver.save_screenshot(f'sh_website{n}.png')

    driver.quit()


def _mse(img1, img2):
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img2.shape[1])

    return err


def _sim(path1, path2):
    i1 = Image.open(path1)
    i2 = Image.open(path2)

    width, height = i1.size
    i2 = i2.resize((width, height))
    i2 = i2.convert(i1.mode)

    return 1 - float(imgcompare.image_diff_percent(i1, i2) / 100)


def _scale(i1, i2):
    height, width, _ = i1.shape
    resized = cv2.resize(i2, (width, height), interpolation=cv2.INTER_AREA)

    return i1, resized


# ------------------------------------------------------------------------------------------------ URL helper functions
def _get_domain_components(url):
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


def _get_image_components(url):
    ol = url.split('/')
    nl = [a for a in ol if a != '']

    return nl


# ------------------------------------------------------------------------------------------------ Calculation functions
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


def calculate_final_similarity_scores(c, d, h, iu, sh, _C_TH, _D_TH, _H_TH, _IU_TH, _SH_TH):
    scores = [(_helper_calc(c, _C_TH, 2), 2.0),
              (_helper_calc(d, _D_TH, 2), 2.0),
              (_helper_calc(h, _H_TH, 3), 3.0),
              (_helper_calc(iu, _IU_TH, 3), 3.0),
              (_helper_calc(sh, _SH_TH, 1), 1.0)
              ]

    return scores


def calculate_final_similarity_scores_min(c, d, h, iu, _C_TH, _D_TH, _H_TH, _IU_TH):
    scores = [(_helper_calc(c, _C_TH, 2), 2.0),
              (_helper_calc(d, _D_TH, 2), 2.0),
              (_helper_calc(h, _H_TH, 3), 3.0),
              (_helper_calc(iu, _IU_TH, 3), 3.0)
              ]

    return scores


def _helper_calc(val, threshold, max_points, percentage=0.2):
    if val == 0.0:
        return 0.0

    rounds = 0
    for points in range(2 * max_points, -1, -1):
        if val > threshold - (rounds * (threshold * percentage)):
            return float(points / 2)
        rounds += 1

    return 0.0


# ------------------------------------------------------------------------------------------------ Output and Logging
def print_content(url1, url2, value_list, score_list, threshold_list, SCREEN=False):
    os.system('clear')
    testcases = ['Content', 'Domain', 'Hrefs', 'Image-Urls']
    if SCREEN:
        testcases.append('Screenshots')
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
    print(f'Final Similarity Score: {sum([a[0] for a in score_list])} / {"11.0" if SCREEN else "10.0"}\n')


def log(url1, url2, value_list, score_list, threshold_list):
    domain1 = '.'.join(_get_domain_components(url1))
    domain2 = '.'.join(_get_domain_components(url2))

    testcases = ['Content', 'Domain', 'Hrefs', 'Image-Urls', 'Screenshots']

    with open(f'./logs/{domain1}_{domain2}.log', 'w') as log_file:
        log_file.write(f'Check similarity for {url1} and {url2}\n\n')
        log_file.write('\tTest\t\t\tAchieved Score\t Similarity\t\tThreshold\n\n')

        for ind in range(len(testcases)):
            log_file.write(f'\t{testcases[ind]}'
                           f'{" " * (15 - len(testcases[ind]))}\t{score_list[ind][0]} / {score_list[ind][1]}'
                           f'\t\t {value_list[ind]:.2f}'
                           f'{" " * (15 - len(str(threshold_list[ind])))}{threshold_list[ind]}\n')

        log_file.write(f'\nFinal Similarity Score: {sum([a[0] for a in score_list])} / 11.0')


# ------------------------------------------------------------------------------------------------ Main
def main(url1, url2, _LOGGING=False):
    # Values received from testcases
    values = compare(url1, url2)

    # extract scores
    content, domain, hrefs, img_urls, screenshots = values

    # set thresholds
    thc, thd, thh, thiu, thsh = 0.25, 0.66, 0.02, 0.05, 0.66
    thresholds = [thc, thd, thh, thiu, thsh]

    # calculate final similarity scores
    final_values = calculate_final_similarity_scores(content,
                                                     domain,
                                                     hrefs,
                                                     img_urls,
                                                     screenshots,
                                                     _C_TH=thc,
                                                     _D_TH=thd,
                                                     _H_TH=thh,
                                                     _IU_TH=thiu,
                                                     _SH_TH=thsh
                                                     )

    # log output
    if _LOGGING:
        log(url1, url2, values, final_values, thresholds)

    return sum([a[0] for a in final_values])