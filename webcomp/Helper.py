# Python

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
import os


def print_error(e, fn):
    print(f'Error occured in {fn} : {e}\n')

def crawl_website(url):
    try:
        w = requests.get(url)           # website html
        psb = w.content                 # page source as bytes
        pss = decode(psb)               # page source as string
        psl = pss.split('\n')           # list of all lines split by '\n'
        ps_rhtml = remove_html(psl)     # html markup removed
        ps = []
        for xline in ps_rhtml:
            line = ''.join(xline.split('\t'))
            if line != '':
                ps.append(line)
        return ps
    except Exception as e:
        # print_error(e, 'crawl_website')
        return []


def remove_html(lines):
    clean_lines = []

    for line in lines:
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

        clean_lines.append(' '.join(new))

    for e in copy.deepcopy(clean_lines):
        if e == '' or e == '\t':
            clean_lines.remove(e)

    return clean_lines


def get_domain_components(url):
    cs = url.split('https://')
    cs = ''.join(cs).split('http://')
    cs = ''.join(cs).split('#')[0]
    cs = ''.join(cs).split('/')[0]
    cs = ''.join(cs).split('.')
    return cs


def get_domain(url):
    cs = url.split('https://')
    cs = ''.join(cs).split('http://')
    cs = ''.join(cs).split('#')[0]
    cs = ''.join(cs).split('/')[0]
    return cs


def get_image_components(url):
    ol = url.split('https://')
    ol = ''.join(ol).split('http://')
    ol = ''.join(ol).split('/')
    nl = [a for a in ol if a not in ['', 'wp-content', 'uploads']]
    return nl


def get_percentage_similarity(l1, l2):
    same1 = 0
    same2 = 0

    for element in l1:
        if element in l2:
            same1 += 1

    for element in l2:
        if element in l1:
            same2 += 1

    try:
        return float((same1 + same2) / (len(l1) + len(l2)))
    except ZeroDivisionError:
        # print_error(e, 'get_percentage_similarity')
        return 0.0

def get_hrefs(url):
    try:
        w = requests.get(url)   # website html
        psb = w.content         # page source as bytes
        pss = decode(psb)  # page source as string

        soup = BeautifulSoup(pss, features="html5lib")
        hrefs = [a['href'] for a in soup.find_all('a', href=True)]
        links = []
        for a in soup.find_all('link', href=True):
            if isinstance(a['href'], list):
                for el in a['href']:
                    links.append(el)
            else:
                links.append(a['href'])
        return hrefs + links

    except Exception as e:
        # print_error(e, 'get_hrefs')
        return []


def get_image_urls(url):
    try:
        w = requests.get(url)   # website html
        psb = w.content         # page source as bytes
        pss = decode(psb)  # page source as string
    except:
        return []

    img_list = []
    try:
        soup = BeautifulSoup(pss, features="html5lib")
        img_list = [a['src'] for a in soup.find_all('img')]
        img_list = [get_image_components(a) for a in img_list]

    except Exception as error:
        pass
        # print_error(error, 'get_image_urls')

    return img_list


def create_screenshots(urls):
    try:
        DRIVER = 'chromedriver'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)

        for n, url in enumerate(urls):
            driver.get(url)
            driver.save_screenshot(f'sh_website{n}.png')

        driver.quit()
    except Exception as error:
        pass
        # print_error(error, 'create_screenshots')


def mse(img1, img2):
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img2.shape[1])
    return err


def sim(path1, path2):
    i1 = Image.open(path1)
    i2 = Image.open(path2)

    width, height = i1.size
    i2 = i2.resize((width, height))
    i2 = i2.convert(i1.mode)

    return 1 - float(imgcompare.image_diff_percent(i1, i2) / 100)


def scale(i1, i2):
    height, width, _ = i1.shape
    resized = cv2.resize(i2, (width, height), interpolation=cv2.INTER_AREA)

    return i1, resized


def calculate_points(percentage, threshold, max_points, percentage_steps=0.2):
    # if similarity percentage is 0
    if percentage == 0.0:
        return 0.0

    # decrease max_points in each step
    rounds = 0
    for points in range(2 * max_points, -1, -1):
        if percentage > threshold - (rounds * (threshold * percentage_steps)):
            return float(points / 2)
        rounds += 1

    return 0.0


def decode(cont):
    try:
        pss = cont.decode()  # page source as string
    except:
        pss = cont.decode(encoding='ISO-8859-1')

    return pss
