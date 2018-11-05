import os
from PIL import Image

import torch
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread

a = torch.load('Cen.p')
im = a.numpy().squeeze()
# plt.imshow(im)
plt.subplot(211)
plt.hist(im.flatten()*255, bins=200)
plt.xlim([0,200])
plt.ylim([0,2000])
# plt.show()

im_ = Image.open('1.png').convert('L')
im2_ = imread('1.png')

plt.subplot(212)
plt.hist(im2_.flatten(), bins = 200)
plt.xlim([1, 200])
plt.ylim([0, 2000])
plt.show()