# Python 3.8

import sys
from PIL import Image
import imgcompare


def _scale(img1, img2):
    width, height = img1.size
    img2 = img2.resize((width, height))
    img2 = img2.convert(img1.mode)

    return img1, img2


def _compare_images(img_path_1, img_path_2):
    try:
        i1 = Image.open(img_path_1)
        i2 = Image.open(img_path_2)

        si1, si2 = _scale(i1, i2)

        return float(f'{imgcompare.image_diff_percent(si1, si2) / 100:.2f}')
    except Exception as e:
        print(f'Error occurred: {e}')


if __name__ == '__main__':
    _THRESHOLD = 0.6
    im1 = sys.argv[1]
    im2 = sys.argv[2]

    val = 1 - _compare_images(im1, im2)
    print(f'{val:.2} >= {_THRESHOLD} --> Suspicious' if val > _THRESHOLD else f'{val} < {_THRESHOLD} --> Not suspicious')