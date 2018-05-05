import matplotlib.pyplot as plt
import numpy as np
import cv2


image = cv2.imread("./116.png")
# print(image)

mask = (image > 0) * 255
# print(mask)

cv2.imwrite('./mask.png', mask)

# cv2.imshow('image',mask)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()