import numpy as np
from PIL import Image
import re
import os

def get_path_list(file_dir, fname):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):    # 遍历文件目录下每一个文件
            if fname in file:  # 判断是否包含指定字符串
                L.append(os.path.join(root, file))

'''
创建文件夹
'''
def make_dirs(paths):
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

'''
归一化为min-max范围
'''
def normalize(image, max, min):
    image_max = 85.
    image_min = np.min(image)
    normalized = (image - image_min) / (image_max - image_min) * (max - min)
    return normalized

'''
像素数据扩展:(原图片路径， 要保存的路径， 最大值保存文件路径)
'''
def pix_expand(dir, expand_dir):
    image_list = os.listdir(dir)    # 文件夹dir内的文件列表

    make_dirs(expand_dir)

    for dir1 in image_list:
        print(dir1)
        imgpath = dir + '/' + dir1

        image = Image.open(imgpath)

        image_normalize = normalize(image, 255, 0)  # 归一化图片

        image2 = Image.fromarray(image_normalize).convert('L')  # 转换图像数据为Image可读形式
        # image2.show()

        image2.save('%s/%s' % (expand_dir, dir1))

    print("expand done.")


if __name__ == '__main__':

    dir = './real_C'  # 原图片文件夹
    # dir = './groundtruth'
    expand_dir = './get'
    # sparse_data_file = os.path.join('./groundtruth_max.txt')   # 要保存的最大值文件路径

    pix_expand(dir, expand_dir)

    # reconstruction(max_data_file, expand_dir, reconstruction_dir)