import numpy as np
import os
from PIL import Image

'''
归一化为0-255范围
'''
def normalize(image):
    max = np.max(image)
    min = np.min(image)
    #minA = A.min()
    #maxA = A.max()
    normalized = (image - min) / (max - min) * 255.0
    # normalized = np.minimum(np.maximum(image, 0), 255.0) / 255.0 * (max - min) + min
    return normalized

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
    dir = './groundtruth'  # 文件夹名
    dirs = os.listdir(dir)      #    ['(1).png', '(10).png', '(100).png', '(1000).png', '(1

    for dir1 in dirs:
        imgpath = dir + '/' +dir1

        image = Image.open(imgpath)
        depth_image = normalize(image)

        image2 = Image.fromarray(depth_image).convert('L')
        image2.save('./groundtruth1/%s' % dir1)




