#!/usr/bin/python

from PIL import Image
import numpy as np

image = Image.open('./real/131_real_B.png')
# image1 = image.resize((608, 176), Image.ANTIALIAS)
# image2 = image1.resize((1216, 352), Image.ANTIALIAS)

#
# depth_png = np.array(image, dtype=int)
# # depth_png1 = np.array(image1, dtype=int)
# # depth_png2 = np.array(image2, dtype=int)
# # image.show()
#
# print(np.max(depth_png))
# # print(np.max(depth_png1))
# # print(np.max(depth_png2))
#
# print(np.min(depth_png))
# # print(np.min(depth_png1))
# print(np.min(depth_png2))

count = np.count_nonzero(np.array(image) > 0)
print(count/(608.0*176.0))