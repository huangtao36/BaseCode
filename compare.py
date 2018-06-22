#-*-coding:utf-8-*-
"""
这个代码用于比较两张图片
"""


import numpy as np
from scipy.misc import imread
from matplotlib import pyplot as plt

im_realB = "./epoch111_real_B.png"
im_fakeB = "./epoch111_fake_B.png"

r = imread(im_realB)
f = imread(im_fakeB) 
print(type(r), r.shape)
print(type(f), f.shape)



print(r.max(), r.min(), f.max(), f.min())

fig = plt.figure()

image = fig.add_subplot(221)
image.imshow(f)
# image.imshow(f[100:200, 200:400])

image = fig.add_subplot(222)
image.imshow(r)
# image.imshow(r[100:200, 200:400])

image = fig.add_subplot(223)
image.imshow(np.abs(r-f)/(r+0.0001))

plt.show()