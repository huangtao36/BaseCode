#-*-coding:utf-8-*-

"""
这个代码用于将16bit的图像数据转换为8bit并保存，原使用对象为KITTI的深度数据集
"""

import numpy as np
import os
from PIL import Image


def get_path_list(file_dir, fname):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):    # 遍历文件目录下每一个文件
            if fname in file:  # 判断是否包含指定字符串
                L.append(os.path.join(root, file))


if __name__ == '__main__':

    dir = './depth_val_000' 
    dirs = os.listdir(dir) 

    for dir1 in dirs:
        imgpath = dir + '/' +dir1
        image = Image.open(imgpath)

        depth_png = np.array(image, dtype=int)

        depth = depth_png.astype(np.float) / 256.

        image2 = Image.fromarray(depth).convert('L')

        image2.save('./test/%s' % dir1)




