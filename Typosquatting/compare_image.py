# Python 3.8

import sys
from PIL import Image
import numpy
from numpy import asarray


def _pooling(img):
    _KERNEL_SIZE = 20

    height, width = img.size
    np_img = asarray(img)

    vertical_squares = int(height / _KERNEL_SIZE)
    horizontal_squares = int(width / _KERNEL_SIZE)

    for y in range(vertical_squares):
        yb = y * _KERNEL_SIZE
        for x in range(horizontal_squares):
            xb = x * _KERNEL_SIZE

            pixel = numpy.zeros(vertical_squares, horizontal_squares)
            for h in range(yb, yb + _KERNEL_SIZE):
                for w in range(xb, xb + _KERNEL_SIZE):
                    pixel[h - yb][w - xb] = np_img[h][w]

            print(pixel.shape)

    print(vertical_squares, horizontal_squares)

    return None


def _compare(image1, image2, threshold):
    suspicious = False

    # load images
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    # pooling
    p_img1 = _pooling(img1)
    p_img2 = _pooling(img2)

    # compare value
    value = 0

    return suspicious, value


if __name__ == '__main__':
    _THRESHOLD = 0.2
    i1 = sys.argv[1]
    i2 = sys.argv[2]

    sus, val = _compare(i1, i2, _THRESHOLD)
    print(f'{val:.2} >= {_THRESHOLD} --> Suspicious' if val else f'{val} < {_THRESHOLD} --> Not suspicious')