from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import ntpath
import cv2
from PIL import Image

def depth_read(filename, count):

    image = Image.open(filename)

    image.save('./rgb1/%s.png'%count)

    # depth[depth_png == 0] = -1.
    return image

def get_path_list(file_dir, fname):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):    # 遍历文件目录下每一个文件
            if fname in file:  # 判断是否包含指定字符串
                L.append(os.path.join(root, file))

if __name__ == '__main__':
    dir = './rgb'  # 文件夹名
    dirs = os.listdir(dir)      #    ['(1).png', '(10).png', '(100).png', '(1000).png', '(1
    count = 0
    for dir1 in dirs:
        print(dir1)
        imgpath = dir + '/' +dir1

        count += 1
        depth = depth_read(imgpath, count)