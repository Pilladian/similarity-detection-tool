# Python 3.7

import os
import cv2
from skimage.metrics import structural_similarity
import os
import os.path as path


def _compare_content(url1, url2):
    content_website_1 = Helper.crawl_website(url1)
    content_website_2 = Helper.crawl_website(url2)

    return Helper.get_percentage_similarity(content_website_1, content_website_2)


def _compare_domains(url1, url2):
    u1_components = Helper.get_domain_components(url1)
    u2_components = Helper.get_domain_components(url2)

    return Helper.get_percentage_similarity(u1_components, u2_components)


def _compare_links(url1, url2):
    url1_refs = [a for a in Helper.get_hrefs(url1) if a != '#']
    url2_refs = [a for a in Helper.get_hrefs(url2) if a != '#']

    return Helper.get_percentage_similarity(url1_refs, url2_refs)


def _compare_image_sources(url1, url2):
    image_l1 = Helper.get_image_urls(url1)
    image_l2 = Helper.get_image_urls(url2)

    #print(image_l1)
    #print(image_l2)

    va = []
    for a in image_l1:
        for b in image_l2:
            va.append(Helper.get_percentage_similarity(a, b))

    try:
        return sum(va) / len(va)
    except ZeroDivisionError:
        return 0.0


def _compare_screenshots(url1, url2):
    Helper.create_screenshots([url1, url2])

    image1 = cv2.imread('sh_website0.png')
    image2 = cv2.imread('sh_website1.png')

    image1, image2 = Helper.scale(image1, image2)

    mse = Helper.mse(image1, image2)
    ssim = structural_similarity(image1, image2, multichannel=True)
    sim = Helper.sim('sh_website0.png', 'sh_website1.png')

    value = 0.0

    if mse < 4000:
        value += 0.33
    if ssim > 0.85:
        value += 0.33
    if sim > 0.97:
        value += 0.33

    # delete created screenshots
    os.system('rm sh_website0.png sh_website1.png')
    return value


def _calculate_points(content,   domains,   links,     img_sources, screen,
                      TH_C=0.25, TH_D=0.66, TH_L=0.02, TH_I=0.05,   TH_S=0.99):

    # contains tuple (achieved_points, max_points)
    points = [(Helper.calculate_points(content,     TH_C, 2), 2.0),
              (Helper.calculate_points(domains,     TH_D, 2), 2.0),
              (Helper.calculate_points(links,       TH_L, 2), 2.0),
              (Helper.calculate_points(img_sources, TH_I, 2), 2.0),
              (Helper.calculate_points(screen,      TH_S, 2, percentage_steps=0.33), 2.0)
              ]

    return points


class Comparer:

    def __init__(self):
        self._LOGGING = False
        self.path = ''

        self.url1 = ""
        self.domain1 = ""
        self.url2 = ""
        self.domain2 = ""

    def disable_logging(self):
        self._LOGGING = False

    def enable_logging(self, p):
        self.path = p
        self._LOGGING = True
        return f'{self.path}{self.domain2}.log'

    def set_parameter(self, url1, url2):
        self.url1 = url1
        self.domain1 = Helper.get_domain(url1)
        self.url2 = url2
        self.domain2 = Helper.get_domain(url2)

    def log(self, similarity_values, similarity_points, thresholds):
        testcases = ['Content', 'Domain', 'Links', 'Image-Urls', 'Screenshots']
#        with open(f'{self.path}{self.domain2}.log', 'w') as log_file:
#            log_file.write(f'Check similarity for {self.url1} and {self.url2}\n\n')
#            log_file.write('\tTest\t\t\tAchieved Score\t Similarity\tThreshold\n\n')
#
#            for ind in range(len(testcases)):
#                log_file.write(f'\t\t{testcases[ind]}'
#                               f'{" " * (15 - len(testcases[ind]))}\t{similarity_points[ind][0]} / {similarity_points[ind][1]}'
#                               f'\t\t {similarity_values[ind]:.2f}'
#                               f'{" " * (15 - len(str(thresholds[ind])))}{thresholds[ind]}\n')
#
#            log_file.write(f'\nFinal Similarity Score: {sum([a[0] for a in similarity_points])} / {sum([a[1] for a in similarity_points])}\n')

        with open(f'{self.path}{self.domain2}.log', 'w') as log_file:
            log_file.write('{')
            log_file.write(f'url1:{self.url1}, ')
            log_file.write(f'url2:{self.url2}, ')
            for ind in range(len(testcases)):
                log_file.write(f'{testcases[ind]}:({similarity_points[ind][0]}, {similarity_points[ind][1]}, {similarity_values[ind]}, {thresholds[ind]})')
                if ind != len(testcases) - 1:
                    log_file.write(', ')
            log_file.write('}')

    def compare_websites(self):

        # Content
        similarity_percentage_content = _compare_content(self.url1, self.url2)

        # Domains
        similarity_percentage_domains = _compare_domains(self.url1, self.url2)

        # Links
        similarity_percentage_links = _compare_links(self.url1, self.url2)

        # Image Sources
        similarity_percentage_img_sources = _compare_image_sources(self.url1, self.url2)

        # Website Screenshots
        similarity_percentage_screenshots = _compare_screenshots(self.url1, self.url2)

        # set thresholds for components
        th_content = 0.25
        th_domains = 0.66
        th_links = 0.02
        th_img_sources = 0.05
        th_screen = 0.99

        # calculate points based on percentages
        similarity_points = _calculate_points(similarity_percentage_content,
                                              similarity_percentage_domains,
                                              similarity_percentage_links,
                                              similarity_percentage_img_sources,
                                              similarity_percentage_screenshots,
                                              TH_C=th_content,
                                              TH_D=th_domains,
                                              TH_L=th_links,
                                              TH_I=th_img_sources,
                                              TH_S=th_screen
                                              )

        if self._LOGGING:
            self.log([similarity_percentage_content,
                      similarity_percentage_domains,
                      similarity_percentage_links,
                      similarity_percentage_img_sources,
                      similarity_percentage_screenshots
                      ],
                     similarity_points,
                     [th_content,
                      th_domains,
                      th_links,
                      th_img_sources,
                      th_screen
                      ])

        # return achieved similarity points, max. similarity points
        return sum([a[0] for a in similarity_points]), sum([a[1] for a in similarity_points])

try:
    from webcomp import Helper
except ModuleNotFoundError:
    import Helper
