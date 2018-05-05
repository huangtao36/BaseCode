import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
# %matplotlib inline


# df = DataFrame(np.random.randn(10,10))
# fig = plt.figure(figsize=(12,5))
# ax = fig.add_subplot(111)

image = plt.imread("epoch200_fake_B.png")

axim = plt.imshow(image,interpolation='nearest', cmap='hsv')#cmap=plt.cm.gray_r, #cmap用来显示颜色，可以另行设置
plt.colorbar(axim)
plt.show()