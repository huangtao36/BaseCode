#-*-coding:utf-8-*-
"""
这个代码用于分区域裁剪图片，自己设定裁剪区域，裁剪图片并另外保存
"""

from PIL import  Image
import numpy as np
import os
from PIL import Image


'''
获得文件路径列表
'''
def get_path_list(file_dir, fname):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):    # 遍历文件目录下每一个文件
            if fname in file:  # 判断是否包含指定字符串
                L.append(os.path.join(root, file))

if __name__ == '__main__':
    dir = './dataset_800_200/test/rgb'  # 文件夹名
    dirs = os.listdir(dir)      #    ['(1).png', '(10).png', '(100).png', '(1000).png', '(1

    for file in dirs:
        print(file)
        count = 1
        # print(dir1)
        imgpath = dir + '/' + file
        # print(file_name)

        file_name = file.split(".")

        file_name = file_name[0]
        # print(type(file_name))

        image = Image.open(imgpath)

        region1 = (0, 0, 608, 176)
        region2 = (608, 0, 1216, 176)

        region3 = (0, 176, 608, 352)
        region4 = (608, 176, 1216, 352)

        # 裁切图片
        cropImg1 = image.crop(region1)
        cropImg2 = image.crop(region2)
        cropImg3 = image.crop(region3)
        cropImg4 = image.crop(region4)

        # 保存裁切后的图片
        cropImg1.save('./rgb/%s_%s.png' %(file_name, count))
        count += 1
        cropImg2.save('./rgb/%s_%s.png' %(file_name, count))
        count += 1
        cropImg3.save('./rgb/%s_%s.png' % (file_name, count))
        count += 1
        cropImg4.save('./rgb/%s_%s.png' % (file_name, count))


