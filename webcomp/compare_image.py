# Python 3.8

from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
import sys
from PIL import Image
import imgcompare


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


image1 = cv2.imread(sys.argv[1])
image2 = cv2.imread(sys.argv[2])

image1, image2 = scale(image1, image2)

mse = mse(image1, image2)
ssim = ssim(image1, image2, multichannel=True)
sim = sim(sys.argv[1], sys.argv[2])

print(f'MSE:\t{mse}\tsmall means suspicious\nSSIM:\t{ssim}\tclose to 1 means suspicious'
      f'\nSim:\t{sim}\tclose to 1 means suspicious')
# print(f'MSE:\t{mse}\t(the smaller the better)\nSSIM:\t{ssim}\t(the closer to 1 the better')
