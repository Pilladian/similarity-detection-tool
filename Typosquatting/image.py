# Python 3.8

from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2


def mse(img1, img2):
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img2.shape[1])

    return err


def scale(i1, i2):
    height, width, _ = i1.shape
    resized = cv2.resize(i2, (width, height), interpolation=cv2.INTER_AREA)

    return i1, resized


def test():
    # original = cv2.imread('/home/us3r/Downloads/original_facebook.svg')
    duplicate = cv2.imread('/home/us3r/Downloads/different_color_facebook.png')
    original = cv2.imread('/home/us3r/Downloads/different_color_facebook.png')

    original, duplicate = scale(original, duplicate)

    diff = cv2.subtract(original, duplicate)

    sift = xfeatures2d.SIFT_create()



image1 = cv2.imread("/home/us3r/Pictures/Me/20190724_231224.jpg")
image2 = cv2.imread("/home/us3r/Pictures/Memes/Screenshot_20200617-134129_9GAG.jpg")

image1, image2 = scale(image1, image2)

mse = mse(image1, image2)
ssim = ssim(image1, image2, multichannel=True)

print(mse, ssim)


test()