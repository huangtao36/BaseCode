import cv2
import numpy as np

img1 = cv2.imread('1.png')
img2 = cv2.imread('2.png')

img_mix = cv2.addWeighted(img1, 1, img2, 1, 0)

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img_mix', img_mix)

cv2.waitKey(0)
cv2.destroyAllWindows()