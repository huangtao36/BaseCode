import numpy as np
from PIL import Image
import re
import os
from scipy.misc import imread
import cv2



if __name__ == '__main__':

    dir = './dataset10/train/groundtruth'  # 原图片文件夹

    image_list = os.listdir(dir)  # 文件夹dir内的文件列表

    Sum_mean =0
    Sum_std = 0

    for dir1 in image_list:
        imgpath = dir + '/' + dir1
        # print(imgpath)

        image = cv2.imread(imgpath)

        count = np.count_nonzero(image[:, :, 0] > 0)

        mask = image > 0
        # print(mask)

        mean = np.sum(image[:, :, 0])/count
        Sum_mean += mean
        std = np.sqrt(np.sum((image[image>0]-mean)**2)/count)
        Sum_std += std

        # std = np.std(image[:, :, 0])
        # std = sqrt(mean(abs(x - x.mean())**2))

        # print(R_std)

        print("mean is %f, std is %f" % (mean, float(std)))

    avr_mean = Sum_mean/10
    avr_std = Sum_std/10
    print("avr_mean is %f, avr_std is %f" % (avr_mean, avr_std))