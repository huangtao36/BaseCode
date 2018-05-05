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
    image_max = np.max(image)
    image_min = np.min(image)
    normalized = (image - image_min) / (image_max - image_min) * (max - min)
    return normalized

'''
获取最大值并保存到txt
'''
def save_max_data(image, image_name, save_file):
    image_max = np.max(image)
    # image_min = np.min(image)

    message = 'image: %s, max: %s\n' % (image_name, image_max)
    with open(save_file, "a") as file:
        file.write('%s' % message)

    return image_max

'''
读取txt文件内容，并缓存到列表
'''
def get_data(dir):
    data = []
    data_list = []
    fp = open(dir, 'r')
    for ln in fp:
        if 'image: ' in ln:
            '''
            image: 964.png, max: 77
            image: 965.png, max: 77
            '''
            #eopch
            arr = re.findall(r'image: \b\d+\b', ln)
            image = int(arr[0].strip(' ')[7:])
            data.append(image)
            #iters
            arr1 = re.findall(r'max: \b\d+\b', ln)
            max = int(arr1[0].strip(' ')[4:])
            data.append(max)

            data_list.append(data)
        data = []
    fp.close()
    return data_list

'''
像素数据扩展:(原图片路径， 要保存的路径， 最大值保存文件路径)
'''
def pix_expand(dir, expand_dir, max_data_file):
    image_list = os.listdir(dir)    # 文件夹dir内的文件列表

    make_dirs(expand_dir)

    for dir1 in image_list:
        imgpath = dir + '/' + dir1

        image = Image.open(imgpath)


        image_max = save_max_data(image, dir1, max_data_file)  # 保存图片像素最大值，(图片，文件名)，返回图片最大值

        image_normalize = normalize(image, 255, 0)  # 归一化图片

        image2 = Image.fromarray(image_normalize).convert('L')  # 转换图像数据为Image可读形式
        # image2.show()

        image2.save('%s/%s' % (expand_dir, dir1))

        print(image_max)
    print("expand done.")

'''
像素数据恢复：(最大值保存文件路径，扩张后的图片存储路径，重建后的图片保存路径)
'''
def reconstruction(data_file_dir, expand_dir, reconstruction_dir):
    image_list = os.listdir(expand_dir)  # 文件夹dir内的文件列表
    data = get_data(data_file_dir)
    # print(data)
    # print(data[2][0])

    for dir1 in image_list:
        imgpath = expand_dir + '/' + dir1
        print(dir1)

        image = Image.open(imgpath)

        image_name = int(re.sub("\D", "", dir1))

        for image_parameter in data:
            if image_parameter[0] == image_name:
                image_reconstruct = normalize(image, image_parameter[1], 0)
                image2 = Image.fromarray(image_reconstruct).convert('L')  # 转换图像数据为Image可读形式
                # image2.show()
                make_dirs(reconstruction_dir)
                image2.save('./%s/%s' % (reconstruction_dir, dir1))
    print("reconstruction done.")

if __name__ == '__main__':

    dir = './dataset10/train/sparse'  # 原图片文件夹
    # dir = './groundtruth'
    expand_dir = './dataset10_expand/train/sparse'

    # reconstruction_dir = './sparse2'
    max_data_file = './dataset10_expand/train/sparse_max.txt'

    # sparse_data_file = os.path.join('./groundtruth_max.txt')   # 要保存的最大值文件路径

    pix_expand(dir, expand_dir, max_data_file)

    # reconstruction(max_data_file, expand_dir, reconstruction_dir)